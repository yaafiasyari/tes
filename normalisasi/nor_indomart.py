import pandas as pd
from sqlalchemy import create_engine
import db_config

# Database configuration
DATABASE_URI = f'postgresql+psycopg2://{db_config.get_user()}:{db_config.get_passwd()}@{db_config.get_host()}:5431/{db_config.get_db()}'
engine = create_engine(DATABASE_URI)

# Load the CSV files
indomart_df = pd.read_csv('D:/Yaafi/Learn/tes/normalisasi/products_klikindomart.csv')
# tokopedia_df = pd.read_csv('products_tokopedia.csv')


indomart_df['original_price'] = indomart_df['original_price'].astype(str)
indomart_df['original_price'] = indomart_df['original_price'].str.replace('Rp', '').str.replace('.', '').fillna('0').astype(int)
indomart_df['discounted_price'] = indomart_df['discounted_price'].apply(lambda x: "{:.3f}".format(x).replace('.', ''))
indomart_df['discount_percentage'] = indomart_df['discount_percentage'].str.rstrip('%').astype(int)



category_mapping = {
    'Kecap & Saus': 'Aneka Sambal',
    'Baby Oil': 'Kids Cologne, Oil, Lotion & Cream',
    'Body Lotion': 'Lotion',
    'Bumbu Instan': 'Bumbu Masak Instan',
    'Bumbu Tradisional': 'Bumbu Masak Instan',
    'Garam & Bumbu': 'Bumbu Masak Instan',
    'Kaldu & Penyedap Rasa': 'Bumbu Masak Instan',
    'Cleanser Wajah': 'Facial Cleanser',
    'Conditioner': 'Kondisioner dan Masker',
    'Deodorant Roll On': 'Deodorant',
    'Deodorant Spray': 'Deodorant',
    'Deterjen': 'Deterjen Laundry',
    'Deterjen Bubuk': 'Deterjen Laundry',
    'Deterjen Cair': 'Deterjen Laundry',
    'Deterjen Matic': 'Deterjen Laundry',
    'Es Krim Stick & Cup': 'Es Krim',
    'Bibir': 'Lip Balm & Oil',
    'Teh Celup': 'Teh',
    'Shampoo Kecantikan': 'Shampoo',
    'Shampoo Perawatan': 'Shampoo',
    'Perlengkapan Bayi': 'Shampoo & Sabun Bayi',
    'Baby Hair & Body Wash': 'Shampoo & Sabun Bayi',
    'Sabun Batang': 'Sabun Mandi',
    'Sabun Cair': 'Sabun Mandi',
    'Sabun Cuci Tangan': 'Sabun Cuci Tangan & Pembersih Tangan',
    'Hand Sanitizer': 'Sabun Cuci Tangan & Pembersih Tangan',
    'Karbol': 'Pembersih Lantai & Toilet',
    'Pembersih Lantai': 'Pembersih Lantai & Toilet',
    'Pembersih Toilet': 'Pembersih Lantai & Toilet',
    'Vitamin & Serum Rambut': 'Perawatan Rambut',
    'Perapi Pakaian': 'Pewangi Pelembut Pakaian',
    'Pelicin & Pewangi Pakaian': 'Pewangi Pelembut Pakaian',
    'Parfum & Cologne Unisex': 'Cologne & Parfum',
    'Cream & Lotion Bayi': 'Baby Cologne, Oil, Lotion & Cream',
    'Parfum & Cologne Anak-Anak': 'Baby Cologne, Oil, Lotion & Cream',
    'Pasta Gigi Sensitif': 'Pasta Gigi',
    'Scrub Wajah': 'Pembersih Wajah',
    'Sunblock wajah': 'Krim Wajah',
    'Krim': 'Krim Wajah',
    'Wajah': 'Krim Wajah',
    'Kids Hair & Body Wash': 'Perlengkapan Anak'
}

indomart_df['category'] = indomart_df['category'].map(category_mapping).fillna(indomart_df['category'])

print(indomart_df)

try:
    indomart_df.to_sql('landing_product_indomart', engine, index=False, if_exists='append', schema='products')
    print("Data saved to PostgreSQL successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

