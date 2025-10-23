#!/usr/bin/env python3
"""模块测试脚本

用于测试各个模块的基本功能
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import setup_logging
from utils.config_loader import config_loader
from modules.data_collection import DataCollectionModule
from modules.feature_engineering import FeatureEngineeringModule
from modules.ai_decision import AIDecisionModule
from modules.risk_management import RiskManagementModule
from modules.order_execution import OrderExecutionModule


async def test_data_collection():
    """测试数据采集模块"""
    print("\n=== 测试数据采集模块 ===")
    
    dc = DataCollectionModule()
    
    # 测试获取价格数据
    price_data = await dc._fetch_price_data("BTC/USDT")
    print(f"价格数据: {price_data}")
    
    # 测试获取K线数据
    kline_data = await dc._fetch_kline_data("BTC/USDT")
    print(f"K线数据长度: {len(kline_data.get('data', []))}")
    
    # 测试获取GMGN数据
    gmgn_data = await dc._fetch_gmgn_data()
    print(f"GMGN数据: {gmgn_data}")
    
    # 测试获取订单簿数据
    orderbook_data = await dc._fetch_orderbook_data("BTC/USDT")
    print(f"订单簿数据: {orderbook_data}")


async def test_feature_engineering():
    """测试特征工程模块"""
    print("\n=== 测试特征工程模块 ===")
    
    fe = FeatureEngineeringModule()
    
    # 创建测试数据
    test_data = {
        'symbol': 'BTC/USDT',
        'price': 30000.0,
        'kline_data': [
            {
                'timestamp': '2025-10-23T12:00:00',
                'open': 29900,
                'high': 30100,
                'low': 29800,
                'close': 30000,
                'volume': 1000
            }
        ] * 60,
        'orderbook_data': {
            'bids': [[30000, 1.0], [29999, 2.0]],
            'asks': [[30001, 1.5], [30002, 2.5]]
        },
        'gmgn_data': {
            'smart_money_signals': [
                {'action': 'buy', 'amount': 100000, 'confidence': 0.85}
            ]
        }
    }
    
    features = fe.process_market_data(test_data)
    print(f"提取的特征数量: {len(features)}")
    print(f"关键特征: {{
        'current_price': features.get('current_price'),
        'rsi': features.get('rsi'),
        'price_volatility': features.get('price_volatility'),
        'overall_risk_score': features.get('overall_risk_score')
    }}")


async def test_ai_decision():
    """测试AI决策模块"""
    print("\n=== 测试AI决策模块 ===")
    
    ai = AIDecisionModule()
    
    # 创建测试特征
    test_features = {
        'symbol': 'BTC/USDT',
        'current_price': 30000.0,
        'price_change_1m': 0.02,
        'price_change_5m': 0.05,
        'rsi': 35.0,
        'macd': 0.001,
        'price_volatility': 0.03,
        'order_book_imbalance': 0.2,
        'smart_money_confidence': 0.8,
        'overall_risk_score': 0.3
    }
    
    decision = await ai.make_trading_decision(test_features)
    print(f"AI决策结果: {decision}")


async def test_risk_management():
    """测试风险管理模块"""
    print("\n=== 测试风险管理模块 ===")
    
    rm = RiskManagementModule()
    
    # 创建测试信号
    test_signal = {
        'symbol': 'BTC/USDT',
        'decision': 'buy',
        'confidence': 0.8,
        'position_size': 0.1,
        'stop_loss': 0.05,
        'take_profit': 0.1
    }
    
    # 创建测试特征
    test_features = {
        'current_price': 30000.0,
        'price_volatility': 0.03,
        'order_book_imbalance': 0.2,
        'rsi': 35.0,
        'overall_risk_score': 0.3
    }
    
    assessment = await rm.evaluate_trading_signal(test_signal, test_features)
    print(f"风险评估结果: {assessment}")
    
    # 测试风险指标
    metrics = rm.get_risk_metrics()
    print(f"风险指标: {metrics}")


async def test_order_execution():
    """测试订单执行模块"""
    print("\n=== 测试订单执行模块 ===")
    
    oe = OrderExecutionModule()
    
    # 创建测试信号
    test_signal = {
        'symbol': 'BTC/USDT',
        'decision': 'buy',
        'position_size': 0.001,  # 小额测试
        'stop_loss': 0.05,
        'take_profit': 0.1
    }
    
    # 执行模拟订单
    result = await oe.execute_order(test_signal)
    print(f"订单执行结果: {result}")
    
    # 获取交易统计
    stats = oe.get_trading_statistics()
    print(f"交易统计: {stats}")


async def run_all_tests():
    """运行所有测试"""
    print("开始测试AI交易系统各模块...")
    
    # 设置测试环境
    setup_logging(log_level='DEBUG', log_dir='logs')
    
    try:
        await test_data_collection()
        await test_feature_engineering()
        await test_ai_decision()
        await test_risk_management()
        await test_order_execution()
        
        print("\n✅ 所有模块测试完成！")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run_all_tests())