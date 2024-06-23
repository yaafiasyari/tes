import db_config
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

# Database connection setup
DATABASE_URI = f'postgresql+psycopg2://{db_config.get_user()}:{db_config.get_passwd()}@{db_config.get_host()}:5431/{db_config.get_db()}'
engine = create_engine(DATABASE_URI)

def get_product():
    select_query = text("SELECT * FROM products.products;")
    try:
        with engine.connect() as conn:
            result = conn.execute(select_query)
            # Convert the result to a pandas DataFrame
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        return None
    
def get_product_master():
    select_query = text("SELECT * FROM products.product_master;")
    try:
        with engine.connect() as conn:
            result = conn.execute(select_query)
            # Convert the result to a pandas DataFrame
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        return None
    
def get_raw_products():
    select_query = text("SELECT * FROM products.raw_products;")
    try:
        with engine.connect() as conn:
            result = conn.execute(select_query)
            # Convert the result to a pandas DataFrame
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        return None


# print(get_product())
# print(get_product_master())
# print(get_raw_products())