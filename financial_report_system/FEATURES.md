# 功能展示 - Feature Showcase

## 系统概览

智能财报分析系统是一个基于 AutoGen 框架的完整解决方案，涵盖从数据获取到深度分析的全流程。

## 核心功能展示

### 1. 数据导入 - 多格式支持

#### PDF 财报导入
```python
from main import FinancialReportSystem

system = FinancialReportSystem()

# 导入 PDF 格式财报
system.import_report(
    file_path="data/raw/alibaba_annual_report_2024.pdf",
    company_name="阿里巴巴",
    year=2024
)
```

**支持的提取内容：**
- 文本内容完整提取
- 财务报表表格识别
- 核心指标自动匹配
  - 营业收入 (Revenue)
  - 净利润 (Net Profit)
  - 总资产 (Total Assets)
  - ROE（净资产收益率）
  - 毛利率 (Gross Margin)
  - 等 8+ 核心指标

#### Excel 财报导入
```python
# 导入 Excel 格式财报
system.import_report(
    file_path="data/raw/tencent_financial_2024.xlsx",
    company_name="腾讯",
    year=2024
)
```

**支持的功能：**
- 多工作表自动识别
- 财务指标智能定位
- 时间序列数据提取
- 多年度数据批量处理

#### 网页数据抓取（加分项）
```python
# 从公开平台自动抓取
system.import_from_web(
    company_name="比亚迪",
    years=[2020, 2021, 2022, 2023, 2024]
)
```

**支持的平台：**
- 巨潮资讯网 (cninfo.com.cn)
- 东方财富 (eastmoney.com)
- 自定义平台扩展

### 2. 智能对话 - 自然语言交互

#### 基础查询
```python
# 简单查询
response = system.query("阿里巴巴2024年的营收是多少？")
# 输出: "根据财务数据，阿里巴巴2024年的营业收入为941,168百万元。"

# 复合查询
response = system.query("给我阿里巴巴2024年的营收、净利润和ROE")
# 输出: "阿里巴巴2024年财务数据：营收941,168百万元，净利润80,234百万元，ROE 9.1%"
```

#### 趋势分析
```python
response = system.query("分析腾讯近5年的营收增长趋势")
```

**输出示例：**
```
腾讯2020-2024年营收表现：
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
```

#### 原因分析
```python
response = system.query("2022年净利润为什么下降？")
```

**输出示例：**
```
2022年净利润下降的可能原因分析：

数据层面：
1. 营收同比下降1.0%
2. 毛利率从45.2%降至43.5%
3. ROE从26.3%降至21.8%

外部因素：
- 宏观经济环境挑战
- 行业监管政策影响
- 市场竞争加剧
- 疫情影响用户活跃度
```

#### 行业对比
```python
response = system.query("比亚迪和特斯拉的盈利能力对比")
```

**输出示例：**
```
比亚迪 vs 特斯拉盈利能力对比：

毛利率：
- 特斯拉：25-30%（更高）
- 比亚迪：23.2%

ROE：
- 比亚迪：21.3%（优秀）
- 特斯拉：约20%

增长速度：
- 比亚迪：营收+23.8%，利润+45.0%
- 特斯拉：增速放缓

比亚迪优势：增长速度、销量规模
特斯拉优势：利润率、品牌溢价
```

### 3. 多轮对话 - 上下文理解

```python
# 连续对话，无需重复上下文
conversation = system.multi_turn_query([
    "比亚迪2024年营收增长如何？",          # 第1轮
    "增长主要来自哪里？",                   # 第2轮 - 自动理解"增长"指比亚迪营收
    "这个增长速度可持续吗？",               # 第3轮 - 继续保持上下文
    "有什么风险需要注意？"                  # 第4轮 - 深入分析
])
```

**对话特点：**
- ✅ 自动保持上下文
- ✅ 无需重复前提信息
- ✅ 支持追问和深入
- ✅ 连贯的分析逻辑

### 4. 图表生成 - 可视化分析

#### 营收趋势图
```python
import pandas as pd

data = pd.DataFrame({
    'Year': [2020, 2021, 2022, 2023, 2024],
    'Revenue': [482064, 560118, 554552, 609020, 667723]
})

chart_path = system.generate_chart(
    'line',
    data,
    x_col='Year',
    y_col='Revenue',
    title='腾讯营收趋势 (2020-2024)',
    xlabel='年份',
    ylabel='营收 (百万元)'
)
```

**生成的图表：**
- 专业的折线图
- 中文标签支持
- 清晰的网格线
- 高分辨率输出（300 DPI）

#### 多指标对比图
```python
data = pd.DataFrame({
    'Year': [2020, 2021, 2022, 2023, 2024],
    'Revenue': [133082, 216142, 424067, 602316, 745523],
    'Net Profit': [4242, 3045, 16622, 30041, 43567]
})

chart_path = system.generate_chart(
    'bar',
    data,
    x_col='Year',
    y_cols=['Revenue', 'Net Profit'],
    title='比亚迪营收与利润对比'
)
```

**图表类型：**
- 📈 折线图 (Line Chart) - 趋势分析
- 📊 柱状图 (Bar Chart) - 对比分析
- 📉 趋势对比图 - 多指标
- 🔄 跨公司对比图 - 行业分析

### 5. 高级分析 - 数据洞察

