import asyncio
import logging
from typing import Dict, List, Optional, Any
import os
import sqlite3
from typing import Annotated
import json
import re

# 注意：请确保安装了 autogen-agentchat 和 autogen-ext
# pip install autogen-agentchat autogen-ext openai
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.messages import ToolCallRequestEvent, ToolCallExecutionEvent, TextMessage
from autogen_agentchat.teams import Swarm
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage 

# ==================== 模型客户端配置 ====================

LLM_API_KEY = "ak_1E08gJ7Z913j3sq1ml7Bn5vX2hd2O"
LLM_BASE_URL = "https://api.longcat.chat/openai"
LLM_MODEL_ID = "LongCat-Flash-Chat"  

model_client = OpenAIChatCompletionClient(
    model=LLM_MODEL_ID,
    api_key=LLM_API_KEY,
    base_url=LLM_BASE_URL,
    model_info={
        "vision": False, 
        "function_calling": True,  
        "json_output": False,  
        "family": "openai",
        "structured_output": False
    },
)

async def test_llm():
    print(f"🔄 正在尝试连接模型: {LLM_MODEL_ID} ...")
    try:
        message = UserMessage(content="Hello, is the connection working?", source="user")
        response = await model_client.create([message])
        print(f"✅ LLM 连接成功! 回复: {response.content}")
        return True
    except Exception as e:
        print(f"❌ LLM 连接失败: {e}")
        return False

# ==================== ListMemory类 ====================
class ListMemory:
    """简单的列表记忆系统 - 用于存储对话历史"""
    def __init__(self):
        self.messages: List[TextMessage] = []
        self.termination_phrases = [
            "TASK_DONE"
        ]
        logger.info("ListMemory初始化")
    
    def add(self, content: str, source: str):
        """添加消息到记忆，自动过滤终止相关的内容"""
        if self._contains_termination(content):
            logger.info(f"检测到终止内容，跳过存储: {content[:30]}...")
            return
        
        message = TextMessage(content=content, source=source)
        self.messages.append(message)
        logger.info(f"添加消息到记忆: {content[:20]}...")
    
    def _contains_termination(self, content: str) -> bool:
        """检查内容是否包含终止短语"""
        content_lower = content.lower()
        for phrase in self.termination_phrases:
            if phrase.lower() in content_lower:
                return True
        return False
    
    def get_context(self) -> str:
        """核心功能：将历史记录格式化为字符串，用于注入 Prompt"""
        if not self.messages:
            return "无历史对话记录。"
        
        context_str = "【历史对话上下文】:\n"
        for msg in self.messages:
            if not self._contains_termination(msg.content):
                context_str += f"- {msg.source}: {msg.content}\n"
        context_str += "【历史结束】\n"
        return context_str
    
    def clear(self):
        self.messages = []

