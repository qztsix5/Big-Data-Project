# 智能财报分析系统 - Financial Report Analysis System

基于 AutoGen 框架构建的智能财报分析系统，实现从财报获取到深度解读的全流程自动化。

## 📋 项目概述

本系统是一套覆盖 "数据处理 - 交互解读 - 能力扩展" 的智能财报分析平台，包含：

- **数据处理工作流**：支持 PDF/Excel/网页格式财报的导入和结构化处理
- **智能 Agent 模块**：基于 AutoGen 的多轮对话式财务分析助手
- **可视化模块**：自动生成财务数据图表
- **扩展功能**：网页抓取、外部信息集成、跨公司对比等

## 🏗️ 系统架构

```
Financial Report Analysis System
├── 数据处理模块 (Data Processing)
│   ├── PDF Parser - 解析 PDF 财报
│   ├── Excel Parser - 解析 Excel 财报
│   ├── Web Scraper - 网页数据抓取
│   └── Data Storage - 数据存储（Excel/SQL）
│
├── 智能 Agent 模块 (Intelligent Agent)
│   ├── AutoGen Framework - 基于 AutoGen 的对话系统
│   ├── Context Manager - 上下文管理
│   └── Function Registry - 自定义函数注册
│
├── 可视化模块 (Visualization)
│   ├── Chart Generator - 图表生成
│   └── Trend Analysis - 趋势分析
│
└── 工具模块 (Utilities)
    ├── Configuration - 配置管理
    ├── Logger - 日志系统
    └── Statistics Tracker - 统计追踪
```

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，添加你的 OpenAI API Key：
```
OPENAI_API_KEY=your_api_key_here
```

3. （可选）修改 `config/config.yaml` 中的配置

### 运行示例

```bash
# 基础查询示例
python examples/example1_basic_query.py

# 高级分析示例
python examples/example2_advanced_analysis.py

# 多轮对话示例
python examples/example3_multi_turn.py
```

## 📊 核心功能

详细文档请查看：[完整 README](docs/FULL_README.md)

## 📁 项目结构

```
.
├── config/                 # 配置文件
├── data/                  # 数据目录
├── examples/              # 示例代码
├── logs/                  # 日志文件
├── src/                   # 源代码
│   ├── agents/           # Agent 模块
│   ├── data_processing/  # 数据处理
│   ├── visualization/    # 可视化
│   └── utils/            # 工具函数
├── main.py               # 主程序
└── requirements.txt      # 依赖包
```

## 🔧 技术栈

- **AI Framework**: AutoGen
- **LLM**: GPT-4 / GPT-3.5
- **Data Processing**: Pandas, PyPDF2, pdfplumber
- **Visualization**: Matplotlib, Seaborn

## 📚 参考文献

1. AutoGen: https://microsoft.github.io/autogen/
2. Template-Based Financial Report Generation
3. DIN-SQL: Text-to-SQL with Self-Correction
4. DeepResearcher: RL in Real-world Environments

---

**Built with ❤️ using AutoGen Framework**