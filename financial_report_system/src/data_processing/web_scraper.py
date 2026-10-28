"""
Web scraper for financial reports from public platforms.
"""
import time
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from pathlib import Path
from src.utils.logger import log


class WebScraper:
    """Scraper for financial reports from public platforms."""
    
    def __init__(self, timeout: int = 30, retry: int = 3):
        """
        Initialize web scraper.
        
        Args:
            timeout: Request timeout in seconds
            retry: Number of retries for failed requests
        """
        self.timeout = timeout
        self.retry = retry
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_page(self, url: str) -> Optional[str]:
        """
        Scrape content from a web page.
        
        Args:
            url: URL to scrape
            
        Returns:
            HTML content or None if failed
        """
        for attempt in range(self.retry):
            try:
                log.info(f"Scraping URL (attempt {attempt + 1}): {url}")
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                return response.text
            except Exception as e:
                log.warning(f"Scraping failed (attempt {attempt + 1}): {e}")
                if attempt < self.retry - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    log.error(f"All scraping attempts failed for {url}")
                    return None
    
    def parse_financial_data(self, html: str) -> Dict:
        """
        Parse financial data from HTML content.
        
        Args:
            html: HTML content
            
        Returns:
            Dictionary containing parsed financial data
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract tables
        tables = []
        for table in soup.find_all('table'):
            table_data = []
            for row in table.find_all('tr'):
                row_data = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                if row_data:
                    table_data.append(row_data)
            if table_data:
                tables.append(table_data)
        
        # Extract text content
        text_content = soup.get_text(separator='\n', strip=True)
        
        return {
            "tables": tables,
            "text_content": text_content,
            "title": soup.title.string if soup.title else ""
        }
    
    def download_file(self, url: str, save_path: str) -> bool:
        """
        Download a file from URL.
        
        Args:
            url: URL of the file
            save_path: Path to save the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            log.info(f"Downloading file from {url} to {save_path}")
            response = self.session.get(url, timeout=self.timeout, stream=True)
            response.raise_for_status()
            
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            log.info(f"File downloaded successfully: {save_path}")
            return True
        except Exception as e:
            log.error(f"File download failed: {e}")
            return False
    
    def search_company_reports(self, company_name: str, platform: str = "cninfo") -> List[Dict]:
        """
        Search for company financial reports on a platform.
        
        Args:
            company_name: Name of the company
            platform: Platform to search on
            
        Returns:
            List of report information dictionaries
        """
        log.info(f"Searching for {company_name} reports on {platform}")
        
        # This is a placeholder - actual implementation would depend on the platform's API/structure
        # For demonstration, returning a mock structure
        
        reports = []
        
        # Example structure for what would be scraped
        # In a real implementation, this would parse the actual website
        
        return reports
