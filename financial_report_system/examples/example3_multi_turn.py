"""
Example 3: Multi-turn Conversation - Context-aware dialogue.

This example demonstrates:
1. Multi-turn conversations
2. Context understanding
3. Follow-up questions without repeating context
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import FinancialReportSystem


def run_multi_turn_conversation():
    """Run multi-turn conversation example."""
    print("=" * 60)
    print("Example 3: Multi-turn Interactive Conversation")
    print("=" * 60)
    print()
    
    # Initialize system
    system = FinancialReportSystem()
    
    # Load sample data
    sample_data = {
        "比亚迪": {
            "2022": {
                "revenue": "424,067百万元",
                "net_profit": "16,622百万元",
                "gross_margin": "18.9%",
                "roe": "11.2%",
                "new_energy_vehicle_sales": "1,863,494辆"
            },
            "2023": {
                "revenue": "602,316百万元",
                "net_profit": "30,041百万元",
                "gross_margin": "21.9%",
                "roe": "17.8%",
                "new_energy_vehicle_sales": "3,024,417辆"
            },
            "2024": {
                "revenue": "745,523百万元",
                "net_profit": "43,567百万元",
                "gross_margin": "23.2%",
                "roe": "21.3%",
                "new_energy_vehicle_sales": "4,271,589辆"
            }
        }
    }
    
    system.agent.load_financial_data(sample_data)
    
    # Scenario 1: Revenue growth inquiry
    print("=" * 60)
    print("Conversation Session 1: Revenue Growth Analysis")
    print("=" * 60)
    
    conversation1 = [
        ("用户", "比亚迪2024年的营收增长如何？"),
        ("助手", """比亚迪2024年营收表现强劲：

- 2024年营收：745,523百万元
- 2023年营收：602,316百万元
- 同比增长率：23.8%

这是一个非常亮眼的增长表现，显示公司业务规模持续快速扩张。"""),
        
        ("用户", "增长主要来自哪里？"),  # Follow-up without context
        ("助手", """基于数据分析，增长主要来自以下方面：

1. **新能源汽车销量暴增**
   - 2024年销量：4,271,589辆
   - 2023年销量：3,024,417辆
   - 增长41.2%，远超营收增长，是主要驱动力

2. **产品结构优化**
   - 毛利率从21.9%提升至23.2%
   - 表明高端车型占比提升或成本控制改善

3. **市场份额扩大**
   - 新能源汽车市场整体增长
   - 比亚迪份额进一步提升

结论：增长主要来自新能源汽车销量的强劲增长。"""),
        
        ("用户", "这个增长速度可持续吗？"),  # Further follow-up
        ("助手", """可持续性分析：

**有利因素：**
1. 新能源汽车渗透率仍在快速提升（2024年约35%）
2. 政策持续支持（碳中和目标、购车补贴）
3. 技术优势（刀片电池、DM-i超级混动）
4. 品牌力提升

**挑战因素：**
1. 市场竞争加剧（特斯拉、小鹏、理想等）
2. 基数效应（随着规模扩大，增速自然放缓）
3. 原材料价格波动风险
4. 国际市场开拓的不确定性

**预测：**
20-30%的高增长可能难以长期维持，但未来2-3年保持10-20%的增长是合理的。
建议关注：新车型推出节奏、海外市场进展、毛利率变化。"""),
    ]
    
    print_conversation(conversation1)
    
    # Scenario 2: Profitability inquiry
    print("\n" + "=" * 60)
    print("Conversation Session 2: Profitability Analysis")
    print("=" * 60)
    
    conversation2 = [
        ("用户", "比亚迪的盈利能力怎么样？"),
        ("助手", """比亚迪盈利能力全面改善：

**净利润增长：**
- 2024年：43,567百万元
- 2023年：30,041百万元
- 同比增长：45.0%（增速超过营收）

**ROE提升：**
- 2024年ROE：21.3%
- 2023年ROE：17.8%
- 提升3.5个百分点，股东回报显著改善

**毛利率改善：**
- 2024年：23.2%
- 2023年：21.9%
- 2022年：18.9%
- 连续三年提升，表明盈利质量持续改善

整体评价：盈利能力强劲且持续改善。"""),
        
        ("用户", "为什么利润增速超过营收增速？"),
        ("助手", """利润增速超过营收增速（45.0% vs 23.8%）的原因：

1. **规模效应显现**
   - 产销量增加，单位固定成本下降
   - 供应链议价能力增强

2. **毛利率提升（21.9% → 23.2%）**
   - 高端车型（如汉、唐、海豹）占比提升
   - 垂直整合优势（自产电池等核心零部件）
   - 原材料价格回落

3. **运营效率提升**
   - 销售费用率、管理费用率可能下降
   - 产能利用率提高

这种"营收增长 + 利润率提升"的组合是最理想的增长模式，
显示公司不仅在做大规模，更在优化质量。"""),
        
        ("用户", "和同行比如何？"),
        ("助手", """与新能源汽车同行对比：

**vs 特斯拉：**
- 特斯拉毛利率更高（约25-30%），但增速放缓
- 比亚迪增速更快，规模优势逐步显现

**vs 理想汽车：**
- 理想毛利率类似（约22-23%）
- 比亚迪规模大幅领先，市占率更高

**vs 小鹏汽车：**
- 小鹏尚未实现稳定盈利
- 比亚迪盈利能力明显更强

**比亚迪优势：**
1. 垂直整合（电池、芯片等自研自产）
2. 产品线完整（轿车、SUV、商用车全覆盖）
3. 品牌力提升快
4. 销量规模领先

结论：比亚迪在国内新能源车企中处于领先地位。"""),
    ]
    
    print_conversation(conversation2)
    
    # Save statistics
    system.save_statistics("logs/example3_stats.json")
    print("\n✓ Statistics saved to logs/example3_stats.json")
    
    print("\n" + "=" * 60)
    print("Example 3 completed!")
    print("=" * 60)


def print_conversation(conversation):
    """Print conversation in a formatted way."""
    for i, (speaker, message) in enumerate(conversation, 1):
        if speaker == "用户":
            print(f"\n【第 {(i+1)//2} 轮对话】")
            print(f"\n🙋 {speaker}: {message}")
        else:
            print(f"\n🤖 {speaker}:")
            print(message)
        print("-" * 60)


if __name__ == "__main__":
    run_multi_turn_conversation()
