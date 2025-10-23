"""Web界面应用

提供系统状态的Web界面展示
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import json
import os
from datetime import datetime
import logging

from utils.logger import logger
from utils.config_loader import config_loader


class WebInterface:
    """Web界面类"""
    
    def __init__(self, trading_system):
        """初始化Web界面
        
        Args:
            trading_system: 交易系统实例
        """
        self.trading_system = trading_system
        
        # 创建Flask应用
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'ai-trading-system-secret'
        
        # 创建SocketIO实例
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        # 设置路由
        self._setup_routes()
        
        # 设置WebSocket事件
        self._setup_socketio_events()
        
    def _setup_routes(self):
        """设置Web路由"""
        
        @self.app.route('/')
        def index():
            """主页"""
            return render_template('index.html')
            
        @self.app.route('/dashboard')
        def dashboard():
            """仪表板页面"""
            return render_template('dashboard.html')
            
        @self.app.route('/api/system/status')
        def system_status():
            """获取系统状态API"""
            try:
                status = self.trading_system.get_system_status()
                return jsonify(status)
            except Exception as e:
                logger.error(f"获取系统状态错误: {e}")
                return jsonify({'error': str(e)}), 500
                
        @self.app.route('/api/performance')
        def performance_data():
            """获取性能数据API"""
            try:
                performance = self.trading_system.get_performance_summary()
                return jsonify(performance)
            except Exception as e:
                logger.error(f"获取性能数据错误: {e}")
                return jsonify({'error': str(e)}), 500
                
        @self.app.route('/api/trading/stats')
        def trading_statistics():
            """获取交易统计API"""
            try:
                stats = self.trading_system.get_trading_statistics()
                return jsonify(stats)
            except Exception as e:
                logger.error(f"获取交易统计错误: {e}")
                return jsonify({'error': str(e)}), 500
                
        @self.app.route('/api/config')
        def system_config():
            """获取系统配置API"""
            try:
                config = {
                    'name': config_loader.get('system.name'),
                    'version': config_loader.get('system.version'),
                    'mode': config_loader.get('system.mode'),
                    'trading_pairs': config_loader.get_trading_pairs(),
                    'risk_parameters': config_loader.get_risk_parameters(),
                    'ai_model_config': config_loader.get_ai_model_config()
                }
                return jsonify(config)
            except Exception as e:
                logger.error(f"获取系统配置错误: {e}")
                return jsonify({'error': str(e)}), 500
                
        @self.app.route('/api/modules/<module_name>/data')
        def module_data(module_name):
            """获取模块数据API"""
            try:
                if module_name in self.trading_system.modules:
                    module = self.trading_system.modules[module_name]
                    if hasattr(module, 'get_real_time_status'):
                        data = module.get_real_time_status()
                    else:
                        data = {'status': 'active', 'name': module_name}
                    return jsonify(data)
                else:
                    return jsonify({'error': 'Module not found'}), 404
            except Exception as e:
                logger.error(f"获取模块数据错误: {e}")
                return jsonify({'error': str(e)}), 500
                
        @self.app.route('/api/control/shutdown', methods=['POST'])
        def shutdown_system():
            """关闭系统API"""
            try:
                # 异步关闭系统
                import threading
                def shutdown_thread():
                    asyncio.run(self.trading_system.shutdown())
                    os._exit(0)
                    
                thread = threading.Thread(target=shutdown_thread)
                thread.start()
                
                return jsonify({'message': '系统关闭中...'})
            except Exception as e:
                logger.error(f"关闭系统错误: {e}")
                return jsonify({'error': str(e)}), 500
                
    def _setup_socketio_events(self):
        """设置WebSocket事件"""
        
        @self.socketio.on('connect')
        def handle_connect():
            """处理客户端连接"""
            logger.info(f"客户端已连接: {request.sid}")
            emit('connected', {'message': '已连接到交易系统'})
            
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """处理客户端断开"""
            logger.info(f"客户端已断开: {request.sid}")
            
        @self.socketio.on('subscribe_metrics')
        def handle_subscribe_metrics(data):
            """订阅指标更新"""
            logger.info(f"客户端 {request.sid} 订阅指标: {data}")
            # 这里可以添加订阅逻辑
            
        @self.socketio.on('unsubscribe_metrics')
        def handle_unsubscribe_metrics(data):
            """取消订阅指标更新"""
            logger.info(f"客户端 {request.sid} 取消订阅指标: {data}")
            # 这里可以添加取消订阅逻辑
            
    def start_real_time_updates(self):
        """启动实时更新推送"""
        async def update_loop():
            while True:
                try:
                    # 获取最新数据
                    status = self.trading_system.get_system_status()
                    performance = self.trading_system.get_performance_summary()
                    stats = self.trading_system.get_trading_statistics()
                    
                    # 推送更新
                    self.socketio.emit('system_update', {
                        'status': status,
                        'performance': performance,
                        'statistics': stats,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    await asyncio.sleep(5)  # 每5秒更新一次
                    
                except Exception as e:
                    logger.error(f"实时更新错误: {e}")
                    await asyncio.sleep(10)
                    
        # 启动更新任务
        asyncio.create_task(update_loop())
        
    def run(self, host='0.0.0.0', port=None, debug=False):
        """运行Web界面
        
        Args:
            host: 主机地址
            port: 端口号
            debug: 调试模式
        """
        if port is None:
            port = config_loader.get('monitoring.web_interface_port', 8081)
            
        # 启动实时更新
        self.start_real_time_updates()
        
        # 运行应用
        logger.info(f"启动Web界面: http://{host}:{port}")
        self.socketio.run(self.app, host=host, port=port, debug=debug)