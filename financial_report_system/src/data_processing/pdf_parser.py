"""
Financial report parser for PDF files.
"""
import re
from pathlib import Path
from typing import Dict, Optional
import pdfplumber
import PyPDF2
from src.utils.logger import log


class PDFParser:
    """Parser for PDF financial reports."""
    
    def __init__(self):
        """Initialize PDF parser."""
        self.text_content = ""
        
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract text from PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        log.info(f"Extracting text from PDF: {pdf_path}")
        
        try:
            # Try pdfplumber first
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                self.text_content = text
                return text
        except Exception as e:
            log.warning(f"pdfplumber failed, trying PyPDF2: {e}")
            
            # Fallback to PyPDF2
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() or ""
                    self.text_content = text
                    return text
            except Exception as e2:
                log.error(f"PDF extraction failed: {e2}")
                raise
    
    def extract_tables(self, pdf_path: str) -> list:
        """
        Extract tables from PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of extracted tables
        """
        log.info(f"Extracting tables from PDF: {pdf_path}")
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                all_tables = []
                for page in pdf.pages:
                    tables = page.extract_tables()
                    if tables:
                        all_tables.extend(tables)
                return all_tables
        except Exception as e:
            log.error(f"Table extraction failed: {e}")
            return []
    
    def extract_financial_data(self, pdf_path: str) -> Dict:
        """
        Extract financial data from PDF.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary containing extracted financial data
        """
        text = self.extract_text(pdf_path)
        tables = self.extract_tables(pdf_path)
        
        # Extract key metrics using regex patterns
        financial_data = {
            "file_path": pdf_path,
            "text_content": text,
            "tables": tables,
            "metrics": self._extract_metrics(text)
        }
        
        return financial_data
    
    def _extract_metrics(self, text: str) -> Dict:
        """
        Extract financial metrics from text using pattern matching.
        
        Args:
            text: Text content to search
            
        Returns:
            Dictionary of extracted metrics
        """
        metrics = {}
        
        # Common patterns for financial metrics (Chinese and English)
        patterns = {
            "revenue": [
                r"营业收入[：:]\s*([\d,\.]+)\s*[万亿]?元?",
                r"总收入[：:]\s*([\d,\.]+)\s*[万亿]?元?",
                r"Revenue[：:]\s*([\d,\.]+)",
            ],
            "net_profit": [
                r"净利润[：:]\s*([\d,\.]+)\s*[万亿]?元?",
                r"归属于母公司股东的净利润[：:]\s*([\d,\.]+)\s*[万亿]?元?",
                r"Net Profit[：:]\s*([\d,\.]+)",
            ],
            "total_assets": [
                r"总资产[：:]\s*([\d,\.]+)\s*[万亿]?元?",
                r"Total Assets[：:]\s*([\d,\.]+)",
            ],
            "roe": [
                r"净资产收益率[：:]\s*([\d,\.]+)\s*%?",
                r"ROE[：:]\s*([\d,\.]+)\s*%?",
            ]
        }
        
        for metric, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, text)
                if match:
                    metrics[metric] = match.group(1)
                    break
        
        return metrics
