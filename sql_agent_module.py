import sqlite3
import logging
from typing import Annotated
from autogen_agentchat.agents import AssistantAgent

# 配置日志
logger = logging.getLogger(__name__)

# ==================== 配置区域 ====================
# 这里配置您的真实数据库路径
# 假设您已经有了一个结构化的数据库文件
DB_PATH = "./local_data/financial.db" 

# ==================== 工具函数定义 ====================

def get_db_connection():
    """建立数据库连接 (私有辅助函数)"""
    # check_same_thread=False 是为了兼容多线程环境
    return sqlite3.connect(DB_PATH, check_same_thread=False)

async def list_tables() -> str:
    """
    [Tool] 列出数据库中所有的表名。
    Agent 在开始查询前必须先调用此工具了解数据库概况。
    """
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
    """
    [Tool] 获取指定表的 DDL (Create Table 语句)。
    Agent 在编写 SQL 之前必须调用此工具查看表结构，以确保字段名正确。
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        target_tables = [t.strip() for t in table_names.split(",")]
        
        schemas = []
        for table in target_tables:
            # SQLite 获取 DDL 的标准方式
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
    """
    [Tool] 执行 SQL 查询并返回结果。
    注意：为了安全，只允许执行 SELECT 语句。
    """
    # 1. 安全检查
    if not query.strip().lower().startswith("select"):
        return "⚠️ 安全警告: 本工具仅允许执行 SELECT 查询语句，禁止修改数据。"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print(f"\n   🔍 [SQL Agent] 执行查询: {query}")
        cursor.execute(query)
        
        # 2. 获取列名
        if cursor.description:
            column_names = [description[0] for description in cursor.description]
        else:
            column_names = []
            
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return "查询执行成功，但未返回任何结果 (Result set is empty)。"
            
        # 3. 格式化输出 (Markdown 表格格式，便于 LLM 理解)
        # 限制返回行数，防止 Token 爆炸
        MAX_ROWS = 20
        result_str = f"| {' | '.join(column_names)} |\n"
        result_str += f"| {' | '.join(['---']*len(column_names))} |\n"
        
        for i, row in enumerate(rows):
            if i >= MAX_ROWS:
                result_str += f"\n... (剩余 {len(rows)-MAX_ROWS} 行数据已省略，建议优化 SQL 添加 LIMIT) ..."
                break
            # 处理 None 值，转为字符串
            row_str = [str(val) if val is not None else "NULL" for val in row]
            result_str += f"| {' | '.join(row_str)} |\n"
            
        return result_str
        
    except sqlite3.Error as e:
        return f"❌ SQL 执行报错: {str(e)}"

# ==================== Agent 工厂函数 ====================

def create_sql_agent(model_client) -> AssistantAgent:
    """
    创建并返回配置好的 SQL Agent 实例。
    
    Args:
        model_client: 主程序中初始化的 LLM 客户端对象
    """
    
    # 定义 System Prompt
    system_message = """你是一个专业的 SQL 数据分析专家 (SQLite 方言)。
    你的唯一职责是准确地从结构化数据库中查询数据。
    
    【核心工作流】
    1. **List Tables**: 总是先调用 `list_tables` 查看有哪些表。
    2. **Get Schema**: 仔细分析用户问题涉及哪些表，调用 `get_table_schema` 获取它们的精确结构。严禁猜测字段名。
    3. **Query**: 编写并执行 SQL。
    
    【查询规范】
    - 使用 `execute_sql_query` 执行。
    - 只使用 SELECT 语句。
    - 如果查询涉及文本匹配，请优先使用 `LIKE` 进行模糊搜索 (例如 `name LIKE '%华为%'`)。
    - 如果需要聚合数据，请使用 `SUM`, `AVG`, `COUNT` 等函数。
    - 在回答中直接给出查询到的数据表格，不要只说“查询成功”。
    
    【错误处理】
    - 如果 SQL 报错，请分析错误信息，修正 SQL 后重试 (例如检查是否拼错了列名)。
    - 如果查不到数据，尝试放宽查询条件 (例如去掉某些 WHERE 子句) 再试一次。
    """

    agent = AssistantAgent(
        name="sql_expert",
        model_client=model_client,
        handoffs=["planner"], 
        tools=[list_tables, get_table_schema, execute_sql_query],
        system_message=system_message
    )
    
    return agent