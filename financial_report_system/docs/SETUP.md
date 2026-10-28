# Installation and Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd financial-report-analysis
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter installation issues, you can install packages individually:

```bash
# Core AutoGen
pip install pyautogen

# Data Processing
pip install pandas openpyxl PyPDF2 pdfplumber beautifulsoup4 lxml

# Web Scraping
pip install requests selenium

# Visualization
pip install matplotlib seaborn plotly

# Database
pip install sqlalchemy

# LLM APIs
pip install openai python-dotenv

# Utilities
pip install tqdm loguru pyyaml
```

### 4. Configure API Keys

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-...
```

### 5. Test the Installation

```bash
python test_system.py
```

## Configuration

### LLM Configuration

Edit `config/config.yaml` to configure:

- LLM model (default: gpt-4)
- Temperature and other parameters
- Agent behavior settings

### Data Storage

Choose between Excel or SQL storage:

```yaml
data:
  output_format: "excel"  # or "sql"
  database_url: "sqlite:///data/processed/financial_reports.db"
```

## Running Examples

After installation, run the example scripts:

```bash
# Basic queries
python examples/example1_basic_query.py

# Advanced analysis
python examples/example2_advanced_analysis.py

# Multi-turn conversations
python examples/example3_multi_turn.py
```

## Troubleshooting

### Import Errors

If you get import errors, make sure:
1. Virtual environment is activated
2. All dependencies are installed: `pip list`
3. You're running from the project root directory

### API Key Issues

If you see API key errors:
1. Check that `.env` file exists
2. Verify your OpenAI API key is valid
3. Ensure `.env` is in the project root

### Chart Generation Issues

For matplotlib/Chinese font issues:
1. Install Chinese fonts on your system
2. Or modify `src/visualization/chart_generator.py` to use available fonts

## Next Steps

1. Import your financial report data
2. Customize the configuration
3. Start analyzing!

For more information, see the main README.md
