"""
Data storage manager for financial report data.
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from src.utils.logger import log

Base = declarative_base()


class FinancialReport(Base):
    """SQLAlchemy model for financial reports."""
    __tablename__ = 'financial_reports'
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String(200))
    year = Column(Integer)
    quarter = Column(Integer, nullable=True)
    revenue = Column(Float, nullable=True)
    net_profit = Column(Float, nullable=True)
    total_assets = Column(Float, nullable=True)
    total_liabilities = Column(Float, nullable=True)
    gross_margin = Column(Float, nullable=True)
    roe = Column(Float, nullable=True)
    operating_cash_flow = Column(Float, nullable=True)
    asset_liability_ratio = Column(Float, nullable=True)
    raw_data = Column(Text, nullable=True)
    source_file = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.now)


class DataStorage:
    """Manager for storing and retrieving financial data."""
    
    def __init__(self, storage_type: str = "excel", db_url: str = None):
        """
        Initialize data storage.
        
        Args:
            storage_type: Type of storage ("excel" or "sql")
            db_url: Database URL for SQL storage
        """
        self.storage_type = storage_type
        self.db_url = db_url or "sqlite:///data/processed/financial_reports.db"
        
        if storage_type == "sql":
            self._init_database()
    
    def _init_database(self):
        """Initialize database connection and create tables."""
        log.info(f"Initializing database: {self.db_url}")
        self.engine = create_engine(self.db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def save_to_excel(self, data: Dict, output_path: str):
        """
        Save financial data to Excel file.
        
        Args:
            data: Financial data dictionary
            output_path: Path to save Excel file
        """
        log.info(f"Saving data to Excel: {output_path}")
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Convert data to DataFrame
        if isinstance(data, dict) and "metrics" in data:
            df = pd.DataFrame([data["metrics"]])
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame([data])
        
        df.to_excel(output_path, index=False)
        log.info(f"Data saved successfully to {output_path}")
    
    def save_to_sql(self, data: Dict):
        """
        Save financial data to SQL database.
        
        Args:
            data: Financial data dictionary
        """
        if self.storage_type != "sql":
            log.warning("Storage type is not SQL, skipping database save")
            return
        
        log.info("Saving data to SQL database")
        
        try:
            metrics = data.get("metrics", {})
            
            report = FinancialReport(
                company_name=data.get("company_name", "Unknown"),
                year=data.get("year"),
                quarter=data.get("quarter"),
                revenue=self._parse_float(metrics.get("revenue")),
                net_profit=self._parse_float(metrics.get("net_profit")),
                total_assets=self._parse_float(metrics.get("total_assets")),
                total_liabilities=self._parse_float(metrics.get("total_liabilities")),
                gross_margin=self._parse_float(metrics.get("gross_margin")),
                roe=self._parse_float(metrics.get("roe")),
                operating_cash_flow=self._parse_float(metrics.get("operating_cash_flow")),
                asset_liability_ratio=self._parse_float(metrics.get("asset_liability_ratio")),
                raw_data=json.dumps(data, ensure_ascii=False),
                source_file=data.get("file_path")
            )
            
            self.session.add(report)
            self.session.commit()
            log.info("Data saved successfully to database")
        except Exception as e:
            log.error(f"Failed to save to database: {e}")
            self.session.rollback()
    
    def load_from_excel(self, excel_path: str) -> pd.DataFrame:
        """
        Load financial data from Excel file.
        
        Args:
            excel_path: Path to Excel file
            
        Returns:
            DataFrame containing the data
        """
        log.info(f"Loading data from Excel: {excel_path}")
        return pd.read_excel(excel_path)
    
    def query_sql(self, company_name: str = None, year: int = None) -> List[FinancialReport]:
        """
        Query financial data from SQL database.
        
        Args:
            company_name: Filter by company name
            year: Filter by year
            
        Returns:
            List of FinancialReport objects
        """
        if self.storage_type != "sql":
            log.warning("Storage type is not SQL")
            return []
        
        query = self.session.query(FinancialReport)
        
        if company_name:
            query = query.filter(FinancialReport.company_name == company_name)
        if year:
            query = query.filter(FinancialReport.year == year)
        
        return query.all()
    
    @staticmethod
    def _parse_float(value) -> Optional[float]:
        """Parse value to float, handling various formats."""
        if value is None:
            return None
        
        try:
            # Remove commas and convert to float
            if isinstance(value, str):
                value = value.replace(',', '').replace('，', '')
            return float(value)
        except (ValueError, TypeError):
            return None
