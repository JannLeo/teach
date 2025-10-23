"""数据采集模块

负责从交易所和GMGN等平台获取市场数据
"""

import asyncio
import aiohttp
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

from utils.logger import logger
from utils.config_loader import config_loader

try:
    import ccxt.pro as ccxt
    from binance.client import Client as BinanceClient
    from binance.streams import BinanceSocketManager
except ImportError as e:
    logger.warning(f"交易所API库导入失败: {e}")


class DataCollectionModule:
    """数据采集模块"""
    
    def __init__(self):
        """初始化数据采集模块"""
        self.exchange_clients = {}
        self.gmgn_client = None
        self.running = False
        self.data_buffer = {}  # 数据缓冲区
        
        # 初始化交易所客户端
        self._init_exchange_clients()
        
    def _init_exchange_clients(self):
        """初始化交易所客户端"""
        try:
            # 初始化Binance客户端
            api_key = config_loader.get('data_sources.exchange.api_key')
            secret_key = config_loader.get('data_sources.exchange.secret_key')
            testnet = config_loader.get('data_sources.exchange.testnet', True)
            
            if api_key and secret_key:
                self.exchange_clients['binance'] = {
                    'client': BinanceClient(api_key, secret_key, testnet=testnet),
                    'enabled': True
                }
                logger.info("Binance客户端初始化成功")
            else:
                logger.warning("未配置交易所API密钥，使用模拟数据")
                
        except Exception as e:
            logger.error(f"交易所客户端初始化失败: {e}")
            
    async def start_data_collection(self, symbols: List[str]):
        """启动数据采集
        
        Args:
            symbols: 要监控的交易对列表
        """
        self.running = True
        logger.info(f"启动数据采集，监控交易对: {symbols}")
        
        tasks = [
            self._collect_market_data(symbols),
            self._collect_gmgn_data(),
            self._collect_orderbook_data(symbols)
        ]
        
        await asyncio.gather(*tasks)
        
    async def stop_data_collection(self):
        """停止数据采集"""
        self.running = False
        logger.info("数据采集已停止")
        
    async def _collect_market_data(self, symbols: List[str]):
        """收集市场数据（K线、交易量等）
        
        Args:
            symbols: 交易对列表
        """
        while self.running:
            try:
                for symbol in symbols:
                    # 获取实时价格数据
                    price_data = await self._fetch_price_data(symbol)
                    
                    # 获取K线数据
                    kline_data = await self._fetch_kline_data(symbol)
                    
                    # 存储到缓冲区
                    self._store_data(f"price_{symbol}", price_data)
                    self._store_data(f"kline_{symbol}", kline_data)
                    
                    logger.debug(f"已采集 {symbol} 的市场数据")
                    
                await asyncio.sleep(5)  # 每5秒采集一次
                
            except Exception as e:
                logger.error(f"市场数据采集错误: {e}")
                await asyncio.sleep(10)
                
    async def _collect_gmgn_data(self):
        """收集GMGN平台数据（聪明钱动向等）"""
        while self.running:
            try:
                if config_loader.get('data_sources.gmgn.enabled'):
                    gmgn_data = await self._fetch_gmgn_data()
                    self._store_data("gmgn_signals", gmgn_data)
                    logger.debug("已采集GMGN数据")
                    
                await asyncio.sleep(30)  # 每30秒采集一次
                
            except Exception as e:
                logger.error(f"GMGN数据采集错误: {e}")
                await asyncio.sleep(60)
                
    async def _collect_orderbook_data(self, symbols: List[str]):
        """收集订单簿数据
        
        Args:
            symbols: 交易对列表
        """
        while self.running:
            try:
                for symbol in symbols:
                    orderbook_data = await self._fetch_orderbook_data(symbol)
                    self._store_data(f"orderbook_{symbol}", orderbook_data)
                    logger.debug(f"已采集 {symbol} 的订单簿数据")
                    
                await asyncio.sleep(1)  # 每秒采集一次
                
            except Exception as e:
                logger.error(f"订单簿数据采集错误: {e}")
                await asyncio.sleep(5)
                
    async def _fetch_price_data(self, symbol: str) -> Dict[str, Any]:
        """获取价格数据
        
        Args:
            symbol: 交易对
            
        Returns:
            价格数据字典
        """
        try:
            if 'binance' in self.exchange_clients:
                client = self.exchange_clients['binance']['client']
                ticker = client.get_symbol_ticker(symbol=symbol.replace('/', ''))
                
                return {
                    'symbol': symbol,
                    'price': float(ticker['price']),
                    'timestamp': datetime.now().isoformat(),
                    'source': 'binance'
                }
            else:
                # 模拟数据
                return {
                    'symbol': symbol,
                    'price': np.random.uniform(30000, 31000),  # 模拟BTC价格
                    'timestamp': datetime.now().isoformat(),
                    'source': 'simulation'
                }
                
        except Exception as e:
            logger.error(f"获取价格数据失败 {symbol}: {e}")
            return {}
            
    async def _fetch_kline_data(self, symbol: str) -> Dict[str, Any]:
        """获取K线数据
        
        Args:
            symbol: 交易对
            
        Returns:
            K线数据字典
        """
        try:
            if 'binance' in self.exchange_clients:
                client = self.exchange_clients['binance']['client']
                klines = client.get_klines(
                    symbol=symbol.replace('/', ''),
                    interval=Client.KLINE_INTERVAL_1MINUTE,
                    limit=60
                )
                
                df = pd.DataFrame(klines, columns=[
                    'timestamp', 'open', 'high', 'low', 'close',
                    'volume', 'close_time', 'quote_volume', 'trades',
                    'taker_buy_base', 'taker_buy_quote', 'ignore'
                ])
                
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df[['open', 'high', 'low', 'close', 'volume']] = df[
                    ['open', 'high', 'low', 'close', 'volume']
                ].astype(float)
                
                return {
                    'symbol': symbol,
                    'data': df.to_dict('records'),
                    'timestamp': datetime.now().isoformat(),
                    'source': 'binance'
                }
            else:
                # 模拟K线数据
                base_price = np.random.uniform(30000, 31000)
                data = []
                
                for i in range(60):
                    price = base_price + np.random.normal(0, 100)
                    data.append({
                        'timestamp': datetime.now() - timedelta(minutes=60-i),
                        'open': price,
                        'high': price + np.random.uniform(0, 50),
                        'low': price - np.random.uniform(0, 50),
                        'close': price + np.random.normal(0, 20),
                        'volume': np.random.uniform(100, 1000)
                    })
                    
                return {
                    'symbol': symbol,
                    'data': data,
                    'timestamp': datetime.now().isoformat(),
                    'source': 'simulation'
                }
                
        except Exception as e:
            logger.error(f"获取K线数据失败 {symbol}: {e}")
            return {}
            
    async def _fetch_gmgn_data(self) -> Dict[str, Any]:
        """获取GMGN平台数据
        
        Returns:
            GMGN数据字典
        """
        try:
            # 这里应该实现真实的GMGN API调用
            # 目前返回模拟数据
            return {
                'smart_money_signals': [
                    {
                        'token': 'BTC',
                        'action': 'buy',
                        'amount': 100000,
                        'address': '0x1234...abcd',
                        'confidence': 0.85,
                        'timestamp': datetime.now().isoformat()
                    }
                ],
                'trending_tokens': ['BTC', 'ETH', 'SOL'],
                'timestamp': datetime.now().isoformat(),
                'source': 'gmgn_simulation'
            }
            
        except Exception as e:
            logger.error(f"获取GMGN数据失败: {e}")
            return {}
            
    async def _fetch_orderbook_data(self, symbol: str) -> Dict[str, Any]:
        """获取订单簿数据
        
        Args:
            symbol: 交易对
            
        Returns:
            订单簿数据字典
        """
        try:
            # 模拟订单簿数据
            return {
                'symbol': symbol,
                'bids': [
                    [30000 + i, np.random.uniform(0.1, 1.0)] 
                    for i in range(10)
                ],
                'asks': [
                    [30001 + i, np.random.uniform(0.1, 1.0)] 
                    for i in range(10)
                ],
                'timestamp': datetime.now().isoformat(),
                'source': 'simulation'
            }
            
        except Exception as e:
            logger.error(f"获取订单簿数据失败 {symbol}: {e}")
            return {}
            
    def _store_data(self, key: str, data: Dict[str, Any]):
        """存储数据到缓冲区
        
        Args:
            key: 数据键
            data: 数据字典
        """
        if key not in self.data_buffer:
            self.data_buffer[key] = []
            
        self.data_buffer[key].append(data)
        
        # 限制缓冲区大小
        if len(self.data_buffer[key]) > 1000:
            self.data_buffer[key] = self.data_buffer[key][-500:]
            
    def get_latest_data(self, key: str) -> Optional[Dict[str, Any]]:
        """获取最新数据
        
        Args:
            key: 数据键
            
        Returns:
            最新数据字典或None
        """
        if key in self.data_buffer and self.data_buffer[key]:
            return self.data_buffer[key][-1]
        return None
        
    def get_historical_data(self, key: str, limit: int = 100) -> List[Dict[str, Any]]:
        """获取历史数据
        
        Args:
            key: 数据键
            limit: 数据条数限制
            
        Returns:
            历史数据列表
        """
        if key in self.data_buffer:
            return self.data_buffer[key][-limit:]
        return []
        
    def get_all_data_keys(self) -> List[str]:
        """获取所有数据键
        
        Returns:
            数据键列表
        """
        return list(self.data_buffer.keys())