import requests
from bs4 import BeautifulSoup
import pandas as pd
import klikindomart_link2


def scrape_klikindomart():
    all_product_details = []
    # links = [
    #     'https://www.klikindomaret.com/product/baby-bath-hair--body-2',
    #     'https://www.klikindomaret.com/product/baby-bath-hair--body-1'
    # ]
    
    for url in klikindomart_link2.links:
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            products = []
            
            for item in soup.select('.section-title.each-content.bg-white'):
                name_tag = item.select_one('.product-title')
                discounted_price_tag = item.select_one('.price .normal.price-final')
                original_price_tag = item.select_one('.strikeout.disc-price')
                discount_tag = item.select_one('.price .discount')
                category_tag = soup.select('.breadcrumb a')
                
                if name_tag and discounted_price_tag and category_tag:
                    name = name_tag.text.strip()
                    discounted_price = discounted_price_tag.text.strip()
                    original_price = original_price_tag.text.strip() if original_price_tag else discounted_price
                    discount_percentage = discount_tag.text.strip() if discount_tag else '0%'
                    category = category_tag[-1].text.strip() if category_tag else None
                    
                    products.append({
                        'name': name,
                        'category': category,
                        'original_price': original_price,
                        'discounted_price': discounted_price,
                        'discount_percentage': discount_percentage,
                        'platform': 'www.klikindomaret.com'
                    })
            
            all_product_details.extend(products)
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
    
    return all_product_details

def save_to_csv(products, file_path):
    df = pd.DataFrame(products)
    df.to_csv(file_path, index=False)

file_path = 'D:/Yaafi/Learn/tes/normalisasi/products_klikindomart.csv'

products = scrape_klikindomart()
save_to_csv(products, file_path)
print("Data saved to CSV successfully")