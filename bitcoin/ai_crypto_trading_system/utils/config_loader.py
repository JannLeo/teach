"""配置文件加载器"""

import os
import yaml
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class ConfigLoader:
    """配置文件加载器类"""
    
    def __init__(self, config_path: str = None):
        """初始化配置加载器
        
        Args:
            config_path: 配置文件路径，如果为None则使用默认路径
        """
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'config',
                'config.yaml'
            )
        
        self.config_path = config_path
        self._config = None
        
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件
        
        Returns:
            配置字典
            
        Raises:
            FileNotFoundError: 配置文件不存在
            yaml.YAMLError: 配置文件格式错误
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                self._config = yaml.safe_load(file)
                
            logger.info(f"配置文件加载成功: {self.config_path}")
            return self._config
            
        except FileNotFoundError:
            logger.error(f"配置文件不存在: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"配置文件格式错误: {e}")
            raise
            
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值
        
        Args:
            key: 配置键，支持点分路径 (如 'system.name')
            default: 默认值
            
        Returns:
            配置值
        """
        if self._config is None:
            self.load_config()
            
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
            
    def get_trading_pairs(self) -> list:
        """获取交易对列表"""
        return self.get('trading.trading_pairs', [])
        
    def get_risk_parameters(self) -> Dict[str, Any]:
        """获取风险管理参数"""
        return self.get('risk_management', {})
        
    def get_ai_model_config(self) -> Dict[str, Any]:
        """获取AI模型配置"""
        return self.get('ai_model', {})


# 全局配置实例
config_loader = ConfigLoader()