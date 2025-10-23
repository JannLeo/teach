"""风险管理模块

负责风险评估、仓位管理和交易信号过滤
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

from utils.logger import logger
from utils.config_loader import config_loader


class RiskManagementModule:
    """风险管理模块"""
    
    def __init__(self):
        """初始化风险管理模块"""
        self.risk_parameters = config_loader.get_risk_parameters()
        self.position_tracker = {}  # 仓位跟踪
        self.daily_trades = {}  # 日交易计数
        self.daily_pnl = {}  # 日盈亏跟踪
        self.risk_metrics = {}  # 风险指标
        
        # 熔断机制
        self.circuit_breaker = {
            'enabled': True,
            'triggered': False,
            'trigger_time': None,
            'cooldown_hours': 24
        }
        
        # 风险限制
        self.risk_limits = {
            'max_daily_loss': self.risk_parameters.get('max_daily_loss', 0.02),
            'max_drawdown': self.risk_parameters.get('max_drawdown', 0.05),
            'max_position_size': self.risk_parameters.get('max_position_size', 0.1),
            'max_daily_trades': 10
        }
        
    async def evaluate_trading_signal(self, signal: Dict[str, Any], features: Dict[str, Any]) -> Dict[str, Any]:
        """评估交易信号的风险
        
        Args:
            signal: 交易信号
            features: 市场特征
            
        Returns:
            风险评估结果
        """
        try:
            symbol = signal.get('symbol', 'unknown')
            logger.info(f"开始评估 {symbol} 的交易信号风险")
            
            # 检查熔断机制
            if await self._check_circuit_breaker():
                return {
                    'approved': False,
                    'reason': '熔断机制已触发，暂停交易',
                    'risk_score': 1.0,
                    'modified_signal': None
                }
                
            # 执行风险评估
            risk_assessment = await self._perform_risk_assessment(signal, features)
            
            # 检查风险限制
            limit_check = await self._check_risk_limits(signal, features)
            
            # 综合评估结果
            final_decision = await self._make_final_decision(
                signal, risk_assessment, limit_check
            )
            
            logger.info(f"风险评估完成: {'通过' if final_decision['approved'] else '拒绝'}")
            return final_decision
            
        except Exception as e:
            logger.error(f"风险评估错误: {e}")
            return {
                'approved': False,
                'reason': f'风险评估错误: {str(e)}',
                'risk_score': 1.0,
                'modified_signal': None
            }
            
    async def _perform_risk_assessment(self, signal: Dict[str, Any], features: Dict[str, Any]) -> Dict[str, Any]:
        """执行风险评估
        
        Args:
            signal: 交易信号
            features: 市场特征
            
        Returns:
            风险评估结果
        """
        assessments = {}
        
        # 市场风险评估
        market_risk = await self._assess_market_risk(features)
        assessments['market_risk'] = market_risk
        
        # 流动性风险评估
        liquidity_risk = await self._assess_liquidity_risk(features)
        assessments['liquidity_risk'] = liquidity_risk
        
        # 波动性风险评估
        volatility_risk = await self._assess_volatility_risk(features)
        assessments['volatility_risk'] = volatility_risk
        
        # 集中风险评估
        concentration_risk = await self._assess_concentration_risk(signal)
        assessments['concentration_risk'] = concentration_risk
        
        # 时间风险评估
        timing_risk = await self._assess_timing_risk(features)
        assessments['timing_risk'] = timing_risk
        
        # 综合风险评分
        overall_risk = await self._calculate_overall_risk(assessments)
        assessments['overall_risk'] = overall_risk
        
        return assessments
        
    async def _assess_market_risk(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """评估市场风险
        
        Args:
            features: 市场特征
            
        Returns:
            市场风险评估结果
        """
        risk_score = 0.0
        risk_factors = []
        
        # 基于RSI的市场风险
        if 'rsi' in features:
            rsi = features['rsi']
            if rsi > 80 or rsi < 20:
                risk_score += 0.3
                risk_factors.append(f"极端RSI值: {rsi:.2f}")
            elif rsi > 70 or rsi < 30:
                risk_score += 0.15
                risk_factors.append(f"超买超卖RSI: {rsi:.2f}")
                
        # 基于价格波动率的风险
        if 'price_volatility' in features:
            volatility = features['price_volatility']
            if volatility > 0.1:  # 10%波动率
                risk_score += 0.4
                risk_factors.append(f"高波动率: {volatility:.3f}")
            elif volatility > 0.05:  # 5%波动率
                risk_score += 0.2
                risk_factors.append(f"中等波动率: {volatility:.3f}")
                
        # 基于趋势的风险
        if 'price_change_15m' in features:
            change_15m = abs(features['price_change_15m'])
            if change_15m > 0.05:  # 5%变化
                risk_score += 0.25
                risk_factors.append(f"大幅价格变化: {change_15m:.3f}")
                
        return {
            'score': min(risk_score, 1.0),
            'factors': risk_factors,
            'level': 'high' if risk_score > 0.6 else 'medium' if risk_score > 0.3 else 'low'
        }
        
    async def _assess_liquidity_risk(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """评估流动性风险
        
        Args:
            features: 市场特征
            
        Returns:
            流动性风险评估结果
        """
        risk_score = 0.0
        risk_factors = []
        
        # 基于买卖价差的风险
        if 'spread_percentage' in features:
            spread_pct = features['spread_percentage']
            if spread_pct > 0.01:  # 1%价差
                risk_score += 0.4
                risk_factors.append(f"高买卖价差: {spread_pct:.4f}")
            elif spread_pct > 0.005:  # 0.5%价差
                risk_score += 0.2
                risk_factors.append(f"中等买卖价差: {spread_pct:.4f}")
                
        # 基于订单簿深度的风险
        if 'bid_depth_10' in features and 'ask_depth_10' in features:
            bid_depth = features['bid_depth_10']
            ask_depth = features['ask_depth_10']
            total_depth = bid_depth + ask_depth
            
            if total_depth < 100:  # 低流动性
                risk_score += 0.5
                risk_factors.append(f"低订单簿深度: {total_depth:.2f}")
            elif total_depth < 1000:  # 中等流动性
                risk_score += 0.2
                risk_factors.append(f"中等订单簿深度: {total_depth:.2f}")
                
        # 基于订单簿不平衡的风险
        if 'order_book_imbalance' in features:
            imbalance = abs(features['order_book_imbalance'])
            if imbalance > 0.8:
                risk_score += 0.3
                risk_factors.append(f"严重订单簿不平衡: {imbalance:.3f}")
                
        return {
            'score': min(risk_score, 1.0),
            'factors': risk_factors,
            'level': 'high' if risk_score > 0.6 else 'medium' if risk_score > 0.3 else 'low'
        }
        
    async def _assess_volatility_risk(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """评估波动性风险
        
        Args:
            features: 市场特征
            
        Returns:
            波动性风险评估结果
        """
        risk_score = 0.0
        risk_factors = []
        
        # 基于历史波动率
        if 'price_volatility' in features:
            volatility = features['price_volatility']
            risk_score = min(volatility * 5, 1.0)  # 波动率*5作为风险评分
            
            if risk_score > 0.6:
                risk_factors.append(f"高波动率风险: {volatility:.3f}")
                
        return {
            'score': risk_score,
            'factors': risk_factors,
            'level': 'high' if risk_score > 0.6 else 'medium' if risk_score > 0.3 else 'low'
        }
        
    async def _assess_concentration_risk(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """评估集中风险
        
        Args:
            signal: 交易信号
            
        Returns:
            集中风险评估结果
        """
        risk_score = 0.0
        risk_factors = []
        
        symbol = signal.get('symbol', 'unknown')
        proposed_position = signal.get('position_size', 0)
        
        # 检查当前仓位
        current_position = self.position_tracker.get(symbol, 0)
        total_exposure = sum(self.position_tracker.values())
        
        # 计算新的总敞口
        new_total_exposure = total_exposure + proposed_position
        
        # 评估集中风险
        if new_total_exposure > 0.5:  # 超过50%总资金
            risk_score += 0.8
            risk_factors.append(f"过度集中风险: {new_total_exposure:.2f}")
        elif new_total_exposure > 0.3:  # 超过30%总资金
            risk_score += 0.4
            risk_factors.append(f"中等集中风险: {new_total_exposure:.2f}")
            
        # 单一资产集中风险
        if current_position + proposed_position > 0.2:  # 单个资产超过20%
            risk_score += 0.3
            risk_factors.append(f"单一资产过度集中: {symbol}")
            
        return {
            'score': min(risk_score, 1.0),
            'factors': risk_factors,
            'level': 'high' if risk_score > 0.6 else 'medium' if risk_score > 0.3 else 'low'
        }
        
    async def _assess_timing_risk(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """评估时机风险
        
        Args:
            features: 市场特征
            
        Returns:
            时机风险评估结果
        """
        risk_score = 0.0
        risk_factors = []
        
        current_time = datetime.now()
        
        # 避免在高波动时段交易（如重要新闻发布前后）
        # 这里可以根据历史数据判断
        
        # 避免在市场开盘/收盘时段交易
        hour = current_time.hour
        if hour in [0, 1, 23]:  # 假设这些是低流动性时段
            risk_score += 0.3
            risk_factors.append(f"低流动性时段: {hour}:00")
            
        return {
            'score': risk_score,
            'factors': risk_factors,
            'level': 'high' if risk_score > 0.6 else 'medium' if risk_score > 0.3 else 'low'
        }
        
    async def _calculate_overall_risk(self, assessments: Dict[str, Any]) -> Dict[str, Any]:
        """计算综合风险评分
        
        Args:
            assessments: 各项风险评估
            
        Returns:
            综合风险评分
        """
        # 加权计算综合风险
        weights = {
            'market_risk': 0.25,
            'liquidity_risk': 0.25,
            'volatility_risk': 0.2,
            'concentration_risk': 0.2,
            'timing_risk': 0.1
        }
        
        total_score = 0.0
        total_weight = 0.0
        
        for risk_type, assessment in assessments.items():
            if risk_type in weights:
                total_score += assessment['score'] * weights[risk_type]
                total_weight += weights[risk_type]
                
        overall_score = total_score / total_weight if total_weight > 0 else 0.0
        
        # 确定风险等级
        if overall_score > 0.7:
            level = 'high'
        elif overall_score > 0.4:
            level = 'medium'
        else:
            level = 'low'
            
        return {
            'score': overall_score,
            'level': level,
            'factors': [f"{k}: {v['score']:.2f}" for k, v in assessments.items()]
        }
        
    async def _check_risk_limits(self, signal: Dict[str, Any], features: Dict[str, Any]) -> Dict[str, Any]:
        """检查风险限制
        
        Args:
            signal: 交易信号
            features: 市场特征
            
        Returns:
            限制检查结果
        """
        symbol = signal.get('symbol', 'unknown')
        current_date = datetime.now().date()
        
        # 初始化日计数
        if symbol not in self.daily_trades:
            self.daily_trades[symbol] = {}
        if current_date not in self.daily_trades[symbol]:
            self.daily_trades[symbol][current_date] = 0
            
        # 检查日交易次数限制
        if self.daily_trades[symbol][current_date] >= self.risk_limits['max_daily_trades']:
            return {
                'passed': False,
                'reason': f'超过日交易次数限制: {self.risk_limits["max_daily_trades"]}'
            }
            
        # 检查日亏损限制
        if symbol in self.daily_pnl and current_date in self.daily_pnl[symbol]:
            daily_loss = self.daily_pnl[symbol][current_date]
            if daily_loss < -self.risk_limits['max_daily_loss']:
                return {
                    'passed': False,
                    'reason': f'超过日亏损限制: {abs(daily_loss):.3f} > {self.risk_limits["max_daily_loss"]}'
                }
                
        return {
            'passed': True,
            'reason': '通过所有风险限制检查'
        }
        
    async def _make_final_decision(self, signal: Dict[str, Any], risk_assessment: Dict[str, Any], limit_check: Dict[str, Any]) -> Dict[str, Any]:
        """做出最终决策
        
        Args:
            signal: 交易信号
            risk_assessment: 风险评估结果
            limit_check: 限制检查结果
            
        Returns:
            最终决策
        """
        overall_risk = risk_assessment['overall_risk']
        
        # 如果风险过高，拒绝交易
        if overall_risk['score'] > 0.8:
            return {
                'approved': False,
                'reason': f'风险评分过高: {overall_risk["score"]:.2f}',
                'risk_score': overall_risk['score'],
                'modified_signal': None
            }
            
        # 如果未通过限制检查，拒绝交易
        if not limit_check['passed']:
            return {
                'approved': False,
                'reason': limit_check['reason'],
                'risk_score': overall_risk['score'],
                'modified_signal': None
            }
            
        # 中等风险，可能需要调整仓位
        modified_signal = signal.copy()
        if overall_risk['score'] > 0.5:
            # 降低仓位大小
            original_size = modified_signal.get('position_size', 0)
            reduced_size = original_size * 0.5  # 降低50%
            modified_signal['position_size'] = reduced_size
            
            return {
                'approved': True,
                'reason': f'中等风险，调整仓位大小: {reduced_size:.3f}',
                'risk_score': overall_risk['score'],
                'modified_signal': modified_signal
            }
            
        # 低风险，批准交易
        return {
            'approved': True,
            'reason': '风险可控，批准交易',
            'risk_score': overall_risk['score'],
            'modified_signal': modified_signal
        }
        
    async def _check_circuit_breaker(self) -> bool:
        """检查熔断机制
        
        Returns:
            熔断机制是否触发
        """
        if not self.circuit_breaker['enabled']:
            return False
            
        if not self.circuit_breaker['triggered']:
            return False
            
        # 检查冷却期
        trigger_time = self.circuit_breaker['trigger_time']
        if trigger_time:
            cooldown_hours = self.circuit_breaker['cooldown_hours']
            if datetime.now() - trigger_time > timedelta(hours=cooldown_hours):
                # 冷却期结束，重置熔断器
                self.circuit_breaker['triggered'] = False
                self.circuit_breaker['trigger_time'] = None
                logger.info("熔断器冷却期结束，重新启用交易")
                return False
                
        return True
        
    def trigger_circuit_breaker(self, reason: str = "手动触发"):
        """触发熔断机制
        
        Args:
            reason: 触发原因
        """
        self.circuit_breaker['triggered'] = True
        self.circuit_breaker['trigger_time'] = datetime.now()
        logger.critical(f"熔断机制已触发: {reason}")
        
    def update_position(self, symbol: str, position_size: float, pnl: float = 0):
        """更新仓位信息
        
        Args:
            symbol: 交易对
            position_size: 仓位大小
            pnl: 盈亏金额
        """
        current_date = datetime.now().date()
        
        # 更新仓位跟踪
        self.position_tracker[symbol] = position_size
        
        # 更新日交易计数
        if symbol not in self.daily_trades:
            self.daily_trades[symbol] = {}
        if current_date not in self.daily_trades[symbol]:
            self.daily_trades[symbol][current_date] = 0
            
        self.daily_trades[symbol][current_date] += 1
        
        # 更新日盈亏
        if symbol not in self.daily_pnl:
            self.daily_pnl[symbol] = {}
        if current_date not in self.daily_pnl[symbol]:
            self.daily_pnl[symbol][current_date] = 0
            
        self.daily_pnl[symbol][current_date] += pnl
        
        # 检查是否需要触发熔断
        if self.daily_pnl[symbol][current_date] < -self.risk_limits['max_daily_loss']:
            self.trigger_circuit_breaker(f"{symbol} 日亏损超过限制")
            
    def get_risk_metrics(self) -> Dict[str, Any]:
        """获取风险指标
        
        Returns:
            风险指标字典
        """
        current_date = datetime.now().date()
        
        # 计算当前风险指标
        total_positions = sum(self.position_tracker.values())
        daily_trades_total = sum(
            trades.get(current_date, 0) 
            for trades in self.daily_trades.values()
        )
        daily_pnl_total = sum(
            pnl.get(current_date, 0) 
            for pnl in self.daily_pnl.values()
        )
        
        return {
            'total_position_size': total_positions,
            'daily_trades_count': daily_trades_total,
            'daily_pnl': daily_pnl_total,
            'circuit_breaker_status': self.circuit_breaker['triggered'],
            'risk_limits': self.risk_limits,
            'position_tracker': self.position_tracker.copy()
        }