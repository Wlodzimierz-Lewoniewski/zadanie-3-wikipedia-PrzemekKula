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
            internal_links.append((link.text, 'https://pl.wikipedia.org' + href))
    
    image_urls = []
    for img in soup.select('img')[:3]:
        img_url = 'https:' + img['src']
        image_urls.append(img_url)

    external_links = []
    for link in soup.select('a.external')[:3]:
        external_links.append(link['href'])
    
    categories = []
    for category in soup.select('div#mw-normal-catlinks li a')[:3]:
        categories.append(category.text)
    
    return {
        "internal_links": internal_links,
        "image_urls": image_urls,
        "external_links": external_links,
        "categories": categories
    }

def main():
    category_name = input("Podaj nazwę kategorii na Wikipedii: ").strip()
    category_url = f"https://pl.wikipedia.org/wiki/Kategoria:{category_name.replace(' ', '_')}"
    article_urls = get_first_two_articles_urls(category_url)
    
    for idx, article_url in enumerate(article_urls):
        print(f"\nInformacje z artykułu {idx + 1}: {article_url}")
        article_info = extract_article_info(article_url)
        
        print("\nPierwsze 5 odnośników wewnętrznych (nazwa i URL):")
        for link_text, link_url in article_info["internal_links"]:
            print(f"- {link_text}: {link_url}")
        
        print("\nPierwsze 3 adresy URL obrazków:")
        for url in article_info["image_urls"]:
            print(f"- {url}")
        
        print("\nPierwsze 3 zewnętrzne linki źródłowe:")
        for url in article_info["external_links"]:
            print(f"- {url}")
        
        print("\nPierwsze 3 kategorie:")
        for category in article_info["categories"]:
            print(f"- {category}")

main()