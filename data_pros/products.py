import db_config
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Database connection setup
DATABASE_URI = f'postgresql+psycopg2://{db_config.get_user()}:{db_config.get_passwd()}@{db_config.get_host()}:5431/{db_config.get_db()}'
engine = create_engine(DATABASE_URI)

try:
    print("Truncating products table")
    truncate_query = text("TRUNCATE TABLE products.products;")
    with engine.connect() as conn:
        conn.execute(truncate_query)
    print("Table truncated successfully.")
    
    insert_query = text("""
    insert into products.products (
        name,
        price,
        originalprice,
        discountpercentage,
        detail,
        platform,
        productmasterid,
        created_date)
        select rp.name,
        discounted_price as price,
        original_price as originalprice,
        discount_percentage as discountpercentage,
        rp.detail,
        platform,
        pm.id as productmasterid,
        created_date
        from products.raw_products rp 
        join products.product_master pm on rp."name" = pm."name" and rp.detail = pm.detail  


    """)
    
    with engine.connect() as conn:
        conn.execute(insert_query)
    print("Table inserted successfully.")
except SQLAlchemyError as e:
    print(f"Error occurred: {e}")
