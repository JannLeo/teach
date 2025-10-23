"""AI决策模块

基于LLM的交易决策引擎，使用DeepSeek API进行智能决策
"""

import asyncio
import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import numpy as np

from utils.logger import logger
from utils.config_loader import config_loader


class AIDecisionModule:
    """AI决策模块"""
    
    def __init__(self):
        """初始化AI决策模块"""
        self.api_key = config_loader.get('ai_model.api_key')
        self.model_name = config_loader.get('ai_model.model_name', 'deepseek-chat')
        self.api_url = self._get_api_url()
        self.decision_history = []
        
        # 决策模板和规则
        self.decision_template = self._load_decision_template()
        self.trading_rules = self._load_trading_rules()
        
    def _get_api_url(self) -> str:
        """获取API URL
        
        Returns:
            API URL字符串
        """
        provider = config_loader.get('ai_model.provider', 'deepseek')
        
        if provider == 'deepseek':
            return "https://api.deepseek.com/v1/chat/completions"
        elif provider == 'openai':
            return "https://api.openai.com/v1/chat/completions"
        else:
            return "https://api.deepseek.com/v1/chat/completions"
            
    def _load_decision_template(self) -> Dict[str, str]:
        """加载决策模板
        
        Returns:
            决策模板字典
        """
        return {
            'system_prompt': """
你是一个专业的加密货币交易分析师，负责基于市场数据做出交易决策。

你的任务是：
1. 分析提供的市场数据和特征
2. 评估当前市场状况和风险
3. 做出买入、卖出或持有的决策
4. 提供决策的理由和置信度

决策原则：
- 优先考虑风险管理，保护资本安全
- 基于技术分析和市场情绪综合判断
- 考虑流动性和市场深度
- 避免过度交易

请以JSON格式输出决策结果，包含以下字段：
{
    "decision": "buy|sell|hold",
    "confidence": 0.0-1.0,
    "reasoning": "决策理由",
    "risk_level": "low|medium|high",
    "position_size": 0.0-1.0,
    "stop_loss": 价格或百分比,
    "take_profit": 价格或百分比
}
""",
            'user_prompt_template': """
请基于以下市场数据做出交易决策：

交易对: {symbol}
当前时间: {timestamp}

市场特征:
{features}

技术分析:
{technical_analysis}

市场情绪:
{market_sentiment}

请提供详细的交易决策分析。
"""
        }
        
    def _load_trading_rules(self) -> Dict[str, Any]:
        """加载交易规则
        
        Returns:
            交易规则字典
        """
        return {
            'max_daily_trades': 10,
            'min_confidence_threshold': 0.6,
            'max_position_size': config_loader.get('risk_management.max_position_size', 0.1),
            'stop_loss_percentage': config_loader.get('risk_management.stop_loss_percentage', 0.05),
            'take_profit_percentage': config_loader.get('risk_management.take_profit_percentage', 0.1),
            'prohibited_conditions': [
                'high_volatility_no_stop_loss',
                'low_liquidity_large_position',
                'contrary_trend_signal'
            ]
        }
        
    async def make_trading_decision(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """做出交易决策
        
        Args:
            features: 市场特征数据
            
        Returns:
            交易决策字典
        """
        try:
            symbol = features.get('symbol', 'unknown')
            logger.info(f"开始为 {symbol} 做出交易决策")
            
            # 准备决策输入
            decision_input = self._prepare_decision_input(features)
            
            # 调用AI模型
            ai_response = await self._call_ai_model(decision_input)
            
            # 解析和验证决策
            validated_decision = self._validate_decision(ai_response, features)
            
            # 记录决策历史
            self._record_decision(features, validated_decision)
            
            logger.info(f"交易决策完成: {validated_decision.get('decision', 'unknown')}")
            return validated_decision
            
        except Exception as e:
            logger.error(f"交易决策错误: {e}")
            # 返回默认的持有决策
            return self._get_default_decision(features)
            
    def _prepare_decision_input(self, features: Dict[str, Any]) -> Dict[str, str]:
        """准备决策输入数据
        
        Args:
            features: 市场特征
            
        Returns:
            格式化的输入数据
        """
        # 技术分析总结
        technical_analysis = self._generate_technical_summary(features)
        
        # 市场情绪分析
        market_sentiment = self._generate_sentiment_summary(features)
        
        # 格式化特征
        formatted_features = self._format_features(features)
        
        return {
            'symbol': features.get('symbol', 'unknown'),
            'timestamp': features.get('timestamp', ''),
            'features': formatted_features,
            'technical_analysis': technical_analysis,
            'market_sentiment': market_sentiment
        }
        
    def _generate_technical_summary(self, features: Dict[str, Any]) -> str:
        """生成技术分析总结
        
        Args:
            features: 市场特征
            
        Returns:
            技术分析文本
        """
        summary_parts = []
        
        # 价格分析
        if 'current_price' in features:
            summary_parts.append(f"当前价格: {features['current_price']:.2f}")
            
        if 'price_change_1m' in features:
            change_1m = features['price_change_1m'] * 100
            summary_parts.append(f"1分钟变化: {change_1m:.2f}%")
            
        if 'price_change_5m' in features:
            change_5m = features['price_change_5m'] * 100
            summary_parts.append(f"5分钟变化: {change_5m:.2f}%")
            
        # RSI指标
        if 'rsi' in features:
            rsi = features['rsi']
            summary_parts.append(f"RSI: {rsi:.2f}")
            if rsi > 70:
                summary_parts.append("RSI显示超买状态")
            elif rsi < 30:
                summary_parts.append("RSI显示超卖状态")
                
        # MACD指标
        if 'macd' in features and 'macd_signal' in features:
            macd = features['macd']
            macd_signal = features['macd_signal']
            summary_parts.append(f"MACD: {macd:.6f}, 信号线: {macd_signal:.6f}")
            
            if macd > macd_signal:
                summary_parts.append("MACD金叉，可能看涨")
            else:
                summary_parts.append("MACD死叉，可能看跌")
                
        # 布林带
        if 'bollinger_upper' in features and 'bollinger_lower' in features:
            upper = features['bollinger_upper']
            lower = features['bollinger_lower']
            summary_parts.append(f"布林带上轨: {upper:.2f}, 下轨: {lower:.2f}")
            
        return "; ".join(summary_parts)
        
    def _generate_sentiment_summary(self, features: Dict[str, Any]) -> str:
        """生成市场情绪总结
        
        Args:
            features: 市场特征
            
        Returns:
            市场情绪文本
        """
        summary_parts = []
        
        # 订单簿不平衡
        if 'order_book_imbalance' in features:
            imbalance = features['order_book_imbalance']
            if imbalance > 0.2:
                summary_parts.append("买盘压力较强")
            elif imbalance < -0.2:
                summary_parts.append("卖盘压力较强")
            else:
                summary_parts.append("买卖盘相对平衡")
                
        # 聪明钱信号
        if 'smart_money_net_pressure' in features:
            net_pressure = features['smart_money_net_pressure']
            if net_pressure > 0:
                summary_parts.append(f"聪明钱净流入: {net_pressure:.0f}")
            elif net_pressure < 0:
                summary_parts.append(f"聪明钱净流出: {abs(net_pressure):.0f}")
                
        # 热门程度
        if 'trending_score' in features:
            trending_score = features['trending_score']
            if trending_score > 5:
                summary_parts.append("市场关注度较高")
            elif trending_score < 2:
                summary_parts.append("市场关注度较低")
                
        return "; ".join(summary_parts)
        
    def _format_features(self, features: Dict[str, Any]) -> str:
        """格式化特征数据
        
        Args:
            features: 特征字典
            
        Returns:
            格式化的特征文本
        """
        formatted_lines = []
        
        for key, value in features.items():
            if isinstance(value, float):
                if abs(value) < 0.01:
                    formatted_lines.append(f"{key}: {value:.6f}")
                else:
                    formatted_lines.append(f"{key}: {value:.4f}")
            else:
                formatted_lines.append(f"{key}: {value}")
                
        return "\n".join(formatted_lines)
        
    async def _call_ai_model(self, decision_input: Dict[str, str]) -> Dict[str, Any]:
        """调用AI模型
        
        Args:
            decision_input: 决策输入数据
            
        Returns:
            AI模型响应
        """
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            
            # 构建消息
            messages = [
                {
                    "role": "system",
                    "content": self.decision_template['system_prompt']
                },
                {
                    "role": "user",
                    "content": self.decision_template['user_prompt_template'].format(
                        symbol=decision_input['symbol'],
                        timestamp=decision_input['timestamp'],
                        features=decision_input['features'],
                        technical_analysis=decision_input['technical_analysis'],
                        market_sentiment=decision_input['market_sentiment']
                    )
                }
            ]
            
            payload = {
                'model': self.model_name,
                'messages': messages,
                'max_tokens': config_loader.get('ai_model.max_tokens', 2000),
                'temperature': config_loader.get('ai_model.temperature', 0.1),
                'response_format': {'type': 'json_object'}
            }
            
            # 模拟API调用（实际使用时取消注释）
            """
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result['choices'][0]['message']['content']
                        return json.loads(content)
                    else:
                        logger.error(f"AI API调用失败: {response.status}")
                        return {}
            """
            
            # 模拟返回（实际使用时删除）
            return await self._simulate_ai_decision(decision_input)
            
        except Exception as e:
            logger.error(f"AI模型调用错误: {e}")
            return {}
            
    async def _simulate_ai_decision(self, decision_input: Dict[str, str]) -> Dict[str, Any]:
        """模拟AI决策（用于测试）
        
        Args:
            decision_input: 决策输入
            
        Returns:
            模拟的AI决策
        """
        # 模拟基于特征的简单决策逻辑
        features = decision_input['features']
        
        # 默认决策
        decision = 'hold'
        confidence = 0.5
        reasoning = "基于当前市场条件分析"
        
        # 简单的决策逻辑
        if 'rsi' in features and 'price_change_1m' in features:
            rsi = 50  # 默认值
            change_1m = 0  # 默认值
            
            # 从文本中提取数值
            import re
            rsi_match = re.search(r'rsi:\s*(\d+\.?\d*)', features.lower())
            if rsi_match:
                rsi = float(rsi_match.group(1))
                
            change_match = re.search(r'price_change_1m:\s*(-?\d+\.?\d*)', features.lower())
            if change_match:
                change_1m = float(change_match.group(1))
                
            # 超卖反弹
            if rsi < 30 and change_1m > -0.01:
                decision = 'buy'
                confidence = 0.7
                reasoning = "RSI超卖区域，可能出现反弹"
                
            # 超买回调
            elif rsi > 70 and change_1m < 0.01:
                decision = 'sell'
                confidence = 0.7
                reasoning = "RSI超买区域，可能出现回调"
                
            # 强势上涨
            elif change_1m > 0.02:
                decision = 'buy'
                confidence = 0.6
                reasoning = "短期强势上涨"
                
            # 大幅下跌
            elif change_1m < -0.02:
                decision = 'sell'
                confidence = 0.6
                reasoning = "短期大幅下跌"
                
        await asyncio.sleep(1)  # 模拟API延迟
        
        return {
            'decision': decision,
            'confidence': confidence,
            'reasoning': reasoning,
            'risk_level': 'medium',
            'position_size': 0.1 if decision != 'hold' else 0.0,
            'stop_loss': 0.05,
            'take_profit': 0.1
        }
        
    def _validate_decision(self, ai_response: Dict[str, Any], features: Dict[str, Any]) -> Dict[str, Any]:
        """验证和修正AI决策
        
        Args:
            ai_response: AI模型响应
            features: 市场特征
            
        Returns:
            验证后的决策
        """
        validated = ai_response.copy()
        
        # 验证决策类型
        decision = ai_response.get('decision', 'hold')
        if decision not in ['buy', 'sell', 'hold']:
            logger.warning(f"无效的决策类型: {decision}")
            validated['decision'] = 'hold'
            
        # 验证置信度
        confidence = ai_response.get('confidence', 0.5)
        if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
            logger.warning(f"无效的置信度: {confidence}")
            validated['confidence'] = 0.5
            
        # 验证仓位大小
        position_size = ai_response.get('position_size', 0)
        max_position = self.trading_rules['max_position_size']
        if position_size > max_position:
            logger.warning(f"仓位大小超过限制: {position_size} > {max_position}")
            validated['position_size'] = max_position
            
        # 应用风险管理规则
        risk_score = features.get('overall_risk_score', 0)
        if risk_score > 0.7 and validated['decision'] != 'hold':
            logger.warning("风险评分过高，建议持有")
            validated['decision'] = 'hold'
            validated['reasoning'] = f"风险评分过高({risk_score:.2f})，执行保守策略"
            
        # 确保有止损和止盈设置
        if validated['decision'] != 'hold':
            if 'stop_loss' not in validated:
                validated['stop_loss'] = self.trading_rules['stop_loss_percentage']
            if 'take_profit' not in validated:
                validated['take_profit'] = self.trading_rules['take_profit_percentage']
                
        return validated
        
    def _get_default_decision(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """获取默认决策（错误时返回）
        
        Args:
            features: 市场特征
            
        Returns:
            默认决策
        """
        return {
            'decision': 'hold',
            'confidence': 0.0,
            'reasoning': "系统错误，执行默认持有策略",
            'risk_level': 'high',
            'position_size': 0.0,
            'stop_loss': self.trading_rules['stop_loss_percentage'],
            'take_profit': self.trading_rules['take_profit_percentage']
        }
        
    def _record_decision(self, features: Dict[str, Any], decision: Dict[str, Any]):
        """记录决策历史
        
        Args:
            features: 市场特征
            decision: 交易决策
        """
        record = {
            'timestamp': datetime.now().isoformat(),
            'symbol': features.get('symbol', 'unknown'),
            'features': features,
            'decision': decision
        }
        
        self.decision_history.append(record)
        
        # 限制历史记录大小
        if len(self.decision_history) > 1000:
            self.decision_history = self.decision_history[-500:]
            
    def get_decision_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取决策历史
        
        Args:
            limit: 历史记录限制
            
        Returns:
            决策历史列表
        """
        return self.decision_history[-limit:]
        
    def get_trading_statistics(self) -> Dict[str, Any]:
        """获取交易统计
        
        Returns:
            交易统计字典
        """
        if not self.decision_history:
            return {}
            
        total_decisions = len(self.decision_history)
        buy_decisions = sum(1 for d in self.decision_history if d['decision']['decision'] == 'buy')
        sell_decisions = sum(1 for d in self.decision_history if d['decision']['decision'] == 'sell')
        hold_decisions = sum(1 for d in self.decision_history if d['decision']['decision'] == 'hold')
        
        avg_confidence = np.mean([
            d['decision']['confidence'] for d in self.decision_history 
            if 'confidence' in d['decision']
        ])
        
        return {
            'total_decisions': total_decisions,
            'buy_decisions': buy_decisions,
            'sell_decisions': sell_decisions,
            'hold_decisions': hold_decisions,
            'average_confidence': avg_confidence,
            'buy_ratio': buy_decisions / total_decisions if total_decisions > 0 else 0,
            'sell_ratio': sell_decisions / total_decisions if total_decisions > 0 else 0,
            'hold_ratio': hold_decisions / total_decisions if total_decisions > 0 else 0
        }