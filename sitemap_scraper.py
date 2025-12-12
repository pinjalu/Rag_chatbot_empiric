import os
import time
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_sitemap_urls(sitemap_url: str) -> list:
    """
    Fetch and parse the sitemap XML to extract all <loc> URL entries.
    """
    response = requests.get(sitemap_url)
    response.raise_for_status()
    # Parse XML and find all <loc> elements under the sitemap namespace
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    root = ET.fromstring(response.content)
    urls = [elem.text for elem in root.findall(".//sm:loc", ns)]
    return urls


def init_driver() -> webdriver.Chrome:
    """
    Initialize a headless Chrome WebDriver.
    Ensure chromedriver is in your PATH or specify executable_path.
    """
    options = Options()
    options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    return driver


def sanitize_filename(url: str) -> str:
    """
    Create a safe filename from a URL path.
    Replaces slashes and unsafe chars with underscores.
    """
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    name = path.replace('/', '_') if path else 'home'
    safe = ''.join(c if c.isalnum() or c in '._-' else '_' for c in name)
    return f"{safe}.txt"


def extract_content(driver: webdriver.Chrome, url: str) -> str:
    """
    Load the page, handle dynamic tabs or sections, and extract plain text in top-to-bottom order.
    """
    driver.get(url)
    # Wait for the body element to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # Click through any tab-like elements to reveal hidden content
    tab_selectors = "[data-toggle='tab'], [role='tab']"
    tabs = driver.find_elements(By.CSS_SELECTOR, tab_selectors)
    for tab in tabs:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", tab)
            tab.click()
            time.sleep(1)
        except Exception:
            continue

    # Parse the final page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    meta_title = soup.title.string.strip() if soup.title else ''
    meta_desc = ''
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    if desc_tag and desc_tag.get('content'):
        meta_desc = desc_tag['content'].strip()

    header_block = f"{meta_title}\n\n{meta_desc}\n\n" if meta_title or meta_desc else ''


    # Extract all text nodes with blank lines between blocks
    raw_text = soup.body.get_text(separator='\n\n', strip=True)
    
    # Append all meaningful anchor text + hrefs
    links = []
    for a in soup.find_all('a', href=True):
        link_text = a.get_text(strip=True)
        # No text in anchor, try alt attribute from <img>
        if not link_text:
            img = a.find('img', alt=True)
            if img and img['alt'].strip():
                link_text = img['alt'].strip()

        href = a['href'].strip()

        # Final output:
        if link_text and href:
            links.append(f"[{link_text}]({href})")        

    if links:
        raw_text += "\n\n---\n\nLinks:\n" + '\n'.join(links)

    # Return the full text (blank lines now intact for section breaks)
    return header_block + raw_text


def save_text(content: str, filename: str, output_dir: str = 'final_output') -> None:
    """
    Save extracted content to a text file under the final_output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def main() -> None:
    """
    Main routine to:
    1. Fetch all URLs from the sitemap
    2. Initialize Selenium WebDriver
    3. Iterate through each URL, extract content, and save to file
user_asked_query = "tell me about the company"
    """
    sitemap_url = 'https://empiricinfotech.com/sitemap.xml'
    urls = get_sitemap_urls(sitemap_url)

    driver = init_driver()
    try:
        for url in urls:
            try:
                print(f"Processing: {url}")
                content = extract_content(driver, url)
                filename = sanitize_filename(url)
                save_text(content, filename)
                print(f"Saved to: final_output/{filename}\n")
            except Exception as e:
                print(f"Error processing {url}: {e}")
    finally:
        driver.quit()
        print(f"Total urls processed: {len(urls)}")


if __name__ == '__main__':
    main()
