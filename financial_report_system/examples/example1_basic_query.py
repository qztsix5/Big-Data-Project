"""
Example 1: Basic Query - Simple financial data queries.

This example demonstrates:
1. Loading sample financial data
2. Basic queries about revenue, profit, etc.
3. Single-turn interactions
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import FinancialReportSystem


def run_basic_queries():
    """Run basic query examples."""
    print("=" * 60)
    print("Example 1: Basic Financial Data Queries")
    print("=" * 60)
    print()
    
    # Initialize system
    system = FinancialReportSystem()
    
    # Load sample data
    sample_data = {
        "阿里巴巴": {
            "2023": {
                "revenue": "868,687百万元",
                "net_profit": "71,337百万元",
                "total_assets": "1,594,023百万元",
                "roe": "8.5%",
                "gross_margin": "37.2%"
            },
            "2024": {
                "revenue": "941,168百万元",
                "net_profit": "80,234百万元",
                "total_assets": "1,687,456百万元",
                "roe": "9.1%",
                "gross_margin": "38.5%"
            }
        }
    }
    
    system.agent.load_financial_data(sample_data)
    
    # Example queries
    queries = [
        "阿里巴巴2024年的营业收入是多少？",
        "阿里巴巴2024年的净利润是多少？",
        "阿里巴巴2024年的ROE是多少？",
    ]
    
    print("Sample Queries:")
    print("-" * 60)
    
    for i, query in enumerate(queries, 1):
        print(f"\nQuery {i}: {query}")
        print("Response:")
        
        # Since we're using a mock setup without actual LLM
        # We'll simulate the response based on the data
        if "2024" in query and "营业收入" in query:
            response = f"根据财务数据，阿里巴巴2024年的营业收入为941,168百万元。"
        elif "2024" in query and "净利润" in query:
            response = f"根据财务数据，阿里巴巴2024年的净利润为80,234百万元。"
        elif "2024" in query and "ROE" in query:
            response = f"根据财务数据，阿里巴巴2024年的ROE（净资产收益率）为9.1%。"
        else:
            response = "需要更多信息来回答这个问题。"
        
        print(response)
        print("-" * 60)
    
    # Save statistics
    system.save_statistics("logs/example1_stats.json")
    print("\n✓ Statistics saved to logs/example1_stats.json")
    
    print("\n" + "=" * 60)
    print("Example 1 completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_basic_queries()
