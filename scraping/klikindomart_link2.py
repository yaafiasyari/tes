import requests
from bs4 import BeautifulSoup
import klikindomart_link  

def scrape_klikindomaret():
    base_url = 'https://www.klikindomaret.com'
    links = []
    
    print("Starting to scrape KlikIndomaret pages.")
    for url in klikindomart_link.links:
        try:
            print(f"Fetching URL: {url}")
            response = requests.get(url)
            response.raise_for_status()
            print(f"Successfully fetched: {url}")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            items = soup.select('.product-collection.list-product.clearfix .item')
            print(f"total {len(items)} page produk")
            
            for item in items:
                link_tag = item.select_one('a')
                if link_tag:
                    link = link_tag['href']
                    full_link = f"{base_url}{link}"
                    links.append(full_link)
        except requests.RequestException as e:
            print(f"Failed to fetch URL {url}. Error: {e}")

    print(f" Total Extracted {len(links)} links")
    return links

links = scrape_klikindomaret()