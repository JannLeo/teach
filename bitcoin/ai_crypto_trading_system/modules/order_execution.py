"""订单执行模块

负责将交易指令转化为实际的市场交易
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import numpy as np

from utils.logger import logger
from utils.config_loader import config_loader

try:
    from binance.client import Client as BinanceClient
    from binance.enums import *
    from binance.exceptions import BinanceAPIException, BinanceOrderException
    BINANCE_AVAILABLE = True
except ImportError:
    logger.warning("Binance API库未安装，将使用模拟执行")
    BINANCE_AVAILABLE = False


class OrderExecutionModule:
    """订单执行模块"""
    
    def __init__(self):
        """初始化订单执行模块"""
        self.exchange_clients = {}
        self.order_history = []
        self.active_orders = {}
        
        # 初始化交易所客户端
        self._init_exchange_clients()
        
        # 订单配置
        self.order_config = {
            'order_type': config_loader.get('trading.order_type', 'limit'),
            'order_timeout': config_loader.get('trading.order_timeout', 60),
            'base_currency': config_loader.get('trading.base_currency', 'USDT')
        }
        
    def _init_exchange_clients(self):
        """初始化交易所客户端"""
        try:
            api_key = config_loader.get('data_sources.exchange.api_key')
            secret_key = config_loader.get('data_sources.exchange.secret_key')
            testnet = config_loader.get('data_sources.exchange.testnet', True)
            
            if BINANCE_AVAILABLE and api_key and secret_key:
                self.exchange_clients['binance'] = {
                    'client': BinanceClient(api_key, secret_key, testnet=testnet),
                    'enabled': True
                }
                logger.info("Binance订单执行客户端初始化成功")
            else:
                logger.warning("使用模拟订单执行")
                
        except Exception as e:
            logger.error(f"交易所客户端初始化失败: {e}")
            
    async def execute_order(self, trading_signal: Dict[str, Any]) -> Dict[str, Any]:
        """执行交易订单
        
        Args:
            trading_signal: 交易信号
            
        Returns:
            订单执行结果
        """
        try:
            symbol = trading_signal.get('symbol', 'unknown')
            decision = trading_signal.get('decision', 'hold')
            
            logger.info(f"开始执行 {symbol} 的 {decision} 订单")
            
            if decision == 'hold':
                return {
                    'success': True,
                    'order_id': None,
                    'reason': '持有决策，无需执行'
                }
                
            # 准备订单参数
            order_params = await self._prepare_order_params(trading_signal)
            
            # 执行订单
            if 'binance' in self.exchange_clients:
                order_result = await self._execute_real_order(order_params)
            else:
                order_result = await self._execute_simulated_order(order_params)
                
            # 记录订单历史
            self._record_order(order_params, order_result)
            
            # 更新活跃订单
            if order_result.get('success') and order_result.get('order_id'):
                await self._track_active_order(order_result['order_id'], symbol)
                
            logger.info(f"订单执行完成: {'成功' if order_result['success'] else '失败'}")
            return order_result
            
        except Exception as e:
            logger.error(f"订单执行错误: {e}")
            return {
                'success': False,
                'order_id': None,
                'reason': f'执行错误: {str(e)}'
            }
            
    async def _prepare_order_params(self, trading_signal: Dict[str, Any]) -> Dict[str, Any]:
        """准备订单参数
        
        Args:
            trading_signal: 交易信号
            
        Returns:
            订单参数字典
        """
        symbol = trading_signal.get('symbol', 'unknown')
        decision = trading_signal.get('decision', 'hold')
        position_size = trading_signal.get('position_size', 0)
        
        # 获取当前价格
        current_price = await self._get_current_price(symbol)
        
        # 计算订单数量
        base_currency = self.order_config['base_currency']
        if symbol.endswith(f'/{base_currency}'):
            # 计算基础货币的订单数量
            order_quantity = position_size / current_price
        else:
            # 直接使用position_size作为数量
            order_quantity = position_size
            
        # 设置止损止盈
        stop_loss = trading_signal.get('stop_loss', 0.05)
        take_profit = trading_signal.get('take_profit', 0.1)
        
        # 计算止损止盈价格
        if decision == 'buy':
            stop_loss_price = current_price * (1 - stop_loss)
            take_profit_price = current_price * (1 + take_profit)
        else:  # sell
            stop_loss_price = current_price * (1 + stop_loss)
            take_profit_price = current_price * (1 - take_profit)
            
        return {
            'symbol': symbol,
            'side': decision.upper(),  # BUY or SELL
            'order_type': self.order_config['order_type'],
            'quantity': order_quantity,
            'price': current_price,
            'stop_loss_price': stop_loss_price,
            'take_profit_price': take_profit_price,
            'timestamp': datetime.now().isoformat()
        }
        
    async def _execute_real_order(self, order_params: Dict[str, Any]) -> Dict[str, Any]:
        """执行真实订单
        
        Args:
            order_params: 订单参数
            
        Returns:
            订单执行结果
        """
        try:
            client = self.exchange_clients['binance']['client']
            symbol = order_params['symbol'].replace('/', '')  # 转换格式
            
            # 创建订单
            if order_params['order_type'] == 'market':
                order = client.order_market(
                    symbol=symbol,
                    side=order_params['side'],
                    quantity=order_params['quantity']
                )
            else:  # limit order
                order = client.order_limit(
                    symbol=symbol,
                    side=order_params['side'],
                    quantity=order_params['quantity'],
                    price=str(order_params['price'])
                )
                
            return {
                'success': True,
                'order_id': order['orderId'],
                'status': order['status'],
                'executed_qty': float(order.get('executedQty', 0)),
                'price': float(order.get('price', order_params['price'])),
                'reason': '订单创建成功'
            }
            
        except BinanceAPIException as e:
            logger.error(f"Binance API错误: {e}")
            return {
                'success': False,
                'order_id': None,
                'reason': f'API错误: {str(e)}'
            }
        except BinanceOrderException as e:
            logger.error(f"订单错误: {e}")
            return {
                'success': False,
                'order_id': None,
                'reason': f'订单错误: {str(e)}'
            }
        except Exception as e:
            logger.error(f"执行订单错误: {e}")
            return {
                'success': False,
                'order_id': None,
                'reason': f'执行错误: {str(e)}'
            }
            
    async def _execute_simulated_order(self, order_params: Dict[str, Any]) -> Dict[str, Any]:
        """执行模拟订单
        
        Args:
            order_params: 订单参数
            
        Returns:
            模拟订单执行结果
        """
        # 模拟订单执行
        order_id = f"SIM_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash(order_params['symbol']) % 10000}"
        
        # 模拟部分成交
        executed_qty = order_params['quantity'] * np.random.uniform(0.8, 1.0)
        executed_price = order_params['price'] * (1 + np.random.uniform(-0.001, 0.001))
        
        await asyncio.sleep(0.5)  # 模拟执行延迟
        
        return {
            'success': True,
            'order_id': order_id,
            'status': 'FILLED',
            'executed_qty': executed_qty,
            'price': executed_price,
            'reason': '模拟订单执行成功'
        }
        
    async def _get_current_price(self, symbol: str) -> float:
        """获取当前价格
        
        Args:
            symbol: 交易对
            
        Returns:
            当前价格
        """
        try:
            if 'binance' in self.exchange_clients:
                client = self.exchange_clients['binance']['client']
                ticker = client.get_symbol_ticker(symbol=symbol.replace('/', ''))
                return float(ticker['price'])
            else:
                # 模拟价格
                return 30000.0 + np.random.uniform(-1000, 1000)
                
        except Exception as e:
            logger.error(f"获取当前价格失败: {e}")
            return 30000.0  # 默认价格
            
    def _record_order(self, order_params: Dict[str, Any], order_result: Dict[str, Any]):
        """记录订单
        
        Args:
            order_params: 订单参数
            order_result: 订单结果
        """
        order_record = {
            'timestamp': datetime.now().isoformat(),
            'order_params': order_params,
            'order_result': order_result,
            'symbol': order_params['symbol'],
            'side': order_params['side'],
            'quantity': order_params['quantity'],
            'price': order_params['price']
        }
        
        self.order_history.append(order_record)
        
        # 限制历史记录大小
        if len(self.order_history) > 1000:
            self.order_history = self.order_history[-500:]
            
    async def _track_active_order(self, order_id: str, symbol: str):
        """跟踪活跃订单
        
        Args:
            order_id: 订单ID
            symbol: 交易对
        """
        self.active_orders[order_id] = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'status': 'active'
        }
        
        # 启动订单状态监控
        asyncio.create_task(self._monitor_order_status(order_id, symbol))
        
    async def _monitor_order_status(self, order_id: str, symbol: str):
        """监控订单状态
        
        Args:
            order_id: 订单ID
            symbol: 交易对
        """
        max_monitor_time = self.order_config['order_timeout']
        start_time = datetime.now()
        
        while order_id in self.active_orders:
            try:
                # 检查超时
                if (datetime.now() - start_time).seconds > max_monitor_time:
                    logger.warning(f"订单 {order_id} 监控超时")
                    await self._cancel_order(order_id, symbol)
                    break
                    
                # 获取订单状态
                if 'binance' in self.exchange_clients:
                    status = await self._get_real_order_status(order_id, symbol)
                else:
                    status = await self._get_simulated_order_status(order_id, symbol)
                    
                # 更新订单状态
                self.active_orders[order_id]['status'] = status['status']
                
                # 如果订单已完成或被取消，停止监控
                if status['status'] in ['FILLED', 'CANCELED', 'REJECTED']:
                    del self.active_orders[order_id]
                    break
                    
                await asyncio.sleep(5)  # 每5秒检查一次
                
            except Exception as e:
                logger.error(f"监控订单状态错误: {e}")
                break
                
    async def _get_real_order_status(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """获取真实订单状态
        
        Args:
            order_id: 订单ID
            symbol: 交易对
            
        Returns:
            订单状态
        """
        try:
            client = self.exchange_clients['binance']['client']
            order = client.get_order(
                symbol=symbol.replace('/', ''),
                orderId=order_id
            )
            
            return {
                'status': order['status'],
                'executed_qty': float(order.get('executedQty', 0)),
                'price': float(order.get('price', 0))
            }
            
        except Exception as e:
            logger.error(f"获取订单状态错误: {e}")
            return {'status': 'ERROR', 'executed_qty': 0, 'price': 0}
            
    async def _get_simulated_order_status(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """获取模拟订单状态
        
        Args:
            order_id: 订单ID
            symbol: 交易对
            
        Returns:
            订单状态
        """
        # 模拟订单在10-30秒内完成
        import random
        if random.random() < 0.1:  # 10%概率完成
            return {'status': 'FILLED', 'executed_qty': 1.0, 'price': 30000.0}
        else:
            return {'status': 'NEW', 'executed_qty': 0, 'price': 0}
            
    async def _cancel_order(self, order_id: str, symbol: str):
        """取消订单
        
        Args:
            order_id: 订单ID
            symbol: 交易对
        """
        try:
            if 'binance' in self.exchange_clients:
                client = self.exchange_clients['binance']['client']
                client.cancel_order(
                    symbol=symbol.replace('/', ''),
                    orderId=order_id
                )
                logger.info(f"订单 {order_id} 已取消")
            else:
                logger.info(f"模拟取消订单 {order_id}")
                
        except Exception as e:
            logger.error(f"取消订单错误: {e}")
        finally:
            if order_id in self.active_orders:
                del self.active_orders[order_id]
                
    def get_order_history(self, symbol: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """获取订单历史
        
        Args:
            symbol: 交易对筛选
            limit: 记录限制
            
        Returns:
            订单历史列表
        """
        orders = self.order_history
        
        if symbol:
            orders = [o for o in orders if o['symbol'] == symbol]
            
        return orders[-limit:]
        
    def get_active_orders(self) -> Dict[str, Any]:
        """获取活跃订单
        
        Returns:
            活跃订单字典
        """
        return self.active_orders.copy()
        
    def get_trading_statistics(self) -> Dict[str, Any]:
        """获取交易统计
        
        Returns:
            交易统计字典
        """
        if not self.order_history:
            return {}
            
        total_orders = len(self.order_history)
        successful_orders = sum(1 for o in self.order_history if o['order_result']['success'])
        
        # 计算总成交量
        total_volume = sum(
            o['quantity'] * o['price'] 
            for o in self.order_history 
            if o['order_result']['success']
        )
        
        # 按交易对统计
        symbol_stats = {}
        for order in self.order_history:
            symbol = order['symbol']
            if symbol not in symbol_stats:
                symbol_stats[symbol] = {'count': 0, 'volume': 0}
            symbol_stats[symbol]['count'] += 1
            if order['order_result']['success']:
                symbol_stats[symbol]['volume'] += order['quantity'] * order['price']
                
        return {
            'total_orders': total_orders,
            'successful_orders': successful_orders,
            'success_rate': successful_orders / total_orders if total_orders > 0 else 0,
            'total_volume': total_volume,
            'active_orders_count': len(self.active_orders),
            'symbol_statistics': symbol_stats
        }