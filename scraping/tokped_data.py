import requests
from bs4 import BeautifulSoup
import tokpedlink 
import pandas as pd


def scrape_tokopedia():
    all_product_details = []

    for url in tokpedlink.links:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            continue  
        
        soup = BeautifulSoup(response.content, 'html.parser')
        product_details = {}

        try:
            name_tag = soup.find('h2', class_='css-1wykgi9-unf-heading e1qvo2ff2')
            name = name_tag.text.strip() if name_tag else 'N/A'

            category_tag = soup.find_all('a', class_='css-1y6qqnj-unf-heading e1qvo2ff7')
            category = category_tag[-1].text.strip() if category_tag else 'N/A'

            discounted_price_tag = soup.find('div', {'data-testid': 'lblPDPDetailProductPrice'})
            discounted_price = discounted_price_tag.text.strip() if discounted_price_tag else 'N/A'

            original_price_tag = soup.find('span', {'data-testid': 'lblPDPDetailOriginalPrice'})
            original_price = original_price_tag.text.strip() if original_price_tag else discounted_price

            discount_percentage_tag = soup.find('span', {'data-testid': 'lblPDPDetailDiscountPercentage'})
            discount_percentage = discount_percentage_tag.text.strip() if discount_percentage_tag else 'N/A'

            discounted_price_tag = soup.find('div', {'data-testid': 'lblPDPDetailProductPrice'})
            discounted_price = discounted_price_tag.text.strip() if discounted_price_tag else '0%'

            product_details = {
                'name': name,
                'category': category,
                'original_price': original_price,
                'discounted_price': discounted_price,
                'discount_percentage': discount_percentage,
                'platform': 'www.tokopedia.com'
            }

        except AttributeError as e:
            print(f"Error extracting product details: {e}")
            continue  

        all_product_details.append(product_details)

    return all_product_details

def save_to_csv(products, file_path):
    df = pd.DataFrame(products)
    df.to_csv(file_path, index=False)

file_path = 'D:/Yaafi/Learn/tes/normalisasi/products_tokopedia.csv'

products = scrape_tokopedia()
save_to_csv(products, file_path)
print("Data saved to CSV successfully")
