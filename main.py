import requests
from bs4 import BeautifulSoup
import re

def get_first_two_articles_urls(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.select('div.mw-category a')
    article_urls = ['https://pl.wikipedia.org' + link['href'] for link in links[:2]]
    return article_urls

def extract_article_info(article_url):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    internal_links = []
    for link in soup.select('a[href^="/wiki/"]')[:5]:
        href = link['href']
        if not re.search(r':', href):
            internal_links.append(link.text)
    
    image_urls = []
    for img in soup.select('img')[:3]:
        img_url = img['src']
        image_urls.append(img_url)

    external_links = []
    for link in soup.select('a.external')[:3]:
        external_links.append(link['href'])
    
    categories = []
    for category in soup.select('div#mw-normal-catlinks li a')[:3]:
        categories.append(category.text)
    
    return {
        "internal_links": " | ".join(internal_links),
        "image_urls": " | ".join(image_urls),
        "external_links": " | ".join(external_links),
        "categories": " | ".join(categories)
    }

def main():
    category_name = input("Podaj nazwę kategorii na Wikipedii: ").strip()
    category_url = f"https://pl.wikipedia.org/wiki/Kategoria:{category_name.replace(' ', '_')}"
    article_urls = get_first_two_articles_urls(category_url)
    
    for article_url in article_urls:
        article_info = extract_article_info(article_url)
        
        print(article_info["internal_links"])
        print(article_info["image_urls"])
        print(article_info["external_links"])
        print(article_info["categories"])

main()
