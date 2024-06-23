import db_config
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Database connection setup
DATABASE_URI = f'postgresql+psycopg2://{db_config.get_user()}:{db_config.get_passwd()}@{db_config.get_host()}:5431/{db_config.get_db()}'
engine = create_engine(DATABASE_URI)

try:
    print("Truncating product_master table")
    truncate_query = text("TRUNCATE TABLE products.product_master;")
    with engine.connect() as conn:
        conn.execute(truncate_query)
    print("Table truncated successfully.")
    
    insert_query = text("""
    insert into products.product_master (type,
name,
detail)
select distinct type,name,detail from products.product_master rp 
    """)
    
    with engine.connect() as conn:
        conn.execute(insert_query)
    print("Table inserted successfully.")
except SQLAlchemyError as e:
    print(f"Error occurred: {e}")
