"""主程序入口

AI驱动加密货币自动化交易系统的主程序
"""

import asyncio
import signal
import sys
from typing import Dict, Any
import logging

from utils.logger import logger, setup_logging
from utils.config_loader import config_loader

from modules.data_collection import DataCollectionModule
from modules.feature_engineering import FeatureEngineeringModule
from modules.ai_decision import AIDecisionModule
from modules.risk_management import RiskManagementModule
from modules.order_execution import OrderExecutionModule
from modules.monitoring import MonitoringModule


class AITradingSystem:
    """AI交易系统主类"""
    
    def __init__(self):
        """初始化AI交易系统"""
        self.running = False
        self.modules = {}
        self.system_config = {}
        
        # 初始化系统配置
        self._load_system_config()
        
        # 初始化各个模块
        self._initialize_modules()
        
        # 设置信号处理
        self._setup_signal_handlers()
        
        logger.info("AI交易系统初始化完成")
        
    def _load_system_config(self):
        """加载系统配置"""
        self.system_config = {
            'name': config_loader.get('system.name', 'AI Crypto Trading System'),
            'version': config_loader.get('system.version', '1.0.0'),
            'mode': config_loader.get('system.mode', 'development'),
            'trading_pairs': config_loader.get_trading_pairs(),
            'log_level': config_loader.get('system.log_level', 'INFO')
        }
        
        logger.info(f"系统配置加载完成: {self.system_config['name']} v{self.system_config['version']}")
        
    def _initialize_modules(self):
        """初始化系统模块"""
        logger.info("初始化系统模块...")
        
        # 数据采集模块
        self.modules['data_collection'] = DataCollectionModule()
        
        # 特征工程模块
        self.modules['feature_engineering'] = FeatureEngineeringModule()
        
        # AI决策模块
        self.modules['ai_decision'] = AIDecisionModule()
        
        # 风险管理模块
        self.modules['risk_management'] = RiskManagementModule()
        
        # 订单执行模块
        self.modules['order_execution'] = OrderExecutionModule()
        
        # 监控模块
        self.modules['monitoring'] = MonitoringModule()
        
        # 注册模块到监控系统
        for name, module in self.modules.items():
            if name != 'monitoring':  # 避免循环注册
                self.modules['monitoring'].register_module(name, module)
                
        logger.info(f"已初始化 {len(self.modules)} 个系统模块")
        
    def _setup_signal_handlers(self):
        """设置信号处理器"""
        def signal_handler(signum, frame):
            logger.info(f"接收到信号 {signum}，准备关闭系统...")
            asyncio.create_task(self.shutdown())
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
    async def start(self):
        """启动系统"""
        if self.running:
            logger.warning("系统已经在运行中")
            return
            
        logger.info("启动AI交易系统...")
        self.running = True
        
        try:
            # 启动各个模块
            await self._start_modules()
            
            # 启动主交易循环
            await self._run_trading_loop()
            
        except Exception as e:
            logger.error(f"系统启动错误: {e}")
            await self.shutdown()
            raise
            
    async def shutdown(self):
        """关闭系统"""
        if not self.running:
            return
            
        logger.info("正在关闭AI交易系统...")
        self.running = False
        
        try:
            # 停止各个模块
            await self._stop_modules()
            
            logger.info("AI交易系统已关闭")
            
        except Exception as e:
            logger.error(f"系统关闭错误: {e}")
            
    async def _start_modules(self):
        """启动各个模块"""
        logger.info("启动系统模块...")
        
        # 启动监控模块
        if 'monitoring' in self.modules:
            asyncio.create_task(self.modules['monitoring'].start_monitoring())
            
        logger.info("所有模块已启动")
        
    async def _stop_modules(self):
        """停止各个模块"""
        logger.info("停止系统模块...")
        
        # 停止数据采集
        if 'data_collection' in self.modules:
            await self.modules['data_collection'].stop_data_collection()
            
        # 停止监控
        if 'monitoring' in self.modules:
            await self.modules['monitoring'].stop_monitoring()
            
        logger.info("所有模块已停止")
        
    async def _run_trading_loop(self):
        """运行主交易循环"""
        logger.info("启动主交易循环...")
        
        # 启动数据采集
        data_collection = self.modules['data_collection']
        trading_pairs = self.system_config['trading_pairs']
        
        # 启动数据采集任务
        data_task = asyncio.create_task(
            data_collection.start_data_collection(trading_pairs)
        )
        
        try:
            while self.running:
                try:
                    # 执行一次完整的交易循环
                    await self._execute_trading_cycle()
                    
                    # 等待下一个周期
                    await asyncio.sleep(30)  # 每30秒执行一次交易循环
                    
                except Exception as e:
                    logger.error(f"交易循环错误: {e}")
                    await asyncio.sleep(60)  # 错误后等待更长时间
                    
        finally:
            # 清理任务
            data_task.cancel()
            
    async def _execute_trading_cycle(self):
        """执行一次完整的交易循环"""
        logger.debug("执行交易循环...")
        
        for symbol in self.system_config['trading_pairs']:
            try:
                await self._process_symbol_trading(symbol)
            except Exception as e:
                logger.error(f"处理 {symbol} 交易时出错: {e}")
                
    async def _process_symbol_trading(self, symbol: str):
        """处理单个交易对的交易流程"""
        logger.debug(f"处理 {symbol} 的交易流程")
        
        # 1. 获取最新市场数据
        market_data = await self._get_market_data(symbol)
        if not market_data:
            logger.warning(f"无法获取 {symbol} 的市场数据")
            return
            
        # 2. 特征工程处理
        features = self.modules['feature_engineering'].process_market_data(market_data)
        if not features:
            logger.warning(f"无法处理 {symbol} 的特征数据")
            return
            
        # 3. AI决策
        trading_decision = await self.modules['ai_decision'].make_trading_decision(features)
        if not trading_decision:
            logger.warning(f"无法获取 {symbol} 的交易决策")
            return
            
        # 4. 风险评估
        risk_assessment = await self.modules['risk_management'].evaluate_trading_signal(
            trading_decision, features
        )
        
        if not risk_assessment['approved']:
            logger.info(f"{symbol} 的交易被风险管理拒绝: {risk_assessment['reason']}")
            return
            
        # 5. 订单执行
        final_signal = risk_assessment.get('modified_signal', trading_decision)
        final_signal['symbol'] = symbol
        
        order_result = await self.modules['order_execution'].execute_order(final_signal)
        
        if order_result['success']:
            logger.info(f"{symbol} 的交易执行成功")
            # 更新风险管理模块的仓位信息
            if final_signal['decision'] != 'hold':
                self.modules['risk_management'].update_position(
                    symbol,
                    final_signal.get('position_size', 0)
                )
        else:
            logger.error(f"{symbol} 的交易执行失败: {order_result['reason']}")
            
    async def _get_market_data(self, symbol: str) -> Dict[str, Any]:
        """获取市场数据
        
        Args:
            symbol: 交易对
            
        Returns:
            市场数据字典
        """
        data_collection = self.modules['data_collection']
        
        # 获取各类数据
        price_data = data_collection.get_latest_data(f"price_{symbol}")
        kline_data = data_collection.get_latest_data(f"kline_{symbol}")
        orderbook_data = data_collection.get_latest_data(f"orderbook_{symbol}")
        gmgn_data = data_collection.get_latest_data("gmgn_signals")
        
        # 组合数据
        market_data = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat()
        }
        
        if price_data:
            market_data['price'] = price_data.get('price')
            market_data['price_data'] = price_data
            
        if kline_data:
            market_data['kline_data'] = kline_data.get('data', [])
            
        if orderbook_data:
            market_data['orderbook_data'] = orderbook_data
            
        if gmgn_data:
            market_data['gmgn_data'] = gmgn_data
            
        return market_data
        
    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态
        
        Returns:
            系统状态字典
        """
        status = {
            'system_info': self.system_config,
            'running': self.running,
            'modules': {}
        }
        
        # 获取各模块状态
        for name, module in self.modules.items():
            if hasattr(module, 'get_real_time_status'):
                status['modules'][name] = module.get_real_time_status()
            else:
                status['modules'][name] = {'status': 'active'}
                
        return status
        
    def get_performance_summary(self) -> Dict[str, Any]:
        """获取性能摘要
        
        Returns:
            性能摘要字典
        """
        if 'monitoring' in self.modules:
            return self.modules['monitoring'].get_performance_summary()
        else:
            return {}
            
    def get_trading_statistics(self) -> Dict[str, Any]:
        """获取交易统计
        
        Returns:
            交易统计字典
        """
        stats = {}
        
        # 从各模块收集统计信息
        if 'ai_decision' in self.modules:
            stats['ai_decisions'] = self.modules['ai_decision'].get_trading_statistics()
            
        if 'risk_management' in self.modules:
            stats['risk_metrics'] = self.modules['risk_management'].get_risk_metrics()
            
        if 'order_execution' in self.modules:
            stats['order_execution'] = self.modules['order_execution'].get_trading_statistics()
            
        return stats


async def main():
    """主函数"""
    try:
        # 设置日志
        setup_logging(
            log_level=config_loader.get('system.log_level', 'INFO'),
            log_dir='logs'
        )
        
        # 创建系统实例
        trading_system = AITradingSystem()
        
        # 启动系统
        await trading_system.start()
        
    except KeyboardInterrupt:
        logger.info("接收到键盘中断")
    except Exception as e:
        logger.error(f"主程序错误: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    # 运行主程序
    exit_code = asyncio.run(main())
    sys.exit(exit_code)