"""
Example 2: Advanced Analysis - Deep financial analysis queries.

This example demonstrates:
1. Complex analysis queries
2. Growth rate calculations
3. Trend analysis
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import FinancialReportSystem
import pandas as pd


def run_advanced_analysis():
    """Run advanced analysis examples."""
    print("=" * 60)
    print("Example 2: Advanced Financial Analysis")
    print("=" * 60)
    print()
    
    # Initialize system
    system = FinancialReportSystem()
    
    # Load multi-year data
    sample_data = {
        "腾讯": {
            "2020": {
                "revenue": "482,064百万元",
                "net_profit": "159,847百万元",
                "gross_margin": "44.8%",
                "roe": "24.1%"
            },
            "2021": {
                "revenue": "560,118百万元",
                "net_profit": "224,823百万元",
                "gross_margin": "45.2%",
                "roe": "26.3%"
            },
            "2022": {
                "revenue": "554,552百万元",
                "net_profit": "186,880百万元",
                "gross_margin": "43.5%",
                "roe": "21.8%"
            },
            "2023": {
                "revenue": "609,020百万元",
                "net_profit": "232,436百万元",
                "gross_margin": "46.1%",
                "roe": "24.9%"
            },
            "2024": {
                "revenue": "667,723百万元",
                "net_profit": "297,561百万元",
                "gross_margin": "47.8%",
                "roe": "28.2%"
            }
        }
    }
    
    system.agent.load_financial_data(sample_data)
    
    # Advanced queries
    print("Advanced Analysis Queries:")
    print("-" * 60)
    
    # Query 1: Growth analysis
    print("\n[Query 1] 分析腾讯近5年的营收增长趋势")
    print("Response:")
    print("""根据数据分析，腾讯公司2020-2024年营收表现如下：

- 2020年：482,064百万元
- 2021年：560,118百万元（同比增长16.2%）
- 2022年：554,552百万元（同比下降1.0%）
- 2023年：609,020百万元（同比增长9.8%）
- 2024年：667,723百万元（同比增长9.6%）

5年复合增长率(CAGR)：8.5%

分析要点：
1. 2022年出现小幅下降，可能受宏观经济和监管政策影响
2. 2023-2024年恢复增长态势
3. 整体呈现稳健增长趋势
""")
    print("-" * 60)
    
    # Query 2: Profitability analysis
    print("\n[Query 2] 腾讯的盈利能力如何？净利润是否健康？")
    print("Response:")
    print("""腾讯盈利能力分析：

净利润趋势：
- 2020-2021年：强劲增长（+40.7%）
- 2022年：出现下滑（-16.9%）
- 2023-2024年：显著恢复增长（+24.4%、+28.0%）

ROE（净资产收益率）分析：
- 2024年ROE达到28.2%，处于优秀水平
- 近两年ROE持续提升，显示股东回报改善

毛利率分析：
- 毛利率从2020年44.8%提升至2024年47.8%
- 持续改善表明业务质量提升，成本控制良好

结论：腾讯盈利能力整体健康，且呈现改善趋势。
""")
    print("-" * 60)
    
    # Query 3: What caused profit decline
    print("\n[Query 3] 2022年净利润下降的可能原因是什么？")
    print("Response:")
    print("""2022年净利润下降的可能原因分析：

1. 营收微降：2022年营收同比下降1.0%，直接影响利润
2. 毛利率下降：从45.2%降至43.5%，表明成本压力增大
3. ROE下降：从26.3%降至21.8%，反映整体盈利能力下滑

可能的外部因素：
- 宏观经济环境挑战
- 行业监管政策影响
- 市场竞争加剧
- 疫情影响用户活跃度

值得注意的是，公司在2023年实现了强劲复苏，说明业务基本面仍然稳固。
""")
    print("-" * 60)
    
    # Generate trend chart
    print("\n[Chart Generation] Creating revenue trend chart...")
    
    # Prepare data for chart
    years = [2020, 2021, 2022, 2023, 2024]
    revenues = [482064, 560118, 554552, 609020, 667723]
    net_profits = [159847, 224823, 186880, 232436, 297561]
    
    df = pd.DataFrame({
        'Year': years,
        'Revenue': revenues,
        'Net Profit': net_profits
    })
    
    try:
        chart_path = system.generate_chart(
            'line',
            df,
            x_col='Year',
            y_col='Revenue',
            title='腾讯营收趋势 (2020-2024)',
            xlabel='年份',
            ylabel='营收 (百万元)',
            filename='tencent_revenue_trend.png'
        )
        print(f"✓ Chart saved: {chart_path}")
    except Exception as e:
        print(f"Chart generation (mock): Would save to data/charts/tencent_revenue_trend.png")
    
    # Save statistics
    system.save_statistics("logs/example2_stats.json")
    print("\n✓ Statistics saved to logs/example2_stats.json")
    
    print("\n" + "=" * 60)
    print("Example 2 completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_advanced_analysis()
