from typing import Dict, List, Any, Optional
from .base import BaseAgent
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin, urlparse
from datetime import datetime
import hashlib
from time import sleep

class WebScraperAgent(BaseAgent):
    """Agent for scraping web content from various sources"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("WebScraperAgent")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def collect(self, urls: List[str], depth: int = 1, max_pages: int = 100) -> Dict[str, List[Dict]]:
        """Collect data from specified websites"""
        data = {}
        
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent=self.headers['User-Agent']
            )
            
            for base_url in urls:
                try:
                    self.logger.info(f"Starting scrape of {base_url}")
                    domain = urlparse(base_url).netloc
                    visited = set()
                    queue = [(base_url, 0)]  # (url, current_depth)
                    data[domain] = []
                    
                    while queue and len(visited) < max_pages:
                        url, current_depth = queue.pop(0)
                        if url in visited or current_depth > depth:
                            continue
                            
                        page_data = self._scrape_page(context, url)
                        if page_data:
                            data[domain].append(page_data)
                            visited.add(url)
                            
                        if current_depth < depth:
                            new_urls = self._extract_links(page_data.get("html", ""), base_url)
                            queue.extend((url, current_depth + 1) for url in new_urls 
                                      if url not in visited)
                            
                        sleep(1)  # Be polite
                        
                    self.logger.info(f"Completed scraping {domain}: {len(data[domain])} pages")
                except Exception as e:
                    self.logger.error(f"Error scraping {base_url}: {str(e)}")
                    
            browser.close()
            
        return data
    
    def _scrape_page(self, context, url: str) -> Optional[Dict]:
        """Scrape a single page using Playwright"""
        try:
            page = context.new_page()
            page.goto(url, wait_until="networkidle")
            
            # Get the rendered HTML
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract key information
            title = soup.title.string if soup.title else ""
            meta_description = (
                soup.find("meta", {"name": "description"})["content"]
                if soup.find("meta", {"name": "description"})
                else ""
            )
            
            # Extract main content
            for element in soup(["script", "style", "nav", "header", "footer"]):
                element.decompose()
                
            main_content = " ".join(soup.stripped_strings)
            
            page_data = {
                "url": url,
                "title": title,
                "meta_description": meta_description,
                "content": main_content,
                "html": html,
                "scrape_date": datetime.now().isoformat(),
                "content_hash": hashlib.md5(main_content.encode()).hexdigest()
            }
            
            page.close()
            return page_data
            
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {str(e)}")
            return None
    
    def _extract_links(self, html: str, base_url: str) -> List[str]:
        """Extract links from HTML content"""
        soup = BeautifulSoup(html, 'html.parser')
        domain = urlparse(base_url).netloc
        links = set()
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(base_url, href)
            
            # Only include links from the same domain
            if urlparse(full_url).netloc == domain:
                links.add(full_url)
                
        return list(links)
    
    def process(self, data: Dict[str, List[Dict]], *args, **kwargs) -> Dict[str, Any]:
        """Process collected web data"""
        processed_data = {
            "metadata": {
                "collection_date": datetime.now().isoformat(),
                "websites": list(data.keys()),
                "total_pages": sum(len(pages) for pages in data.values())
            },
            "data": data
        }
        return processed_data