#### 增长率计算
```python
# CAGR（复合年均增长率）计算
response = system.query("计算腾讯2020-2024年营收的复合增长率")
# 输出: "腾讯2020-2024年营收CAGR为8.5%"
```

#### 跨公司对比
```python
# 加载多家公司数据后
response = system.query("对比阿里巴巴、腾讯、比亚迪三家公司的盈利能力")
```

**输出示例：**
```
三家公司盈利能力对比（2024年）：

ROE排名：
1. 腾讯：28.2%（优秀）
2. 比亚迪：21.3%（良好）
3. 阿里巴巴：9.1%（一般）

毛利率排名：
1. 腾讯：47.8%
2. 阿里巴巴：38.5%
3. 比亚迪：23.2%

增长速度排名（营收CAGR 2020-2024）：
1. 比亚迪：53.6%
2. 腾讯：8.5%
3. 阿里巴巴：6.8%

结论：
- 腾讯：盈利能力最强，ROE和毛利率领先
- 比亚迪：增长最快，处于高速成长期
- 阿里巴巴：业务稳定，规模优势明显
```

#### 财务健康度分析
```python
response = system.query("分析比亚迪的财务健康状况")
```

**分析维度：**
- 资产负债率
- 经营现金流
- 流动性指标
- 偿债能力
- 综合评级

### 6. 外部信息集成（加分项）

#### 政策影响分析
```python
response = system.query("分析新能源汽车相关政策对比亚迪的影响")
```

**集成信息：**
- 购置税减免政策
- 双碳目标政策
- 地方补贴政策
- 行业准入标准

#### 市场新闻整合
```python
response = system.query("最近有什么新闻可能影响腾讯的股价？")
```

**信息来源：**
- 财经新闻
- 行业动态
- 政策发布
- 竞品信息

### 7. 数据导出

#### Excel 导出
```python
# 导出处理后的数据
system.export_data(
    output_path="output/financial_analysis_results.xlsx",
    format="excel"
)
```

#### SQL 数据库
```python
# 配置使用 SQL 存储
system = FinancialReportSystem()
system.data_storage = DataStorage(storage_type="sql")

# 数据自动存储到数据库
system.import_report("report.pdf", "公司", 2024)
```

### 8. 统计和监控

#### 调用统计
```python
# 获取统计信息
stats = system.get_statistics()

print(f"总调用次数: {stats['total_agent_calls']}")
print(f"总Token使用: {stats['total_tokens']}")
print(f"平均每次Token: {stats['average_tokens_per_call']:.0f}")
```

#### 导出统计报告
```python
# 保存详细统计
system.save_statistics("logs/statistics.json")
```

**统计内容：**
```json
{
  "summary": {
    "total_agent_calls": 15,
    "total_tokens": 8567,
    "average_tokens_per_call": 571,
    "total_conversations": 3
  },
  "details": {
    "queries": [...],
    "conversations": [...]
  }
}
```

## 使用场景示例

### 场景 1: 投资决策支持
```python
# 分析公司投资价值
questions = [
    "阿里巴巴的盈利能力如何？",
    "近5年增长趋势怎样？",
    "和腾讯相比有什么优势？",
    "主要风险是什么？",
    "适合长期持有吗？"
]
conversation = system.multi_turn_query(questions)
```

### 场景 2: 行业研究
```python
# 新能源汽车行业分析
system.import_report("byd_2024.pdf", "比亚迪", 2024)
system.import_report("tesla_2024.pdf", "特斯拉", 2024)
system.import_report("li_auto_2024.pdf", "理想汽车", 2024)

response = system.query("对比这三家新能源车企的竞争力")
```

### 场景 3: 财报解读
```python
# 快速了解财报要点
response = system.query("总结阿里巴巴2024年财报的核心要点")
```

### 场景 4: 趋势预测
```python
# 基于历史数据预测
response = system.query("基于过去5年数据，预测比亚迪2025年营收范围")
```

## 系统优势

### 1. 智能化
- ✅ 基于 GPT-4 的深度理解
- ✅ 自然语言交互
- ✅ 自动推理和分析
- ✅ 上下文连续性

### 2. 自动化
- ✅ 自动数据提取
- ✅ 自动指标计算
- ✅ 自动图表生成
- ✅ 自动报告生成

### 3. 专业性
- ✅ 财务指标完整
- ✅ 分析方法科学
- ✅ 对比维度全面
- ✅ 结论客观准确

### 4. 易用性
- ✅ 简单的 API
- ✅ 丰富的示例
- ✅ 完善的文档
- ✅ 清晰的错误提示

## 技术特点

- **模块化**: 各模块职责清晰，易于维护
- **可扩展**: 支持自定义指标、数据源、分析方法
- **高性能**: 支持批量处理和并发
- **可靠性**: 完善的错误处理和日志记录

## 开始使用

1. **安装**: `pip install -r requirements.txt`
2. **配置**: 复制 `.env.example` 为 `.env` 并添加 API key
3. **运行**: `python examples/example4_complete_workflow.py`
4. **学习**: 查看 `docs/` 目录中的完整文档

## 获取帮助

- 📖 **完整文档**: `docs/REPORT.md`
- 🚀 **快速开始**: `docs/QUICKSTART.md`
- ⚙️ **安装指南**: `docs/SETUP.md`
- 💡 **示例代码**: `examples/` 目录

---

**立即开始智能财报分析！** 🎉
