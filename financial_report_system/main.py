"""
Main application for Financial Report Analysis System.
"""
import sys
from pathlib import Path
from typing import Dict, List
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data_processing.pdf_parser import PDFParser
from src.data_processing.excel_parser import ExcelParser
from src.data_processing.web_scraper import WebScraper
from src.data_processing.data_storage import DataStorage
from src.visualization.chart_generator import ChartGenerator
from src.agents.financial_agent import FinancialAnalysisAgent
from src.utils.config_loader import config
from src.utils.logger import log
from src.utils.stats_tracker import stats_tracker


class FinancialReportSystem:
    """Main system for financial report analysis."""
    
    def __init__(self):
        """Initialize the financial report system."""
        log.info("Initializing Financial Report Analysis System")
        
        # Initialize components
        self.pdf_parser = PDFParser()
        self.excel_parser = ExcelParser()
        self.web_scraper = WebScraper()
        self.data_storage = DataStorage(storage_type="excel")
        self.chart_generator = ChartGenerator()
        self.agent = FinancialAnalysisAgent(
            data_storage=self.data_storage,
            chart_generator=self.chart_generator
        )
        
        self.processed_data = {}
        
    def import_report(self, file_path: str, company_name: str = None, year: int = None) -> Dict:
        """
        Import a financial report from file.
        
        Args:
            file_path: Path to the report file
            company_name: Name of the company
            year: Report year
            
        Returns:
            Processed financial data
        """
        log.info(f"Importing report from: {file_path}")
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            log.error(f"File not found: {file_path}")
            return {}
        
        # Parse based on file type
        if file_path.suffix.lower() == '.pdf':
            data = self.pdf_parser.extract_financial_data(str(file_path))
        elif file_path.suffix.lower() in ['.xlsx', '.xls']:
            data = self.excel_parser.extract_financial_data(str(file_path))
        else:
            log.error(f"Unsupported file type: {file_path.suffix}")
            return {}
        
        # Add metadata
        if company_name:
            data['company_name'] = company_name
        if year:
            data['year'] = year
        
        # Store data
        self._store_processed_data(data, company_name, year)
        
        log.info(f"Successfully imported report for {company_name} ({year})")
        return data
    
    def import_from_web(self, company_name: str, years: List[int] = None):
        """
        Import financial reports from web (auto-scraping).
        
        Args:
            company_name: Name of the company
            years: List of years to fetch
        """
        log.info(f"Auto-scraping reports for {company_name}")
        
        # This would use the web scraper to fetch reports
        # For now, it's a placeholder
        reports = self.web_scraper.search_company_reports(company_name)
        
        log.info(f"Found {len(reports)} reports for {company_name}")
        return reports
    
    def _store_processed_data(self, data: Dict, company_name: str, year: int):
        """Store processed data internally."""
        if company_name not in self.processed_data:
            self.processed_data[company_name] = {}
        
        if year:
            self.processed_data[company_name][str(year)] = data.get('metrics', {})
        
        # Load into agent
        self.agent.load_financial_data(self.processed_data)
    
    def query(self, question: str, context: Dict = None) -> str:
        """
        Query the financial data using natural language.
        
        Args:
            question: Natural language question
            context: Additional context
            
        Returns:
            Answer from the agent
        """
        return self.agent.chat(question, context)
    
    def multi_turn_query(self, questions: List[str]) -> List[Dict]:
        """
        Perform multi-turn conversation.
        
        Args:
            questions: List of questions
            
        Returns:
            Conversation history
        """
        return self.agent.multi_turn_conversation(questions)
    
    def generate_chart(self, chart_type: str, data: pd.DataFrame, **kwargs) -> str:
        """
        Generate a visualization chart.
        
        Args:
            chart_type: Type of chart (line, bar, etc.)
            data: Data to visualize
            **kwargs: Additional parameters for chart
            
        Returns:
            Path to generated chart
        """
        log.info(f"Generating {chart_type} chart")
        
        if chart_type == "line":
            return self.chart_generator.create_line_chart(data, **kwargs)
        elif chart_type == "bar":
            return self.chart_generator.create_bar_chart(data, **kwargs)
        elif chart_type == "trend":
            return self.chart_generator.create_trend_chart(data, **kwargs)
        
        return ""
    
    def export_data(self, output_path: str, format: str = "excel"):
        """
        Export processed data to file.
        
        Args:
            output_path: Path to save the data
            format: Export format (excel or sql)
        """
        log.info(f"Exporting data to {output_path}")
        
        # Convert processed data to DataFrame
        all_data = []
        for company, years in self.processed_data.items():
            for year, metrics in years.items():
                row = {"company": company, "year": year}
                row.update(metrics)
                all_data.append(row)
        
        if all_data:
            if format == "excel":
                self.data_storage.save_to_excel(all_data, output_path)
            elif format == "sql":
                for row in all_data:
                    self.data_storage.save_to_sql(row)
    
    def get_statistics(self) -> Dict:
        """Get usage statistics."""
        return stats_tracker.get_summary()
    
    def save_statistics(self, filepath: str = "logs/statistics.json"):
        """Save statistics to file."""
        stats_tracker.save_stats(filepath)


def main():
    """Main entry point for demonstration."""
    print("=" * 60)
    print("Financial Report Analysis System")
    print("基于 AutoGen 的智能财报分析系统")
    print("=" * 60)
    print()
    
    # Initialize system
    system = FinancialReportSystem()
    
    print("System initialized successfully!")
    print("\nFeatures:")
    print("1. Import financial reports (PDF/Excel/Web)")
    print("2. Natural language query interface")
    print("3. Multi-turn interactive analysis")
    print("4. Automatic chart generation")
    print("5. Industry comparison and advanced analysis")
    print("\nFor usage examples, see examples/ directory")
    print()
    
    return system


if __name__ == "__main__":
    system = main()