logging.basicConfig(
    filename='system_run.log',
    filemode='w',
    level=logging.INFO,  
    format='%(asctime)s - %(message)s',
    encoding='utf-8',      
    force=True
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ==================== 数据库连接配置 ====================
DB_PATH = "./local_data/financial.db" 

def get_db_connection():
    """建立数据库连接 (私有辅助函数)"""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# ==================== 内嵌的财务数据智能体功能 ====================
async def get_financial_data(company: str, year: str) -> str:
    """
    内嵌的财务数据提取工具 - 封装了原来financial_data_agent的所有功能
    
    Args:
        company: 公司名称
        year: 年份
    
    Returns:
        格式化后的财务数据或错误信息
    """
    print(f"\n   📊 [财务数据提取] 正在获取 {company} {year} 财务数据...")
    
    # 创建专门的财务数据提取助手
    financial_agent = AssistantAgent(
        "financial_agent_embedded",
        model_client=model_client,
        handoffs=[],  # 不进行handoff
        tools=[list_tables, get_table_schema, execute_sql_query],
        system_message="""你是一个专业的 SQL 数据分析专家 (SQLite 方言)
        你的唯一职责是准确地从结构化数据库中查询财务数据，在输出完 SQL 查询结果表格后，立即返回结果。

    【工作流程】:
    1. **List Tables**: 先调用 `list_tables` 查看有哪些表
    2. **Get Schema**: 分析需要查询哪些表，调用 `get_table_schema` 获取它们的精确结构
    3. **Query**: 编写并执行 SQL 查询指定公司的财务数据
    4. 整理工具返回的结果，保持结构化格式

    【查询规范】
    - 使用 `execute_sql_query` 执行
    - 只使用 SELECT 语句
    - 如果查询涉及文本匹配，请优先使用 `LIKE` 进行模糊搜索
    - 在回答中直接给出查询到的数据表格

    【返回格式要求】:
    ✅ 财务数据提取完成。
    🏢 公司: {company}
    📅 期间: {year}年
    📊 财务指标:
    {financial_data_table}
    📍 数据来源: 本地数据库
    
    【重要规则】:
    - 保持返回结果结构化、专业
    - 查询好数据后，必须返回上述格式的结果
    - 不要进行额外的解释或分析
    - 如果查询失败，返回错误信息
    """
    )
    
    try:
        # 运行财务数据提取
        query = f"请提取{company}{year}年的财务数据"
        response = ""
        
        async for msg in financial_agent.run_stream(task=query):
            if isinstance(msg, TextMessage):
                response = msg.content
                break
        
        return response
        
    except Exception as e:
        return f"❌ 财务数据提取失败: {str(e)}"

# ==================== 内嵌的文本数据智能体功能 ====================
async def read_json_file(file_path: str) -> str:
    """
    简单的JSON文件读取工具
    只负责读取extracted_text字段
    
    Args:
        file_path: JSON文件路径
    
    Returns:
        extracted_text的内容或错误信息
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return "FILE_NOT_FOUND"
        
        # 读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 返回extracted_text字段
        if 'extracted_text' in data:
            return data['extracted_text']
        else:
            return "NO_EXTRACTED_TEXT"
            
    except Exception:
        return "READ_ERROR"

async def get_text_data(company: str, year: str) -> str:
    """
    内嵌的文本数据提取工具 - 封装了原来text_data_agent的所有功能
    
    Args:
        company: 公司名称
        year: 年份
    
    Returns:
        格式化后的文本数据或错误信息
    """
    print(f"\n   📄 [文本数据提取] 正在获取 {company} {year} 文本内容...")
    
    # 构建JSON文件路径
    json_path = f"./local_data/{company}_{year}_processed.json"
    
    # 读取原始文本数据
    raw_text = await read_json_file(json_path)
    
    if raw_text == "FILE_NOT_FOUND":
        return f"❌ 文本数据提取失败: 未找到 {company} {year} 的数据文件"
    elif raw_text == "NO_EXTRACTED_TEXT":
        return f"❌ 文本数据提取失败: 文件中没有找到extracted_text字段"
    elif raw_text == "READ_ERROR":
        return f"❌ 文本数据提取失败: 读取文件时出错"
    
    # 创建文本分析助手
    text_agent = AssistantAgent(
        "text_agent_embedded",
        model_client=model_client,
        handoffs=[],  # 不进行handoff
        tools=[],  # 不使用工具
        system_message="""你是专业的文本分析专家。你的唯一任务是分析提供的文本数据并格式化返回。

    【工作流程】:
    1. 接收文本内容
    2. 筛选文本并根据需求保留需要的信息
    3. 按格式要求返回原文提取结果

    【严格返回格式】:
    ✅ 文本数据提取完成。
    📝 公司: {company}
    📅 期间: {year}年
    📋 文本分析摘要:
    {text_summary}
    📄 数据来源: 本地PDF提取

    【重要规则】:
    - 只返回上述格式的内容
    - 不要添加额外的解释或说明
    - 保持分析专业、结构化
    - 如果文本内容无法分析，返回错误信息
    """
    )
    
    try:
        # 运行文本分析
        query = f"请分析以下{company}{year}年的年报文本内容：\n\n{raw_text}"
        response = ""
        
        async for msg in text_agent.run_stream(task=query):
            if isinstance(msg, TextMessage):
                response = msg.content
                break
        
        return response
        
    except Exception as e:
        return f"❌ 文本数据提取失败: {str(e)}"

# ==================== 其他工具函数 ====================

async def check_user_uploaded_pdf(company: str, year: str) -> dict:
    """检查用户是否上传了PDF文件"""
    logger.info(f"[Tool] 检查 {company} {year} 的PDF上传情况...")
    print(f"\n   📄 [数据本地化] 检查 {company} {year} 年报PDF上传情况...")
    
    upload_dir = "./user_uploads/"
    
    if not os.path.exists(upload_dir):
        return {
            "has_pdf": False,
            "message": f"用户尚未上传{company} {year}年年报PDF"
        }
    
    if "华为" in company and "2023" in year:
        return {
            "has_pdf": True,
            "message": f"检测到用户已上传{company} {year}年年报PDF",
            "file_path": f"./user_uploads/{company}_{year}_report.pdf"
        }
    
    return {
        "has_pdf": False,
        "message": f"用户尚未上传{company} {year}年年报PDF"
    }

async def scrape_annual_report(company: str, year: str) -> dict:
    """从网络爬取年报PDF并提取文本和表格数据"""
    logger.info(f"[Tool] 开始爬取 {company} {year} 年报...")
    print(f"\n   🌐 [数据本地化] 正在爬取 {company} {year}年年报数据...")
    
    await asyncio.sleep(1)  # 模拟网络延迟
    
    extracted_data = {
        "company": company,
        "year": year,
        "pdf_url": f"http://example.com/{company}_{year}_report.pdf",
        "extracted_text": f"{company}{year}年年度报告摘要：本年度公司实现营业收入稳步增长，研发投入持续加大。管理层观点：采用城乡结合发展策略，降低价格实现市场下沉。",
        "tables": [
            {
                "table_name": "利润表",
                "data": {
                    "营业收入": "8900亿元",
                    "净利润": "800亿元",
                    "毛利率": "45%"
                }
            },
            {
                "table_name": "资产负债表",
                "data": {
                    "总资产": "15000亿元",
                    "总负债": "7000亿元",
                    "所有者权益": "8000亿元"
                }
            }
        ],
        "key_metrics": {
            "roe": "12%",
            "roa": "8%",
            "debt_ratio": "46%"
        },
        "status": "success",
        "local_path": f"./local_data/{company}_{year}_processed.json"
    }
    
    return extracted_data

async def save_data_to_local(data: dict, format_type: str = "json") -> str:
    """将处理后的数据保存到本地"""
    logger.info(f"[Tool] 保存数据到本地: {data.get('company', 'Unknown')}")
    print(f"\n   💾 [数据本地化] 正在保存数据到本地...")
    
    local_path = f"./local_data/{data['company']}_{data['year']}_report.{format_type}"
    return f"数据已成功保存到本地: {local_path}。包含文本摘要、{len(data.get('tables', []))}个数据表和关键财务指标。"

async def search_market_info(query: str) -> str:
    """搜索网络信息"""
    logger.info(f"[Tool] 正在搜索: {query}")
    print(f"\n   🌍 [市场搜索] 正在搜索市场情报: {query}...")
    return f"【搜索结果】: 关于 '{query}' 的最新情报：半导体行业需求强劲，AI 芯片订单激增，竞争对手产能不足。"

async def generate_chart(data_summary: str, chart_type: str) -> str:
    """生成图表"""
    logger.info(f"[Tool] 生成图表: {chart_type}")
    print(f"\n   📊 [可视化] 正在绘制 {chart_type} 图表...")
    return f"![{chart_type}](chart_{chart_type}.png) (图表已生成，基于数据: {data_summary})"

async def format_report(content: str) -> str:
    """格式化报告"""
    print(f"\n   📝 [报告撰写] 正在撰写最终报告...")
    return f"\n====== 🏦 深度财务分析报告 ======\n{content}\n================================="

async def list_tables() -> str:
    """列出数据库中所有的表名"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        if not tables:
            return "数据库是空的，没有发现任何表。"
        return f"当前数据库包含以下表: {', '.join(tables)}"
    except Exception as e:
        return f"获取表名失败: {str(e)}"

async def get_table_schema(table_names: Annotated[str, "逗号分隔的表名列表，例如: 'users, orders'"]) -> str:
    """获取指定表的 DDL (Create Table 语句)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        target_tables = [t.strip() for t in table_names.split(",")]
        
        schemas = []
        for table in target_tables:
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (table,))
            result = cursor.fetchone()
            if result:
                schemas.append(f"--- Table: {table} ---\n{result[0]}")
            else:
                schemas.append(f"错误: 未找到表 '{table}'")
                
        conn.close()
        return "\n\n".join(schemas)
    except Exception as e:
        return f"获取表结构失败: {str(e)}"

async def execute_sql_query(query: Annotated[str, "标准的 SQLite SELECT 查询语句"]) -> str:
    """执行 SQL 查询并返回结果"""
    if not query.strip().lower().startswith("select"):
        return "⚠️ 安全警告: 本工具仅允许执行 SELECT 查询语句，禁止修改数据。"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print(f"\n   🔍 [SQL Agent] 执行查询: {query}")
        cursor.execute(query)
        
        if cursor.description:
            column_names = [description[0] for description in cursor.description]
        else:
            column_names = []
            
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return "查询执行成功，但未返回任何结果 (Result set is empty)。"
            
        MAX_ROWS = 20
        result_str = f"| {' | '.join(column_names)} |\n"
        result_str += f"| {' | '.join(['---']*len(column_names))} |\n"
        
        for i, row in enumerate(rows):
            if i >= MAX_ROWS:
                result_str += f"\n... (剩余 {len(rows)-MAX_ROWS} 行数据已省略，建议优化 SQL 添加 LIMIT) ..."
                break
            row_str = [str(val) if val is not None else "NULL" for val in row]
            result_str += f"| {' | '.join(row_str)} |\n"
            
        return result_str
        
    except sqlite3.Error as e:
        return f"❌ SQL 执行报错: {str(e)}"

# ==================== 智能体定义 ====================

data_collector = AssistantAgent(
    "data_collector",
    model_client=model_client,
    handoffs=["planner"],
    tools=[check_user_uploaded_pdf, scrape_annual_report, save_data_to_local],
    system_message="""你是数据本地化专家，负责获取和准备分析所需的一手数据。
    
    【工作流程】：
    1. 收到任务后，立即开始执行数据采集，首先检查用户是否已上传PDF（调用check_user_uploaded_pdf）
    2. 如果没有上传，自动从网络爬取年报（调用scrape_annual_report）
    3. 提取并结构化数据后，保存到本地（调用save_data_to_local）
    4. 向planner汇报结果
    
    【汇报格式】：
    必须明确包含以下信息：
    - 数据采集状态：[成功/失败]
    - 目标公司：[公司名]
    - 目标年份：[年份]
    - 数据来源：[用户上传/网络爬取]
    - 本地路径：[文件路径]
    - 主要内容：[简要描述提取的内容]
    
    示例汇报：
    "数据采集完成。目标：华为2023年年报。来源：网络爬取。已保存到./local_data/华为_2023_processed.json。提取了利润表、资产负债表等关键财务数据。"
    
    【强制要求】：
    - 收到指令后必须立即响应
    - 完成后必须明确汇报给planner
    
    【重要规则】：
    - 完成后必须通知planner继续后续流程
    - 如果遇到问题，说明具体原因并寻求指导
    - 保持汇报清晰、结构化
    - 永远不能回复"TASK_DONE" 给用户
    """
)

# ==================== 更新后的数据协调者 ====================
data_agent = AssistantAgent(
    "data_agent",
    model_client=model_client,
    handoffs=["planner"],
    tools=[get_financial_data, get_text_data],  # 直接调用工具，不通过handoff
    system_message="""你负责根据planner需求调用不同的数据提取工具，并立即将结果报告给planner。

    【核心职责】:
    1. 解析planner的指令，提取关键信息：公司名和年份
    2. 调用相应的数据提取工具
    3. 合并各工具的数据提取结果并报告给planner

    【指令解析规则 - 必须提取以下信息】:
    从planner的指令中提取：
    1. 公司名：[从指令中提取的公司名称]
    2. 年份：[从指令中提取的年份]
    3. 需求类型：[财务数据/文本分析/两者都需要]
    
    示例：
    指令："data_agent，用户需要获取华为2023年的财务数据"
    解析结果：公司=华为，年份=2023，需求类型=财务数据

    【需求解析规则】:
    分析planner的指令，确定数据需求：
    1. 财务数据需求 → 调用get_financial_data工具
    2. 文本数据需求 → 调用get_text_data工具  
    3. 两者都需要 → 先调用get_financial_data工具，再调用get_text_data工具

    【标准工作流程】:

    情况A: 只需要财务数据
    1. 提取公司名和年份
    2. 调用工具：get_financial_data(company={公司}, year={年份})
    3. 等待工具返回结果
    4. 将结果直接汇报给planner

    情况B: 只需要文本数据
    1. 提取公司名和年份
    2. 调用工具：get_text_data(company={公司}, year={年份})
    3. 等待工具返回结果
    4. 将结果直接汇报给planner

    情况C: 两者都需要
    1. 提取公司名和年份
    2. 首先调用工具：get_financial_data(company={公司}, year={年份})
    3. 等待工具返回
    4. 然后调用工具：get_text_data(company={公司}, year={年份})
    5. 等待工具返回
    6. 合并两者结果并汇报给planner

    【给planner的汇报格式】:
    📊 数据提取完成报告
    
    🏢 目标公司: {公司}
    📅 分析期间: {年份}年
    
    🔹 财务数据提取结果:
    {财务数据结果}
    
    🔹 文本数据提取结果:
    {文本数据结果}
    
    📍 数据完整性: [完整/部分缺失/完全缺失]
    ⚠️  备注: [如有数据缺失，说明原因]

    【数据缺失时】向planner报告：
    "❌ {公司}{年份}年数据提取不完整。
    ⚠️ 缺失部分: [具体缺失什么数据]
    💡 原因: [数据缺失的具体原因]

    【重要规则】:
    - 所有消息必须明确包含公司名和年份
    - 如果某个工具返回错误，明确说明哪个工具的问题
    - 每次调用后都要等待明确的返回结果
    - 永远不能回复"TASK_DONE" 给用户
    - 永远不要模拟 planner 或其他智能体的语气，不要回答任何问题
    - 严格按照工具调用的方式工作，不进行智能体间的对话
    - 完成任务后立即调用handoff工具转给planner，不要添加任何过渡语句
    - 汇报完成后，立即调用handoff工具，不要等待或添加额外文本
    """
)

planner = AssistantAgent(
    "planner",
    model_client=model_client,
    handoffs=["data_collector", "data_agent", "web_search_agent", "visualization_agent", "writer"],
    system_message="""你是财务报表分析系统的总规划师，负责指挥整个分析流程。

    【核心职责】：
    1. 智能需求识别：分析用户问题需要什么类型的数据
    2. 流程控制：按正确顺序调用专家智能体
    3. 状态管理：根据数据可用性调整流程

    【重要信息提取规则】：
    在每条指令中必须明确包含：
    1. 公司名：[从用户问题中提取的公司名称]
    2. 年份：[从用户问题中提取的年份]
    示例：用户说"分析华为2023年的财务状况" → 公司=华为，年份=2023
    
    【需求类型识别规则】：
    分析用户问题，判断需要哪些数据：
    1. 财务数据需求：当问题涉及财务指标、数字、业绩、利润、营收、增长率等
       - 标志词：收入、利润、毛利率、ROE、EPS、财务数据、业绩、增长
       - 示例："华为2023年的营收是多少？" → 需要财务数据
       - 示例："华为近些年的主要财务数据分析" → 需要财务数据
       
    2. 文本分析需求：当问题涉及文本内容、管理层观点、战略、风险、讨论、展望等
       - 标志词：管理层、行业、观点、战略、风险、展望、讨论、分析、评述
       - 示例："华为的管理层对未来有什么展望？" → 需要文本分析
       - 示例："从行业的视角看华为的未来规划是什么？"→ 需要文本分析
       
    3. 综合需求：既需要财务数据也需要文本分析

    【标准工作流程 - 严格按此顺序】：
    步骤1: 数据准备判断
    - 根据上下文判断是否需要数据采集，只要用户的提问中涉及新的公司都必须进行数据采集 → 如果需要，handoff_to_data_collector
    - 如果已有数据或不需要采集 → 直接到步骤2
    
    步骤2: 本地数据分析
    - 根据需求类型指导data_agent：
      a) 如果只需要财务数据 → "data_agent，用户需要获取{公司}{年份}年的财务数据"
      b) 如果只需要文本分析 → "data_agent，用户需要分析{公司}{年份}年的文本内容"
      c) 如果需要两者 → "data_agent，用户需要综合分析{公司}{年份}年的财务和文本数据"
    - 等待data_agent汇报结果
    
    步骤3: 数据完整性检查
    - 如果data_agent报告数据完整满足需求 → 跳转到步骤5
    - 如果data_agent报告数据缺失 → 执行步骤4
    
    步骤4: 网络数据补充
    - handoff_to_web_search_agent (搜索公开信息)
    
    步骤5: 可视化处理
    - 如果用户没有明确指出需要“画图”“可视化分析”等 → 跳转到步骤6
    - 如果用户明确指出需要可视化处理 → handoff_to_visualization_agent
    
    步骤6: 报告生成
    将步骤2和步骤4获得的所有数据明确传给writer，并让其生成回答
    - handoff_to_writer

    【给各智能体的指令格式 - 必须包含公司名和年份】：
    1. 给data_collector：
       "data_collector，请采集{公司}{年份}年年报数据。目标：{公司}，年份：{年份}"
    
    2. 给data_agent：
       "data_agent，用户需要提取{公司}{年份}年的{需求类型}数据。目标：{公司}，年份：{年份}，需求：{具体需求}"
    
    3. 给web_search_agent：
       "web_search_agent，请搜索{公司}{年份}年相关市场信息。关键词：{具体关键词}"
    
    4. 给visualization_agent：
       "visualization_agent，请为{公司}{年份}年数据生成图表。数据类型：{图表类型}"
    
    5. 给writer：
       "writer，请基于{公司}{年份}年数据生成用户问题的回答。数据内容：{数据}{文本}"

    【重要规则】：
    - 每次指令必须明确包含公司名和年份
    - 每次决策前，查看历史对话上下文
    - 每次回答在有足够的信息后必须传给writer，请务必等待writer执行完成，才能说"TASK_DONE"
    - 严格按流程执行，不要跳过步骤
    - 明确告诉data_agent需要什么类型的数据
    - 请等待其他智能体执行完成后再进行下一步

    【强制要求】
    - 请控制和智能体之间对话发生的次数，一旦当前任务完成，请立即结束任务，说"TASK_DONE"
    """
)

web_search_agent = AssistantAgent(
    "web_search_agent",
    model_client=model_client,
    handoffs=["planner", "writer"],
    tools=[search_market_info],
    system_message="你是实时财务新闻信息分析师。调用search_market_info工具搜索信息，并汇报给planner。"
)

visualization_agent = AssistantAgent(
    "visualization_agent",
    model_client=model_client,
    handoffs=["planner", "writer"],
    tools=[generate_chart],
    system_message="你是财务信息可视化专家。根据数据和需求调用generate_chart工具生成图表链接后汇报给planner。"
)

writer = AssistantAgent(
    "writer",
    model_client=model_client,
    handoffs=["planner"],
    system_message="""你是报告撰写人。汇总所有专家的信息，特别注意：
    
    【报告要求】
    1. 注明数据来源（本地PDF分析/数据库/网络搜索）
    2. 突出基于本地数据的新发现
    3. 结构化呈现财务指标，并对公司经营、财务指标变化趋势等方面进行深入分析
    4. 如果信息较多，请使用format_report工具格式化
    5. 生成回答后请展示给用户看（这是最重要的！！）
    6. 一旦展示了回答之后马上告诉planner任务完成了！！
    
    完成后务必通知planner任务完成。
    
    【重要规则】
    1. 请完成回答的撰写后立即向planner汇报让其结束任务，控制整体的对话次数。
    2. 报告必须完整显示给用户，不要省略内容
    3. 永远不能回复"TASK_DONE" 给用户
    """
)

# ==================== 主逻辑 ====================
class FinancialAnalysisSystem:
    def __init__(self):
        self.memory = ListMemory()
        self.data_collection_status = {}  # 记录各公司的数据采集状态
        self.termination = TextMentionTermination("TASK_DONE") 
        self.team = Swarm(
            participants=[
                planner, 
                data_collector,  # 新增的数据采集器
                data_agent, 
                web_search_agent, 
                visualization_agent, 
                writer
            ],
            termination_condition=self.termination
        )
        
        # 创建必要的目录
        os.makedirs("./user_uploads", exist_ok=True)
        os.makedirs("./local_data", exist_ok=True)

    async def run_turn(self, user_input: str):
        # 1. 构建包含上下文的提示
        history = self.memory.get_context()
        
        # 2. 添加数据采集状态信息
        collection_status_str = "【各公司数据采集状态】:\n"
        for key, status in self.data_collection_status.items():
            collection_status_str += f"- {key}: {'已采集' if status else '未采集'}\n"
        if not self.data_collection_status:
            collection_status_str += "尚无数据采集记录\n"
        
        # 3. 分析用户需求类型
        user_input_lower = user_input.lower()
        
        finance_keywords = ["收入", "利润", "财务", "业绩", "毛利率", "roe", "eps", "增长", "营收", "盈利", "指标"]
        text_keywords = ["管理层", "观点", "战略", "风险", "展望", "讨论", "分析", "评述", "说明", "报告", "内容"]
        
        has_finance_need = any(keyword in user_input_lower for keyword in finance_keywords)
        has_text_need = any(keyword in user_input_lower for keyword in text_keywords)
        
        need_analysis = ""
        if has_finance_need and has_text_need:
            need_analysis = "【需求分析】: 用户需要综合财务数据和文本分析。"
        elif has_finance_need:
            need_analysis = "【需求分析】: 用户主要需要财务数据。"
        elif has_text_need:
            need_analysis = "【需求分析】: 用户主要需要文本分析（管理层观点等）。"
        else:
            need_analysis = "【需求分析】: 无法确定具体需求类型，请根据上下文判断。"
        
        full_prompt = f"""
        【历史对话上下文】:
        {history}
        
        {collection_status_str}
        
        {need_analysis}
        
        【当前用户指令】: {user_input}
        
        请作为总规划师，分析用户需求并指挥团队工作。
        
        【特别提醒】:
        1. 首先判断用户需要什么类型的数据（财务数据/文本分析/两者都需要）
        2. 根据需求类型给data_agent明确的指令
        3. 如果用户询问具体公司的财务分析，请先判断是否需要调用数据采集器
        4. 按照标准流程指挥：数据准备 → 数据提取 → 市场信息 → 可视化 → 报告生成
        """
        
        # 存储用户输入
        self.memory.add(user_input, "User")
        
        last_response = ""
        last_planner_message = ""
        
        # 3. 运行对话流
        print(f"\n{'='*10} 系统开始思考 {'='*10}")
        print(f"📋 需求分析: {need_analysis}")
        
        async for msg in self.team.run_stream(task=full_prompt):
            if isinstance(msg, TextMessage):
                print(f"\n🗣️  [{msg.source}]: {msg.content}")
                last_response = msg.content
                
                # 智能检测数据采集完成并更新状态
                if msg.source == "data_collector":
                    content = msg.content.lower()
                    if "华为" in content and "2023" in content and "完成" in content:
                        key = "华为_2023"
                        self.data_collection_status[key] = True
                        print(f"✅ 系统自动记录: {key} 数据采集完成")
                    elif "腾讯" in content and "完成" in content:
                        for year in ["2024", "2023", "2022"]:
                            if year in content:
                                key = f"腾讯_{year}"
                                self.data_collection_status[key] = True
                                print(f"✅ 系统自动记录: {key} 数据采集完成")
                
                if msg.source == "planner":
                    last_planner_message = msg.content
        
        print(f"\n{'='*10} 本轮结束 {'='*10}")
        
        # 4. 存储非终止的系统回复
        if last_response and not self.memory._contains_termination(last_response):
            useful_content = self._extract_useful_content(last_response)
            if useful_content:
                self.memory.add(useful_content, "System")
                print(f"📝 已将系统回复存入记忆")

    def _extract_useful_content(self, content: str) -> str:
        """从可能包含终止标记的消息中提取有用内容"""
        if not content:
            return ""
        
        if "TASK_DONE" in content.upper():
            sentences = content.split('。')
            useful_sentences = []
            
            for sentence in sentences:
                if "TASK_DONE" not in sentence.upper():
                    useful_sentences.append(sentence.strip())
            
            if useful_sentences:
                return '。'.join(useful_sentences) + ('。' if useful_sentences else '')
        
        return content

# ==================== 启动入口 ====================

async def main():
    print("\n💰 金融多智能体分析系统 v4.0（工具化架构）已启动")
    print("=" * 50)
    print("🎯 新架构特性:")
    print("   - data_agent直接调用工具函数")
    print("   - 财务和文本数据提取内嵌在工具中")
    print("   - 更简洁的工作流程")
    print("=" * 50)
    
    # 测试LLM连接
    if not await test_llm():
        print("❌ LLM连接失败，请检查配置")
        return
    
    system = FinancialAnalysisSystem()

    while True:
        try:
            user_input = input("\n👤 请输入指令: ").strip()
            if not user_input: 
                continue
            if user_input.lower() in ["exit", "quit", "退出"]: 
                break

            await system.run_turn(user_input)
            
        except KeyboardInterrupt:
            print("\n程序已停止")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            import traceback
            traceback.print_exc()
