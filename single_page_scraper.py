import os
import time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


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
    
    return header_block + raw_text


def save_text(content: str, filename: str, output_dir: str = 'single_page_output') -> None:
    """
    Save extracted content to a text file under the single_page_output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    """
    Extract and save text content from a single web page URL.
    """
    # CHANGE THIS to your desired page
    single_page_url = 'https://empiricinfotech.com/'

    driver = init_driver()
    try:
        print(f"Processing: {single_page_url}")
        content = extract_content(driver, single_page_url)
        filename = sanitize_filename(single_page_url)
        save_text(content, filename)
        print(f"Saved to: single_page_output/{filename}\n")
    except Exception as e:
        print(f"Error processing {single_page_url}: {e}")
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
