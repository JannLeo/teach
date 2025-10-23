"""特征工程模块

负责数据清洗、特征提取和预处理
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from utils.logger import logger

try:
    import ta  # 技术分析库
    TA_AVAILABLE = True
except ImportError:
    logger.warning("技术分析库ta未安装，将使用基础指标")
    TA_AVAILABLE = False


class FeatureEngineeringModule:
    """特征工程模块"""
    
    def __init__(self):
        """初始化特征工程模块"""
        self.feature_buffer = {}
        self.feature_definitions = self._define_features()
        
    def _define_features(self) -> Dict[str, Any]:
        """定义特征集合
        
        Returns:
            特征定义字典
        """
        return {
            'price_features': [
                'current_price', 'price_change_1m', 'price_change_5m', 
                'price_change_15m', 'price_volatility', 'price_momentum'
            ],
            'volume_features': [
                'current_volume', 'volume_change_1m', 'volume_ma_5m',
                'volume_ratio', 'buy_sell_ratio'
            ],
            'technical_features': [
                'rsi', 'macd', 'bollinger_upper', 'bollinger_lower',
                'sma_20', 'ema_12', 'ema_26'
            ],
            'market_features': [
                'spread', 'order_book_imbalance', 'market_depth',
                'smart_money_signal', 'trending_score'
            ],
            'risk_features': [
                'volatility_risk', 'liquidity_risk', 'market_risk_score'
            ]
        }
        
    def process_market_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理市场数据，提取特征
        
        Args:
            raw_data: 原始市场数据
            
        Returns:
            特征字典
        """
        try:
            features = {}
            
            # 处理价格数据
            if 'price' in raw_data:
                price_features = self._extract_price_features(raw_data)
                features.update(price_features)
                
            # 处理K线数据
            if 'kline_data' in raw_data:
                kline_features = self._extract_kline_features(raw_data['kline_data'])
                features.update(kline_features)
                
            # 处理订单簿数据
            if 'orderbook_data' in raw_data:
                orderbook_features = self._extract_orderbook_features(
                    raw_data['orderbook_data']
                )
                features.update(orderbook_features)
                
            # 处理GMGN数据
            if 'gmgn_data' in raw_data:
                gmgn_features = self._extract_gmgn_features(raw_data['gmgn_data'])
                features.update(gmgn_features)
                
            # 计算综合风险评分
            risk_score = self._calculate_risk_score(features)
            features['overall_risk_score'] = risk_score
            
            # 添加时间戳
            features['timestamp'] = datetime.now().isoformat()
            features['symbol'] = raw_data.get('symbol', 'unknown')
            
            logger.debug(f"特征提取完成: {len(features)} 个特征")
            return features
            
        except Exception as e:
            logger.error(f"特征工程处理错误: {e}")
            return {}
            
    def _extract_price_features(self, data: Dict[str, Any]) -> Dict[str, float]:
        """提取价格相关特征
        
        Args:
            data: 包含价格数据的字典
            
        Returns:
            价格特征字典
        """
        features = {}
        current_price = data.get('price', 0)
        
        features['current_price'] = current_price
        
        # 计算价格变化率（需要历史数据）
        if self._has_historical_data('price'):
            hist_data = self._get_historical_data('price', 15)
            
            # 1分钟价格变化
            if len(hist_data) >= 1:
                prev_price = hist_data[-1].get('current_price', current_price)
                features['price_change_1m'] = (current_price - prev_price) / prev_price
                
            # 5分钟价格变化
            if len(hist_data) >= 5:
                prev_price_5m = hist_data[-5].get('current_price', current_price)
                features['price_change_5m'] = (current_price - prev_price_5m) / prev_price_5m
                
            # 15分钟价格变化
            if len(hist_data) >= 15:
                prev_price_15m = hist_data[-15].get('current_price', current_price)
                features['price_change_15m'] = (current_price - prev_price_15m) / prev_price_15m
                
            # 价格波动率
            prices = [d.get('current_price', current_price) for d in hist_data]
            if len(prices) > 1:
                features['price_volatility'] = np.std(prices) / np.mean(prices)
                
        return features
        
    def _extract_kline_features(self, kline_data: List[Dict]) -> Dict[str, float]:
        """提取K线相关特征
        
        Args:
            kline_data: K线数据列表
            
        Returns:
            K线特征字典
        """
        features = {}
        
        if not kline_data:
            return features
            
        # 转换为DataFrame
        df = pd.DataFrame(kline_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # 基础特征
        latest_candle = df.iloc[-1]
        features['open_price'] = float(latest_candle['open'])
        features['high_price'] = float(latest_candle['high'])
        features['low_price'] = float(latest_candle['low'])
        features['close_price'] = float(latest_candle['close'])
        features['volume'] = float(latest_candle['volume'])
        
        # 技术指标
        if TA_AVAILABLE and len(df) >= 20:
            # RSI
            rsi_indicator = ta.momentum.RSIIndicator(df['close'])
            features['rsi'] = float(rsi_indicator.rsi().iloc[-1])
            
            # MACD
            macd_indicator = ta.trend.MACD(df['close'])
            features['macd'] = float(macd_indicator.macd().iloc[-1])
            features['macd_signal'] = float(macd_indicator.macd_signal().iloc[-1])
            
            # 布林带
            bb_indicator = ta.volatility.BollingerBands(df['close'])
            features['bollinger_upper'] = float(bb_indicator.bollinger_hband().iloc[-1])
            features['bollinger_lower'] = float(bb_indicator.bollinger_lband().iloc[-1])
            features['bollinger_mavg'] = float(bb_indicator.bollinger_mavg().iloc[-1])
            
            # 移动平均线
            features['sma_20'] = float(ta.trend.sma_indicator(df['close'], 20).iloc[-1])
            features['ema_12'] = float(ta.trend.ema_indicator(df['close'], 12).iloc[-1])
            features['ema_26'] = float(ta.trend.ema_indicator(df['close'], 26).iloc[-1])
            
        return features
        
    def _extract_orderbook_features(self, orderbook_data: Dict[str, Any]) -> Dict[str, float]:
        """提取订单簿相关特征
        
        Args:
            orderbook_data: 订单簿数据
            
        Returns:
            订单簿特征字典
        """
        features = {}
        
        if not orderbook_data:
            return features
            
        bids = orderbook_data.get('bids', [])
        asks = orderbook_data.get('asks', [])
        
        if bids and asks:
            best_bid = float(bids[0][0])
            best_ask = float(asks[0][0])
            
            # 买卖价差
            features['spread'] = best_ask - best_bid
            features['spread_percentage'] = features['spread'] / best_bid
            
            # 订单簿不平衡
            bid_volume = sum(float(bid[1]) for bid in bids[:10])
            ask_volume = sum(float(ask[1]) for ask in asks[:10])
            
            if bid_volume + ask_volume > 0:
                features['order_book_imbalance'] = (bid_volume - ask_volume) / (bid_volume + ask_volume)
                
            # 市场深度
            features['bid_depth_10'] = bid_volume
            features['ask_depth_10'] = ask_volume
            
        return features
        
    def _extract_gmgn_features(self, gmgn_data: Dict[str, Any]) -> Dict[str, float]:
        """提取GMGN平台相关特征
        
        Args:
            gmgn_data: GMGN数据
            
        Returns:
            GMGN特征字典
        """
        features = {}
        
        if not gmgn_data:
            return features
            
        # 聪明钱信号
        smart_money_signals = gmgn_data.get('smart_money_signals', [])
        if smart_money_signals:
            # 计算聪明钱信号强度
            total_buy_amount = sum(
                signal['amount'] for signal in smart_money_signals 
                if signal['action'] == 'buy'
            )
            total_sell_amount = sum(
                signal['amount'] for signal in smart_money_signals 
                if signal['action'] == 'sell'
            )
            
            features['smart_money_buy_pressure'] = total_buy_amount
            features['smart_money_sell_pressure'] = total_sell_amount
            features['smart_money_net_pressure'] = total_buy_amount - total_sell_amount
            
            # 平均置信度
            if smart_money_signals:
                avg_confidence = np.mean([s['confidence'] for s in smart_money_signals])
                features['smart_money_confidence'] = avg_confidence
                
        # 热门代币趋势
        trending_tokens = gmgn_data.get('trending_tokens', [])
        features['trending_score'] = len(trending_tokens)
        
        return features
        
    def _calculate_risk_score(self, features: Dict[str, float]) -> float:
        """计算综合风险评分
        
        Args:
            features: 特征字典
            
        Returns:
            风险评分 (0-1)
        """
        risk_score = 0.0
        risk_factors = 0
        
        # 波动性风险
        if 'price_volatility' in features:
            volatility = features['price_volatility']
            if volatility > 0.05:  # 5%以上波动视为高风险
                risk_score += min(volatility * 10, 1.0)
            risk_factors += 1
            
        # 流动性风险（基于订单簿深度）
        if 'order_book_imbalance' in features:
            imbalance = abs(features['order_book_imbalance'])
            risk_score += imbalance * 0.5
            risk_factors += 1
            
        # 技术风险（基于RSI超买超卖）
        if 'rsi' in features:
            rsi = features['rsi']
            if rsi > 70 or rsi < 30:  # RSI超买超卖区域
                risk_score += 0.3
            risk_factors += 1
            
        # 市场风险（基于聪明钱信号）
        if 'smart_money_confidence' in features:
            confidence = features['smart_money_confidence']
            if confidence < 0.5:
                risk_score += 0.2
            risk_factors += 1
            
        if risk_factors > 0:
            return min(risk_score / risk_factors, 1.0)
        else:
            return 0.5  # 默认中等风险
            
    def _has_historical_data(self, key: str) -> bool:
        """检查是否有历史数据
        
        Args:
            key: 数据键
            
        Returns:
            是否有历史数据
        """
        return key in self.feature_buffer and len(self.feature_buffer[key]) > 0
        
    def _get_historical_data(self, key: str, limit: int = 100) -> List[Dict[str, Any]]:
        """获取历史数据
        
        Args:
            key: 数据键
            limit: 数据条数限制
            
        Returns:
            历史数据列表
        """
        if key in self.feature_buffer:
            return self.feature_buffer[key][-limit:]
        return []
        
    def store_features(self, symbol: str, features: Dict[str, Any]):
        """存储特征数据
        
        Args:
            symbol: 交易对
            features: 特征字典
        """
        key = f"features_{symbol}"
        if key not in self.feature_buffer:
            self.feature_buffer[key] = []
            
        self.feature_buffer[key].append(features)
        
        # 限制缓冲区大小
        if len(self.feature_buffer[key]) > 1000:
            self.feature_buffer[key] = self.feature_buffer[key][-500:]
            
    def get_latest_features(self, symbol: str) -> Optional[Dict[str, Any]]:
        """获取最新特征
        
        Args:
            symbol: 交易对
            
        Returns:
            最新特征字典或None
        """
        key = f"features_{symbol}"
        if key in self.feature_buffer and self.feature_buffer[key]:
            return self.feature_buffer[key][-1]
        return None
        
    def get_feature_definitions(self) -> Dict[str, List[str]]:
        """获取特征定义
        
        Returns:
            特征定义字典
        """
        return self.feature_definitions