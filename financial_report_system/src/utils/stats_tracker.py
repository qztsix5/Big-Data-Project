"""
Statistics tracker for agent calls and token usage.
"""
from typing import Dict, List
from datetime import datetime
import json
from pathlib import Path


class StatisticsTracker:
    """Track agent calls, token usage, and other metrics."""
    
    def __init__(self):
        """Initialize statistics tracker."""
        self.stats = {
            "total_agent_calls": 0,
            "total_tokens": 0,
            "conversations": [],
            "queries": [],
            "start_time": datetime.now().isoformat(),
        }
        
    def log_agent_call(self, agent_name: str, message: str, response: str, tokens: int = 0):
        """
        Log an agent call.
        
        Args:
            agent_name: Name of the agent
            message: Input message
            response: Agent response
            tokens: Estimated tokens used
        """
        self.stats["total_agent_calls"] += 1
        self.stats["total_tokens"] += tokens if tokens > 0 else len(message) + len(response)
        
        self.stats["queries"].append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "message_length": len(message),
            "response_length": len(response),
            "tokens": tokens if tokens > 0 else len(message) + len(response)
        })
    
    def log_conversation(self, conversation: List[Dict]):
        """
        Log a complete conversation.
        
        Args:
            conversation: List of conversation messages
        """
        self.stats["conversations"].append({
            "timestamp": datetime.now().isoformat(),
            "messages": conversation,
            "num_turns": len(conversation)
        })
    
    def get_summary(self) -> Dict:
        """Get statistics summary."""
        return {
            "total_agent_calls": self.stats["total_agent_calls"],
            "total_tokens": self.stats["total_tokens"],
            "total_conversations": len(self.stats["conversations"]),
            "total_queries": len(self.stats["queries"]),
            "average_tokens_per_call": self.stats["total_tokens"] / max(self.stats["total_agent_calls"], 1),
            "start_time": self.stats["start_time"],
            "end_time": datetime.now().isoformat()
        }
    
    def save_stats(self, filepath: str = "logs/statistics.json"):
        """
        Save statistics to file.
        
        Args:
            filepath: Path to save statistics
        """
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "summary": self.get_summary(),
                "details": self.stats
            }, f, indent=2, ensure_ascii=False)


# Global statistics tracker
stats_tracker = StatisticsTracker()
