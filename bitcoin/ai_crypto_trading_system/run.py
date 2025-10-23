"""项目启动脚本

提供多种启动模式和配置选项
"""

import asyncio
import argparse
import sys
import os
from typing import Optional

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import AITradingSystem
from web_interface.app import WebInterface
from utils.logger import setup_logging
from utils.config_loader import config_loader


async def start_system(mode: str = 'full', web_only: bool = False, system_only: bool = False):
    """启动系统
    
    Args:
        mode: 启动模式 ('full', 'paper', 'backtest')
        web_only: 仅启动Web界面
        system_only: 仅启动交易系统
    """
    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    AI驱动加密货币交易系统                    ║
    ║                                                              ║
    ║  基于深度研究报告实现的分层模块化交易系统                   ║
    ║  采用管道-过滤器架构，支持端到端自动化交易                  ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    if web_only:
        # 仅启动Web界面
        await start_web_interface_only()
    elif system_only:
        # 仅启动交易系统
        await start_trading_system_only(mode)
    else:
        # 启动完整系统
        await start_full_system(mode)


async def start_trading_system_only(mode: str):
    """仅启动交易系统"""
    print("启动交易系统...")
    
    # 设置日志
    setup_logging(
        log_level=config_loader.get('system.log_level', 'INFO'),
        log_dir='logs'
    )
    
    # 创建并启动交易系统
    trading_system = AITradingSystem()
    
    try:
        await trading_system.start()
    except KeyboardInterrupt:
        print("\n接收到键盘中断，正在关闭系统...")
    except Exception as e:
        print(f"系统错误: {e}")
    finally:
        await trading_system.shutdown()


async def start_web_interface_only():
    """仅启动Web界面"""
    print("启动Web界面...")
    
    # 创建模拟的交易系统实例用于Web界面
    class MockTradingSystem:
        def get_system_status(self):
            return {
                'system_info': {
                    'name': 'AI Crypto Trading System',
                    'version': '1.0.0',
                    'mode': 'simulation'
                },
                'running': True,
                'modules': {
                    'data_collection': {'status': 'active'},
                    'ai_decision': {'status': 'active'},
                    'risk_management': {'status': 'warning'},
                    'order_execution': {'status': 'active'}
                }
            }
        
        def get_performance_summary(self):
            return {
                'system_metrics': {
                    'cpu_percent': 45.2,
                    'memory_percent': 67.8,
                    'disk_percent': 23.4
                },
                'trading_metrics': {
                    'data_sources': 3,
                    'performance_summary': {
                        'overall_health': 'good'
                    }
                }
            }
        
        def get_trading_statistics(self):
            return {
                'ai_decisions': {
                    'total_decisions': 150,
                    'buy_decisions': 45,
                    'sell_decisions': 30,
                    'hold_decisions': 75,
                    'average_confidence': 0.78
                },
                'risk_metrics': {
                    'daily_pnl': 125.50,
                    'circuit_breaker_status': False
                }
            }
    
    mock_system = MockTradingSystem()
    web_interface = WebInterface(mock_system)
    
    # 启动Web界面
    web_interface.run(debug=True)


async def start_full_system(mode: str):
    """启动完整系统"""
    print("启动完整AI交易系统...")
    
    # 设置日志
    setup_logging(
        log_level=config_loader.get('system.log_level', 'INFO'),
        log_dir='logs'
    )
    
    # 创建交易系统
    trading_system = AITradingSystem()
    
    # 创建Web界面
    web_interface = WebInterface(trading_system)
    
    # 启动任务
    tasks = [
        trading_system.start(),
        run_web_interface(web_interface)
    ]
    
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("\n接收到键盘中断，正在关闭系统...")
    except Exception as e:
        print(f"系统错误: {e}")
    finally:
        await trading_system.shutdown()


async def run_web_interface(web_interface):
    """运行Web界面"""
    import threading
    
    def run_web():
        web_interface.run(
            host='0.0.0.0',
            port=config_loader.get('monitoring.web_interface_port', 8081),
            debug=False
        )
    
    # 在后台线程中运行Web界面
    web_thread = threading.Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()
    
    # 保持异步循环运行
    while True:
        await asyncio.sleep(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='AI驱动加密货币交易系统启动脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
    python run.py                    # 启动完整系统
    python run.py --mode paper       # 启动模拟交易模式
    python run.py --web-only         # 仅启动Web界面
    python run.py --system-only      # 仅启动交易系统
    python run.py --help             # 显示帮助信息
        """
    )
    
    parser.add_argument(
        '--mode', '-m',
        choices=['full', 'paper', 'backtest'],
        default='full',
        help='启动模式: full(完整), paper(模拟), backtest(回测)'
    )
    
    parser.add_argument(
        '--web-only',
        action='store_true',
        help='仅启动Web界面'
    )
    
    parser.add_argument(
        '--system-only',
        action='store_true',
        help='仅启动交易系统'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='指定配置文件路径'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='设置日志级别'
    )
    
    args = parser.parse_args()
    
    # 检查参数冲突
    if args.web_only and args.system_only:
        print("错误: --web-only 和 --system-only 不能同时使用")
        sys.exit(1)
    
    # 运行系统
    try:
        asyncio.run(start_system(
            mode=args.mode,
            web_only=args.web_only,
            system_only=args.system_only
        ))
    except KeyboardInterrupt:
        print("\n程序已终止")
    except Exception as e:
        print(f"启动错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()