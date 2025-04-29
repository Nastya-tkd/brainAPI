import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Nanoparticle, Experiment, AccumulationData

# Настройка подключения к SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./nanoparticles.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание таблиц
Base.metadata.create_all(bind=engine)


def import_excel_to_db(file_path: str):
    db = SessionLocal()

    try:
        # Чтение Excel файла, пропуская первые 2 строки (заголовки)
        df = pd.read_excel(file_path, sheet_name='Лист1', header=None, skiprows=2)

        # Создаем эксперименты
        experiments = {
            "Без цитоблокады": db.query(Experiment).filter(Experiment.name == "Без цитоблокады").first() or
                               Experiment(name="Без цитоблокады", description="Эксперимент без цитоблокады"),
            "С цитоблокадой": db.query(Experiment).filter(Experiment.name == "С цитоблокадой").first() or
                              Experiment(name="С цитоблокадой", description="Эксперимент с цитоблокадой"),
            "Эксперимент с магнитом + везикулы": db.query(Experiment).filter(
                Experiment.name == "Эксперимент с магнитом + везикулы").first() or
                                                 Experiment(name="Эксперимент с магнитом + везикулы",
                                                            description="Эксперимент с магнитом + везикулы")
        }

        for exp in experiments.values():
            db.add(exp)
        db.commit()

        # Функция для обработки строки
        def process_row(row, exp_name, np_col, start_col):
            np_name = row.iloc[np_col] if isinstance(row, pd.Series) else row[np_col]
            if pd.isna(np_name) or not isinstance(np_name, str):
                return

            try:
                # Извлекаем номер мыши
                mouse_num = int(np_name.split("(")[-1].replace("Мышь ", "").replace(")", ""))

                # Получаем название наночастицы
                np_base_name = np_name.split("(")[0].strip()

                # Создаем или получаем наночастицу
                nanoparticle = db.query(Nanoparticle).filter(Nanoparticle.name == np_base_name).first()
                if not nanoparticle:
                    nanoparticle = Nanoparticle(name=np_base_name)
                    db.add(nanoparticle)
                    db.commit()

                # Создаем запись о накоплении
                accumulation = AccumulationData(
                    nanoparticle_id=nanoparticle.id,
                    experiment_id=experiments[exp_name].id,
                    mouse_number=mouse_num,
                    lungs=row.iloc[start_col] if not pd.isna(row.iloc[start_col]) else None,
                    liver=row.iloc[start_col + 1] if not pd.isna(row.iloc[start_col + 1]) else None,
                    kidneys=row.iloc[start_col + 2] if not pd.isna(row.iloc[start_col + 2]) else None,
                    spleen=row.iloc[start_col + 3] if not pd.isna(row.iloc[start_col + 3]) else None,
                    brain=row.iloc[start_col + 4] if not pd.isna(row.iloc[start_col + 4]) else None,
                    heart=row.iloc[start_col + 5] if not pd.isna(row.iloc[start_col + 5]) else None
                )
                db.add(accumulation)
            except Exception as e:
                print(f"Ошибка обработки строки: {np_name}. Ошибка: {str(e)}")

        # Обрабатываем данные
        for _, row in df.iterrows():
            # Данные без цитоблокады (столбцы A-H)
            process_row(row, "Без цитоблокады", 0, 1)

            # Данные с цитоблокадой (столбцы I-P)
            process_row(row, "С цитоблокадой", 8, 9)

            # Эксперимент с магнитом (столбцы Q-W)
            process_row(row, "Эксперимент с магнитом + везикулы", 16, 17)

        db.commit()
        print("Данные успешно импортированы!")

    except Exception as e:
        db.rollback()
        print(f"Ошибка при импорте данных: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Использование: python testsss.py <путь_к_excel_файлу>")
    else:
        import_excel_to_db(sys.argv[1])