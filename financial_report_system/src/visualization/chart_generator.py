"""
Chart generator for financial data visualization.
"""
from pathlib import Path
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import seaborn as sns
import pandas as pd
from src.utils.logger import log

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # Support Chinese
plt.rcParams['axes.unicode_minus'] = False


class ChartGenerator:
    """Generator for financial data charts."""
    
    def __init__(self, save_path: str = "data/charts/", dpi: int = 300, figsize: tuple = (12, 6)):
        """
        Initialize chart generator.
        
        Args:
            save_path: Directory to save charts
            dpi: Resolution of saved charts
            figsize: Figure size (width, height)
        """
        self.save_path = Path(save_path)
        self.save_path.mkdir(parents=True, exist_ok=True)
        self.dpi = dpi
        self.figsize = figsize
    
    def create_line_chart(self, data: pd.DataFrame, x_col: str, y_col: str, 
                         title: str = "", xlabel: str = "", ylabel: str = "",
                         filename: str = None) -> str:
        """
        Create a line chart.
        
        Args:
            data: DataFrame containing the data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            filename: Filename to save chart
            
        Returns:
            Path to saved chart
        """
        log.info(f"Creating line chart: {title}")
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        ax.plot(data[x_col], data[y_col], marker='o', linewidth=2, markersize=8)
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel(xlabel or x_col, fontsize=12)
        ax.set_ylabel(ylabel or y_col, fontsize=12)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if filename is None:
            filename = f"line_chart_{title.replace(' ', '_')}.png"
        
        filepath = self.save_path / filename
        plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        log.info(f"Chart saved: {filepath}")
        return str(filepath)
    
    def create_bar_chart(self, data: pd.DataFrame, x_col: str, y_cols: List[str],
                        title: str = "", xlabel: str = "", ylabel: str = "",
                        filename: str = None) -> str:
        """
        Create a bar chart (supports multiple series).
        
        Args:
            data: DataFrame containing the data
            x_col: Column name for x-axis
            y_cols: List of column names for y-axis
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            filename: Filename to save chart
            
        Returns:
            Path to saved chart
        """
        log.info(f"Creating bar chart: {title}")
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        if len(y_cols) == 1:
            ax.bar(data[x_col], data[y_cols[0]], alpha=0.8)
        else:
            x = range(len(data))
            width = 0.8 / len(y_cols)
            
            for i, col in enumerate(y_cols):
                offset = (i - len(y_cols)/2) * width + width/2
                ax.bar([xi + offset for xi in x], data[col], width=width, 
                      label=col, alpha=0.8)
            
            ax.set_xticks(x)
            ax.set_xticklabels(data[x_col])
            ax.legend()
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel(xlabel or x_col, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if filename is None:
            filename = f"bar_chart_{title.replace(' ', '_')}.png"
        
        filepath = self.save_path / filename
        plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        log.info(f"Chart saved: {filepath}")
        return str(filepath)
    
    def create_trend_chart(self, data: Dict[str, List], title: str = "",
                          xlabel: str = "Year", ylabel: str = "Value",
                          filename: str = None) -> str:
        """
        Create a trend chart from dictionary data.
        
        Args:
            data: Dictionary with years as keys and values as lists
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            filename: Filename to save chart
            
        Returns:
            Path to saved chart
        """
        df = pd.DataFrame(data)
        
        if len(df.columns) > 1:
            x_col = df.columns[0]
            y_cols = df.columns[1:].tolist()
            
            fig, ax = plt.subplots(figsize=self.figsize)
            
            for col in y_cols:
                ax.plot(df[x_col], df[col], marker='o', linewidth=2, 
                       markersize=8, label=col)
            
            ax.legend()
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel(xlabel, fontsize=12)
            ax.set_ylabel(ylabel, fontsize=12)
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            if filename is None:
                filename = f"trend_chart_{title.replace(' ', '_')}.png"
            
            filepath = self.save_path / filename
            plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
            plt.close()
            
            log.info(f"Chart saved: {filepath}")
            return str(filepath)
        
        return ""
    
    def create_comparison_chart(self, data: pd.DataFrame, metric: str,
                               companies: List[str], title: str = "",
                               filename: str = None) -> str:
        """
        Create a comparison chart for multiple companies.
        
        Args:
            data: DataFrame with company data
            metric: Metric to compare
            companies: List of company names
            title: Chart title
            filename: Filename to save chart
            
        Returns:
            Path to saved chart
        """
        log.info(f"Creating comparison chart for {metric}")
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        comparison_data = data[data['company'].isin(companies)]
        
        for company in companies:
            company_data = comparison_data[comparison_data['company'] == company]
            ax.plot(company_data['year'], company_data[metric], 
                   marker='o', linewidth=2, markersize=8, label=company)
        
        ax.legend()
        ax.set_title(title or f"{metric} Comparison", fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel(metric, fontsize=12)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if filename is None:
            filename = f"comparison_{metric}.png"
        
        filepath = self.save_path / filename
        plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        log.info(f"Chart saved: {filepath}")
        return str(filepath)
