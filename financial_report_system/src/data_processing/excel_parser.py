"""
Financial report parser for Excel files.
"""
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
from src.utils.logger import log


class ExcelParser:
    """Parser for Excel financial reports."""
    
    def __init__(self):
        """Initialize Excel parser."""
        self.dataframes = {}
        
    def load_excel(self, excel_path: str) -> Dict[str, pd.DataFrame]:
        """
        Load Excel file and return all sheets as DataFrames.
        
        Args:
            excel_path: Path to Excel file
            
        Returns:
            Dictionary of sheet names to DataFrames
        """
        log.info(f"Loading Excel file: {excel_path}")
        
        try:
            # Read all sheets
            excel_file = pd.ExcelFile(excel_path)
            self.dataframes = {
                sheet_name: excel_file.parse(sheet_name)
                for sheet_name in excel_file.sheet_names
            }
            
            log.info(f"Loaded {len(self.dataframes)} sheets from Excel")
            return self.dataframes
        except Exception as e:
            log.error(f"Failed to load Excel file: {e}")
            raise
    
    def extract_financial_data(self, excel_path: str) -> Dict:
        """
        Extract financial data from Excel file.
        
        Args:
            excel_path: Path to Excel file
            
        Returns:
            Dictionary containing extracted financial data
        """
        dfs = self.load_excel(excel_path)
        
        financial_data = {
            "file_path": excel_path,
            "sheets": list(dfs.keys()),
            "data": {},
            "metrics": {}
        }
        
        # Convert DataFrames to dictionaries
        for sheet_name, df in dfs.items():
            financial_data["data"][sheet_name] = df.to_dict(orient='records')
            
            # Try to extract metrics from each sheet
            metrics = self._extract_metrics_from_df(df)
            if metrics:
                financial_data["metrics"][sheet_name] = metrics
        
        return financial_data
    
    def _extract_metrics_from_df(self, df: pd.DataFrame) -> Dict:
        """
        Extract financial metrics from DataFrame.
        
        Args:
            df: DataFrame to extract from
            
        Returns:
            Dictionary of extracted metrics
        """
        metrics = {}
        
        # Common metric names (Chinese and English)
        metric_keywords = {
            "revenue": ["营业收入", "总收入", "Revenue", "Total Revenue"],
            "net_profit": ["净利润", "Net Profit", "归属于母公司股东的净利润"],
            "total_assets": ["总资产", "Total Assets", "资产总计"],
            "total_liabilities": ["总负债", "Total Liabilities", "负债总计"],
            "gross_margin": ["毛利率", "Gross Margin"],
            "roe": ["净资产收益率", "ROE", "Return on Equity"],
        }
        
        # Search for metrics in the DataFrame
        for metric, keywords in metric_keywords.items():
            for keyword in keywords:
                # Search in first column (usually contains labels)
                if df.shape[1] > 0:
                    for idx, row in df.iterrows():
                        if any(keyword in str(cell) for cell in row):
                            # Try to get the value from adjacent columns
                            for col_idx in range(1, min(df.shape[1], 5)):
                                value = row.iloc[col_idx] if col_idx < len(row) else None
                                if pd.notna(value) and value != '':
                                    metrics[metric] = value
                                    break
                            if metric in metrics:
                                break
                if metric in metrics:
                    break
        
        return metrics
    
    def get_sheet_data(self, sheet_name: str) -> Optional[pd.DataFrame]:
        """
        Get DataFrame for a specific sheet.
        
        Args:
            sheet_name: Name of the sheet
            
        Returns:
            DataFrame or None if not found
        """
        return self.dataframes.get(sheet_name)
