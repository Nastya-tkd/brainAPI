from sqlalchemy.orm import Session
from app import models, schemas


def compare_nanoparticles(db: Session, organ: str, nanoparticle_types: list[str]):
    results = []
    for np_type in nanoparticle_types:
        nanoparticles = db.query(models.Nanoparticle).filter(
            models.Nanoparticle.nanoparticle_type == np_type
        ).all()

        if not nanoparticles:
            continue

        accumulations = [getattr(n, organ) for n in nanoparticles]
        avg_accumulation = sum(accumulations) / len(accumulations)

        results.append(schemas.AnalysisResult(
            nanoparticle_type=np_type,
            organ=organ,
            average_accumulation=avg_accumulation
        ))

    return sorted(results, key=lambda x: x.average_accumulation, reverse=True)


def find_most_effective(db: Session, target_organ: str, min_samples: int = 2):
    from collections import defaultdict

    type_accumulations = defaultdict(list)

    nanoparticles = db.query(models.Nanoparticle).all()
    for np in nanoparticles:
        type_accumulations[np.nanoparticle_type].append(getattr(np, target_organ))

    results = []
    for np_type, accumulations in type_accumulations.items():
        if len(accumulations) >= min_samples:
            avg = sum(accumulations) / len(accumulations)
            results.append(schemas.AnalysisResult(
                nanoparticle_type=np_type,
                organ=target_organ,
                average_accumulation=avg
            ))

    return sorted(results, key=lambda x: x.average_accumulation, reverse=True)