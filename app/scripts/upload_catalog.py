import pandas as pd
from dotenv import load_dotenv


load_dotenv()
from app.models.ProductCatalog import ProductCatalog
from sqlalchemy import insert
from app.database import SessionLocal  # Import your existing connection


def sync_catalog(file_path: str):
    # 1. Read Excel
    df = pd.read_excel(file_path)

    # 2. Match column names to your SQLAlchemy model attributes
    # Converts 'Order_number' -> 'order_number'
    df.columns = [c.lower().replace(' ', '') for c in df.columns]

    # 3. Handle Dates (Crucial for Postgres Date columns)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date']).dt.date

    session = SessionLocal()
    failed = 0
    successful = 0

    records = df.to_dict(orient="records")

    # 4. Create tables if they don't exist
    # This uses your existing engine to check the DB
    # Base.metadata.create_all(bind=engine)

    # 5. Dump data
    for record in records:
        try:
            stmnt = insert(ProductCatalog).values(**record)
            session.execute(stmnt)
            session.commit()
            successful += 1

        except FileNotFoundError as e:
            session.rollback()  # Important: Reset the transaction after an error
            failed += 1
            print(f"Skipping row due to error: {e}")
            continue
        except Exception as e:
            session.rollback()  # Important: Reset the transaction after an error
            failed += 1
            print(f"Skipping row due to error: {e}")
            continue

    print("Successful imports: {}".format(successful))
    print("Failed imports: {}".format(failed))


if __name__ == "__main__":
    sync_catalog("C:\\Users\\mn Technology Group\\Downloads\\all-products.xlsx")
