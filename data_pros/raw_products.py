import db_config
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Database connection setup
DATABASE_URI = f'postgresql+psycopg2://{db_config.get_user()}:{db_config.get_passwd()}@{db_config.get_host()}:5431/{db_config.get_db()}'
engine = create_engine(DATABASE_URI)

try:
    # Truncate raw_products table
    print("Truncating raw_products table")
    truncate_query = text("TRUNCATE TABLE products.raw_products;")
    with engine.connect() as conn:
        conn.execute(truncate_query)
    print("Table truncated successfully.")
    
    # Insert data into raw_products table
    insert_query = text("""
    insert into products.raw_products (
full_name_prodct,
type,
name,
detail,
original_price,
discounted_price,
discount_percentage,
platform,
created_date)
SELECT 
	name as full_name_prodct,
    category as type,
    REGEXP_REPLACE(
    REGEXP_REPLACE(
        REGEXP_REPLACE(
            name, 
            '\s\d+(\.\d+)?\s?(ml|gram|g|kg|ltr|liter|pcs|pack|isi|L).*$|\[Buy\s\d\sGet\s\d\]', 
            '', 
            'gi'
        ), 
        '\b(\d+)X\d+(\.\d+)?(ml|gram|g|kg|ltr|liter|pcs|pack|isi|L)\b', 
        '\1', 
        'gi'
    ),
    'Buy\s',
    '',
    'gi'
) AS name,
    regexp_replace(name, '.*?(\d+[GgMmLl]+).*', '\1', 'i') AS detail,
    original_price,
	discounted_price,
	discount_percentage,
	platform,
	created_date
FROM 
    products.landing_product_tokopedia lpi
union ALL
SELECT 
	name as full_name_prodct,
    category as type,
    REGEXP_REPLACE(
    REGEXP_REPLACE(
        REGEXP_REPLACE(
            name, 
           'Buy\s',
    '',
    'gi'
        ), 
        '\s\d+(\.\d+)?\s?(ml|gram|g|kg|ltr|liter|pcs|pack|isi|L).*$|\[Buy\s\d\sGet\s\d\]', 
            '', 
            'gi'
        
    ),
    '\b(\d+)X\d+(\.\d+)?(ml|gram|g|kg|ltr|liter|pcs|pack|isi|L)\b', 
        '\1', 
        'gi'
) AS name,
    regexp_replace(name, '.*?(\d+[GgMmLl]+).*', '\1', 'i') AS detail,
    original_price,
	discounted_price,
	discount_percentage,
	platform,
	created_date
FROM 
    products.landing_product_indomart id
    """)
    
    with engine.connect() as conn:
        conn.execute(insert_query)
    print("Table inserted successfully.")
except SQLAlchemyError as e:
    print(f"Error occurred: {e}")
