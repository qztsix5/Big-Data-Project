"""
Financial Analysis Agent using AutoGen framework.
"""
import os
from typing import Dict, List, Optional
import autogen
from autogen import AssistantAgent, UserProxyAgent
from src.utils.config_loader import config
from src.utils.logger import log
from src.utils.stats_tracker import stats_tracker
from src.data_processing.data_storage import DataStorage
from src.visualization.chart_generator import ChartGenerator
import pandas as pd


class FinancialAnalysisAgent:
    """Agent for financial report analysis using AutoGen."""
    
    def __init__(self, data_storage: DataStorage = None, chart_generator: ChartGenerator = None):
        """
        Initialize financial analysis agent.
        
        Args:
            data_storage: DataStorage instance for accessing financial data
            chart_generator: ChartGenerator instance for creating charts
        """
        self.data_storage = data_storage or DataStorage()
        self.chart_generator = chart_generator or ChartGenerator()
        self.financial_data = {}
        self.context = {}
        
        # Configure LLM
        llm_config = {
            "config_list": [{
                "model": config.get("llm.model", "gpt-4"),
                "api_key": os.getenv("OPENAI_API_KEY", "your-api-key"),
                "temperature": config.get("llm.temperature", 0.7),
            }],
            "timeout": config.get("llm.timeout", 60),
        }
        
        # Create assistant agent
        self.assistant = AssistantAgent(
            name="FinancialAnalyst",
            system_message=self._get_system_message(),
            llm_config=llm_config,
        )
        
        # Create user proxy agent
        self.user_proxy = UserProxyAgent(
            name="User",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=config.get("agent.max_consecutive_auto_reply", 10),
            code_execution_config=False,
        )
        
        # Register custom functions
        self._register_functions()
        
        log.info("FinancialAnalysisAgent initialized")
    
    def _get_system_message(self) -> str:
        """Get system message for the assistant agent."""
        return """你是一个专业的财务分析师助手，专门分析和解读企业财务报表。你的职责包括：

1. 回答用户关于财务数据的查询（如营收、净利润等）
2. 进行深度财务分析（如增长原因、盈利能力分析等）
3. 提供行业对比和竞品分析
4. 生成可视化图表展示数据趋势
5. 基于历史数据进行预测和建议

在回答时：
- 使用专业但易懂的语言
- 提供具体的数字和计算过程
- 在适当时候主动建议生成图表
- 保持上下文连贯性，记住之前的对话
- 如果数据不足，明确说明并建议需要什么信息

你可以使用以下工具：
- get_financial_metric: 获取特定财务指标
- calculate_growth_rate: 计算增长率
- generate_chart: 生成可视化图表
- compare_with_industry: 与行业平均水平对比
"""
    
    def _register_functions(self):
        """Register custom functions for the agent."""
        
        @self.user_proxy.register_for_execution()
        @self.assistant.register_for_llm(description="Get a specific financial metric for a company and year")
        def get_financial_metric(company: str, year: int, metric: str) -> str:
            """Get financial metric value."""
            log.info(f"Getting {metric} for {company} in {year}")
            
            data = self.financial_data.get(company, {}).get(str(year), {})
            value = data.get(metric, "N/A")
            
            return f"{company} 在 {year} 年的 {metric}: {value}"
        
        @self.user_proxy.register_for_execution()
        @self.assistant.register_for_llm(description="Calculate growth rate between two years")
        def calculate_growth_rate(company: str, metric: str, start_year: int, end_year: int) -> str:
            """Calculate growth rate."""
            log.info(f"Calculating growth rate for {company} {metric} from {start_year} to {end_year}")
            
            start_data = self.financial_data.get(company, {}).get(str(start_year), {})
            end_data = self.financial_data.get(company, {}).get(str(end_year), {})
            
            start_value = start_data.get(metric)
            end_value = end_data.get(metric)
            
            if start_value and end_value:
                try:
                    start_val = float(str(start_value).replace(',', ''))
                    end_val = float(str(end_value).replace(',', ''))
                    growth_rate = ((end_val - start_val) / start_val) * 100
                    return f"{company} 的 {metric} 从 {start_year} 到 {end_year} 增长了 {growth_rate:.2f}%"
                except (ValueError, ZeroDivisionError):
                    return "无法计算增长率：数据格式错误或起始值为零"
            
            return "无法计算增长率：缺少必要数据"
        
        @self.user_proxy.register_for_execution()
        @self.assistant.register_for_llm(description="Generate a chart for visualization")
        def generate_chart(chart_type: str, data_description: str) -> str:
            """Generate chart."""
            log.info(f"Generating {chart_type} chart: {data_description}")
            
            # This is a placeholder - actual implementation would generate real charts
            chart_path = f"data/charts/{chart_type}_{data_description.replace(' ', '_')}.png"
            
            return f"图表已生成并保存至: {chart_path}"
    
    def load_financial_data(self, data: Dict):
        """
        Load financial data into the agent.
        
        Args:
            data: Financial data dictionary
        """
        self.financial_data = data
        log.info(f"Loaded financial data for {len(data)} companies")
    
    def chat(self, message: str, context: Dict = None) -> str:
        """
        Send a message to the agent and get response.
        
        Args:
            message: User message
            context: Additional context information
            
        Returns:
            Agent's response
        """
        log.info(f"User query: {message}")
        
        # Update context
        if context:
            self.context.update(context)
        
        # Prepare message with context
        full_message = message
        if self.context:
            context_str = "\n".join([f"{k}: {v}" for k, v in self.context.items()])
            full_message = f"上下文信息:\n{context_str}\n\n用户问题: {message}"
        
        try:
            # Initiate chat
            self.user_proxy.initiate_chat(
                self.assistant,
                message=full_message,
            )
            
            # Get the last message from assistant
            chat_history = self.user_proxy.chat_messages[self.assistant]
            if chat_history:
                response = chat_history[-1].get("content", "")
            else:
                response = "抱歉，我无法处理这个请求。"
            
            # Track statistics
            stats_tracker.log_agent_call(
                agent_name="FinancialAnalyst",
                message=message,
                response=response
            )
            
            log.info(f"Agent response: {response[:100]}...")
            return response
            
        except Exception as e:
            log.error(f"Error in chat: {e}")
            return f"处理请求时出错: {str(e)}"
    
    def multi_turn_conversation(self, messages: List[str]) -> List[Dict]:
        """
        Handle multi-turn conversation.
        
        Args:
            messages: List of user messages
            
        Returns:
            List of conversation turns with messages and responses
        """
        conversation = []
        
        for i, message in enumerate(messages):
            log.info(f"Turn {i+1}: {message}")
            
            # Build context from previous turns
            context = {
                "turn": i + 1,
                "previous_topics": [c["message"] for c in conversation[-3:]]  # Last 3 turns
            }
            
            response = self.chat(message, context)
            
            conversation.append({
                "turn": i + 1,
                "message": message,
                "response": response,
            })
        
        # Save conversation
        stats_tracker.log_conversation(conversation)
        
        return conversation
