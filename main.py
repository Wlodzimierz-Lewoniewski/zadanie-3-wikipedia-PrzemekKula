import re
import requests
import itertools

article_pattern = r'<li[^>]*>.*<a[^>]*href=\"(/wiki/(?![^"]*:)[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>.*</li>'
internal_link_pattern = r'<a[^>]*href=\"(/wiki/(?![^"]*:)[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>'
image_pattern = r'<img[^>]*src=\"(//upload\.wikimedia\.org/[^"]+)\"[^>]*/>'
external_link_pattern = r'<a[^>]*class=\"external[^"]*\"[^>]*href=\"([^"]+)\"[^>]*>'
category_pattern = r'<a[^>]*href=\"(/wiki/Kategoria:[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>'

def join_results(items):
    print(' | '.join(items))

def main_content(html_code: str) -> str:
    return html_code[html_code.find('<div id="mw-content-text"'):html_code.find('<div id="catlinks"')]

def extract_references(html_code: str) -> str:
    references_part = html_code[html_code.find('id="Przypisy"'):]
    return references_part[:references_part.find('<div class="mw-heading')]

def extract_categories_section(html_code: str) -> str:
    return html_code[html_code.find('<div id="catlinks"'):]

def pattern_search(pattern: str, content: str, flags: int = 0, max_matches: int = 5) -> list:
    return [match.groups() for match in itertools.islice(re.finditer(pattern, content, flags=flags), max_matches)]

def generate_category_url(category_name: str) -> str:
    formatted_category = category_name.replace(' ', '_')
    return f'https://pl.wikipedia.org/wiki/Kategoria:{formatted_category}'

def fetch_category_articles(category_name: str, max_results: int = 3) -> list[tuple[str, str]]:
    category_page_url = generate_category_url(category_name)
    response = requests.get(category_page_url)
    page_content = response.text
    return pattern_search(article_pattern, page_content, max_matches=max_results)

def fetch_article_html(article_path: str) -> str:
    article_url = "https://pl.wikipedia.org" + article_path
    return requests.get(article_url).text

def find_internal_links(html_content: str, max_results: int = 5) -> list[tuple[str, str]]:
    main_section = main_content(html_content)
    return pattern_search(internal_link_pattern, main_section, max_matches=max_results)

def find_images(html_content: str, max_results: int = 3) -> list:
    main_section = main_content(html_content)
    return pattern_search(image_pattern, main_section, max_matches=max_results)

def find_external_links(html_content: str, max_results: int = 3) -> list:
    references_section = extract_references(html_content)
    return pattern_search(external_link_pattern, references_section, max_matches=max_results)

def find_article_categories(html_content: str, max_results: int = 3) -> list:
    categories_section = extract_categories_section(html_content)
    return pattern_search(category_pattern, categories_section, max_matches=max_results)

def main():
    category_input = input("Enter the category name: ").strip()
    articles = fetch_category_articles(category_input)
    for path in articles:
        article_html_content = fetch_article_html(path[0])
        
        internal_links = find_internal_links(article_html_content)
        join_results([link_title for _, link_title in internal_links])
        
        image_links = find_images(article_html_content)
        join_results([img_url for img_url, in image_links])
        
        external_links = find_external_links(article_html_content)
        join_results([ext_url for ext_url, in external_links])
        
        categories = find_article_categories(article_html_content)
        join_results([cat_name.replace('Kategoria:', '') for _, cat_name in categories])
    
if __name__ == '__main__':
    main()