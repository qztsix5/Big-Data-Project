# Quick Start Guide - 快速入门指南

## 5分钟快速开始

### 1. 安装 (1分钟)

```bash
# 克隆仓库
git clone <repository-url>
cd financial-report-analysis

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 (1分钟)

```bash
# 复制配置文件
cp .env.example .env

# 编辑 .env，添加你的 API key
# OPENAI_API_KEY=sk-your-key-here
```

### 3. 运行示例 (3分钟)

```bash
# 运行基础示例
python examples/example1_basic_query.py

# 运行高级分析示例
python examples/example2_advanced_analysis.py

# 运行多轮对话示例
python examples/example3_multi_turn.py
```

## 基本使用

### 导入财报数据

```python
from main import FinancialReportSystem

# 初始化系统
system = FinancialReportSystem()

# 从PDF导入
system.import_report(
    file_path="data/raw/company_report.pdf",
    company_name="公司名称",
    year=2024
)
```

### 查询分析

```python
# 单次查询
response = system.query("公司2024年营收是多少？")
print(response)

# 多轮对话
questions = [
    "公司2024年营收增长如何？",
    "增长主要来自哪里？",
    "未来趋势如何？"
]
conversation = system.multi_turn_query(questions)
```

### 生成图表

```python
import pandas as pd

# 准备数据
data = pd.DataFrame({
    'Year': [2020, 2021, 2022, 2023, 2024],
    'Revenue': [100000, 120000, 135000, 150000, 180000]
})

# 生成趋势图
chart_path = system.generate_chart(
    'line',
    data,
    x_col='Year',
    y_col='Revenue',
    title='营收趋势'
)
```

## 常见场景

### 场景1：基础数据查询

```python
# 查询单个指标
system.query("阿里巴巴2024年净利润是多少？")

# 查询多个指标
system.query("给我阿里巴巴2024年的营收、净利润和ROE")
```

### 场景2：趋势分析

```python
# 分析增长趋势
system.query("分析腾讯近5年的营收增长趋势")

# 分析下降原因
system.query("2022年净利润为什么下降？")
```

### 场景3：对比分析

```python
# 同行对比
system.query("比亚迪和特斯拉的毛利率对比")

# 跨年度对比
system.query("比较2023年和2024年的盈利能力")
```

### 场景4：预测建议

```python
# 未来预测
system.query("基于历史数据，预测明年的营收增长")

# 投资建议
system.query("从财务角度，这家公司值得投资吗？")
```

## 进阶功能

### 自动抓取财报

```python
# 从网络抓取多年度数据
system.import_from_web(
    company_name="腾讯",
    years=[2020, 2021, 2022, 2023, 2024]
)
```

### 跨公司对比

```python
# 加载多家公司数据
companies = ["阿里巴巴", "腾讯", "比亚迪"]
for company in companies:
    system.import_report(f"data/{company}_2024.pdf", company, 2024)

# 进行对比分析
system.query("对比这三家公司的盈利能力")
```

### 导出分析结果

```python
# 导出处理后的数据
system.export_data("output/financial_data.xlsx", format="excel")

# 保存统计信息
system.save_statistics("logs/statistics.json")
```

## 自定义配置

### 修改 LLM 模型

编辑 `config/config.yaml`:

```yaml
llm:
  model: "gpt-3.5-turbo"  # 或 "gpt-4"
  temperature: 0.7
  max_tokens: 2000
```

### 添加自定义指标

编辑 `config/config.yaml`:

```yaml
metrics:
  core:
    - revenue
    - net_profit
    - your_custom_metric  # 添加自定义指标
```

## 故障排查

### 问题1：导入错误

```bash
# 确保虚拟环境已激活
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 重新安装依赖
pip install -r requirements.txt
```

### 问题2：API Key 错误

```bash
# 检查 .env 文件
cat .env

# 确保格式正确
OPENAI_API_KEY=sk-...
```

### 问题3：中文显示问题

```python
# 在 chart_generator.py 中修改字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows
# 或
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac
```

## 获取帮助

- 查看完整文档：`docs/REPORT.md`
- 查看安装指南：`docs/SETUP.md`
- 查看示例代码：`examples/`
- 提交Issue：GitHub Issues

## 下一步

1. ✅ 完成快速开始
2. 📚 阅读完整文档
3. 💻 运行所有示例
4. 🔧 根据需求自定义
5. 📊 分析你的财报数据

Happy Analyzing! 🚀
