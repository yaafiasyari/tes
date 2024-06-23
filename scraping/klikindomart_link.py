import requests
from bs4 import BeautifulSoup

url = "https://www.klikindomaret.com/page/unilever-officialstore"

def extract_urls_from_page(url):
    print(f"Fetching the webpage: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return []

    print("Webpage fetched successfully.")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    a_tags = soup.find_all('div', class_="item-subBanner")

    links = [a.find('a').get('href') for a in a_tags if a.find('a') and a.find('a').get('href')]
    print(f"Total Link {len(links)} ")

    return links

links = extract_urls_from_page(url)
