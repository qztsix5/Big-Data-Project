"""
Configuration loader for the financial report analysis system.
"""
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for loading and accessing system settings."""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize configuration from YAML file."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> dict:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def get(self, key: str, default=None):
        """Get configuration value by key."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    @property
    def llm_config(self) -> dict:
        """Get LLM configuration."""
        return {
            "model": self.get("llm.model", "gpt-4"),
            "temperature": self.get("llm.temperature", 0.7),
            "max_tokens": self.get("llm.max_tokens", 2000),
            "timeout": self.get("llm.timeout", 60),
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    
    @property
    def agent_config(self) -> dict:
        """Get agent configuration."""
        return {
            "max_consecutive_auto_reply": self.get("agent.max_consecutive_auto_reply", 10),
            "human_input_mode": self.get("agent.human_input_mode", "NEVER"),
            "code_execution_config": self.get("agent.code_execution_config", False),
        }
    
    @property
    def core_metrics(self) -> list:
        """Get list of core financial metrics."""
        return self.get("metrics.core", [])


# Global configuration instance
config = Config()
