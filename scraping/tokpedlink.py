import requests
from bs4 import BeautifulSoup

def scrape_tokopedia_unilever(page_limit=70):
    base_url = "https://www.tokopedia.com/unilever/product/page/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    links = []

    for page in range(1, page_limit + 1):
        url = f"{base_url}{page}"
        print(f"Scraping URL: {url}")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print(f"Successfully retrieved page {page}")
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, 'html.parser')

            items = soup.select('.css-19oqosi')
            print(f"Found {len(items)} product on page {page}")
            
            for item in items:
                link_tag = item.select_one('a')
                if link_tag:
                    link = link_tag['href']
                    links.append(link)
                    # print(f"Found link: {link}")

        else:
            print(f"Failed to retrieve content on page {page}. Status code: {response.status_code}")
            break

    print(f"Total links : {len(links)}")
    return links

links = scrape_tokopedia_unilever(page_limit=70)
# print(links)
