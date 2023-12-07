import os
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
import re

def parse_sitemap(sitemap_path):
    # Initialize an empty list to store URLs
    url_list = []
    try:
        # Parse the XML file using ElementTree
        tree = ET.parse(sitemap_path)
        root = tree.getroot()

        # Define the XML namespace (if any) used in the sitemap
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # Find all URL elements in the sitemap
        url_elements = root.findall('.//ns:url/ns:loc', namespaces=ns)

        # Extract URLs and add them to the list
        url_list = [url_element.text for url_element in url_elements]

    except ET.ParseError as e:
        print(f"Error parsing the sitemap file: {e}")

    return url_list

def fetch_html_content(url):
    # Fetch the website content using requests
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad requests
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return None

def clean_html_and_extract_text(html_text):
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_text, 'html.parser')

    # Extract text content
    text_content = soup.get_text('\n', strip=True)
    result = text_content.split('\n')
    result = [x for x in result if x != '']
    #print(result)
    cleaned_text="\n".join(result)
    # Normalize the text (standardise format-convert to lowercase)
    #cleaned_text = cleaned_text.lower()
    return cleaned_text

def save_to_file(content, folder_path, filename):
    invalid_chars = ['?', ':', '<', '>', '|', '"', '*', '\\', '/']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    try:
        # Create directory and intermediate directories if they don't exist
        os.makedirs(folder_path, exist_ok=True)

        filepath = os.path.join(folder_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Error saving content to file: {e}")

def crawl_url(url, folder_path):
    # Fetch the website content
    html_content = fetch_html_content(url)

    if html_content is not None:
        # Clean the HTML content and extract text
        extracted_text = clean_html_and_extract_text(html_content)

        # Generate filename based on the crawled URL (replace special characters with underscores)
        filename = url.replace('://', '_').replace('/', '_').replace('.', '_').replace(':','_').replace('&','_').replace('=',"_")
        #filename = re.sub(r'[^a-zA-Z0-9_]', '_', url)
        # Store the HTML content and extracted text in separate files within the folder
        save_to_file(html_content,'C:/Users/varshitha/acuration-demos/k_varshitha/crawled_content/url', f"{filename}_html.html")
        save_to_file(extracted_text,'C:/Users/varshitha/acuration-demos/k_varshitha/crawled_content/extracted', f"{filename}_extracted_text.txt")
    else:
        # Generate filename based on the crawled URL (replace special characters with underscores)
        filename = url.replace('://', '_').replace('/', '_').replace('.', '_').replace(':','_').replace('&','_').replace('=',"_")
        response=requests.get(url)
        save_to_file(response.text,'C:/Users/varshitha/acuration-demos/k_varshitha/crawled_content/error404', f"{filename}_html.html")
def main():
    # Specify the path to the sitemap.xml file
    sitemap_path = 'C:/Users/varshitha/Downloads/sofarocean_sitemap.xml'

    # Specify the folder where you want to store the crawled content
    output_folder = 'C:/Users/varshitha/acuration-demos/k_varshitha/crawled_content/'

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Parse the sitemap to get a list of URLs
    urls_to_crawl = parse_sitemap(sitemap_path)
    print(len(urls_to_crawl))
    print(len(set(urls_to_crawl)))
    # Iterate through each URL and crawl the content
    for url in urls_to_crawl:
        crawl_url(url, output_folder)

if __name__ == "__main__":
    main()
