import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import db_config
import table_product

DATABASE_URI = f'postgresql+psycopg2://{db_config.get_user()}:{db_config.get_passwd()}@{db_config.get_host()}:5431/{db_config.get_db()}'
engine = create_engine(DATABASE_URI)

products = table_product.get_product()

required_columns = ['productmasterid', 'price']
for col in required_columns:
    if col not in products.columns:
        raise ValueError(f"The '{col}' column is missing from the products data.")

print("Products with required columns:")
print(products[required_columns].head())

products['created_date'] = pd.date_range(start='2024-06-01', periods=len(products), freq='D')

products['created_date'] = pd.to_datetime(products['created_date'])
products = products.sort_values('created_date')

print("Counts per productmasterid:")
print(products['productmasterid'].value_counts())

sufficient_data = products['productmasterid'].value_counts() >= 2
sufficient_data_ids = sufficient_data[sufficient_data].index
filtered_products = products[products['productmasterid'].isin(sufficient_data_ids)]

print("Counts per productmasterid after filtering:")
print(filtered_products['productmasterid'].value_counts())

def create_lag_features(df, lag=1):
    for i in range(1, lag + 1):
        df[f'price_lag_{i}'] = df.groupby('productmasterid')['price'].shift(i)
    df = df.dropna()
    return df

data_with_lags = create_lag_features(filtered_products)

print("Data with Lag Features:")
print(data_with_lags.head())

def predict_next_3_days_per_product(model, recent_data, lag=1):
    predictions = []
    last_known_prices = recent_data[-lag:].tolist()
    for _ in range(3):
        next_price = model.predict([last_known_prices[-lag:]])[0]
        predictions.append(next_price)
        last_known_prices.append(next_price)
    return predictions

all_predictions = pd.DataFrame()

for product_id in data_with_lags['productmasterid'].unique():
    product_data = data_with_lags[data_with_lags['productmasterid'] == product_id]
    
    print(f"Product Data for productmasterid {product_id}:")
    print(product_data.head())
    
    X = product_data[[f'price_lag_{i}' for i in range(1, 2)]]
    y = product_data['price']
    
    model = LinearRegression()
    model.fit(X, y)
    
    recent_data = filtered_products[filtered_products['productmasterid'] == product_id]['price'][-1:]
    
    predicted_prices = predict_next_3_days_per_product(model, recent_data)
    
    future_dates = [datetime.now() + timedelta(days=i) for i in range(1, 4)]
    predictions_df = pd.DataFrame({
        'productmasterid': product_id,
        'date': future_dates,
        'predicted_price': predicted_prices
    })
    
    all_predictions = pd.concat([all_predictions, predictions_df], ignore_index=True)

print("Predictions DataFrame:")
print(all_predictions.head())

try:
    all_predictions.to_sql('pricerecommendation', engine, index=False, if_exists='append', schema='products')
    print("Data saved to PostgreSQL successfully.")
except Exception as e:
    print(f"An error occurred: {e}")