"""监控与性能模块

负责系统监控、性能分析和实时状态展示
"""

import asyncio
import time
import psutil
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

from utils.logger import logger
from utils.config_loader import config_loader


class MonitoringModule:
    """监控与性能模块"""
    
    def __init__(self):
        """初始化监控模块"""
        self.monitoring_enabled = config_loader.get('monitoring.enabled', True)
        self.metrics_port = config_loader.get('monitoring.metrics_port', 8080)
        self.web_port = config_loader.get('monitoring.web_interface_port', 8081)
        self.update_interval = config_loader.get('monitoring.performance_update_interval', 300)
        
        # 性能指标
        self.performance_metrics = {
            'system_metrics': {},
            'trading_metrics': {},
            'module_metrics': {},
            'alert_history': []
        }
        
        # 模块引用
        self.modules = {}
        
        # 监控状态
        self.monitoring_active = False
        self.last_update_time = None
        
        # 警报配置
        self.alert_thresholds = {
            'cpu_usage': 80.0,
            'memory_usage': 80.0,
            'disk_usage': 90.0,
            'api_response_time': 5.0,
            'error_rate': 0.1,
            'daily_loss': 0.05
        }
        
    def register_module(self, name: str, module_instance):
        """注册模块实例
        
        Args:
            name: 模块名称
            module_instance: 模块实例
        """
        self.modules[name] = module_instance
        logger.info(f"模块 {name} 已注册到监控系统")
        
    async def start_monitoring(self):
        """启动监控"""
        if not self.monitoring_enabled:
            logger.info("监控功能已禁用")
            return
            
        self.monitoring_active = True
        logger.info("启动系统监控...")
        
        # 启动监控任务
        tasks = [
            self._monitor_system_resources(),
            self._monitor_trading_performance(),
            self._monitor_module_health(),
            self._perform_periodic_updates()
        ]
        
        await asyncio.gather(*tasks)
        
    async def stop_monitoring(self):
        """停止监控"""
        self.monitoring_active = False
        logger.info("系统监控已停止")
        
    async def _monitor_system_resources(self):
        """监控系统资源"""
        while self.monitoring_active:
            try:
                # CPU使用率
                cpu_percent = psutil.cpu_percent(interval=1)
                
                # 内存使用率
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                
                # 磁盘使用率
                disk = psutil.disk_usage('/')
                disk_percent = disk.percent
                
                # 网络连接
                network_connections = len(psutil.net_connections())
                
                # 系统负载
                load_average = psutil.getloadavg() if hasattr(psutil, 'getloadavg') else (0, 0, 0)
                
                # 更新系统指标
                self.performance_metrics['system_metrics'] = {
                    'timestamp': datetime.now().isoformat(),
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory_percent,
                    'memory_available_gb': memory.available / (1024**3),
                    'disk_percent': disk_percent,
                    'network_connections': network_connections,
                    'load_average': load_average,
                    'process_count': len(psutil.pids())
                }
                
                # 检查警报
                await self._check_system_alerts()
                
                await asyncio.sleep(10)  # 每10秒检查一次
                
            except Exception as e:
                logger.error(f"系统资源监控错误: {e}")
                await asyncio.sleep(30)
                
    async def _monitor_trading_performance(self):
        """监控交易性能"""
        while self.monitoring_active:
            try:
                trading_stats = {}
                
                # 从各模块收集交易统计
                if 'data_collection' in self.modules:
                    dc_stats = self.modules['data_collection'].get_all_data_keys()
                    trading_stats['data_sources'] = len(dc_stats)
                    
                if 'ai_decision' in self.modules:
                    ai_stats = self.modules['ai_decision'].get_trading_statistics()
                    trading_stats['ai_decisions'] = ai_stats
                    
                if 'risk_management' in self.modules:
                    risk_stats = self.modules['risk_management'].get_risk_metrics()
                    trading_stats['risk_metrics'] = risk_stats
                    
                if 'order_execution' in self.modules:
                    exec_stats = self.modules['order_execution'].get_trading_statistics()
                    trading_stats['order_execution'] = exec_stats
                    
                # 计算综合性能指标
                performance_summary = self._calculate_performance_summary(trading_stats)
                trading_stats['performance_summary'] = performance_summary
                
                # 更新交易指标
                self.performance_metrics['trading_metrics'] = trading_stats
                
                # 检查交易警报
                await self._check_trading_alerts(trading_stats)
                
                await asyncio.sleep(60)  # 每60秒更新一次
                
            except Exception as e:
                logger.error(f"交易性能监控错误: {e}")
                await asyncio.sleep(60)
                
    async def _monitor_module_health(self):
        """监控模块健康状态"""
        while self.monitoring_active:
            try:
                module_health = {}
                
                for module_name, module_instance in self.modules.items():
                    health_status = {
                        'status': 'healthy',
                        'last_check': datetime.now().isoformat(),
                        'uptime': time.time() - getattr(module_instance, 'start_time', time.time())
                    }
                    
                    # 检查模块特定指标
                    if hasattr(module_instance, 'get_health_status'):
                        custom_health = module_instance.get_health_status()
                        health_status.update(custom_health)
                        
                    module_health[module_name] = health_status
                    
                # 更新模块健康指标
                self.performance_metrics['module_metrics'] = module_health
                
                await asyncio.sleep(30)  # 每30秒检查一次
                
            except Exception as e:
                logger.error(f"模块健康监控错误: {e}")
                await asyncio.sleep(30)
                
    async def _perform_periodic_updates(self):
        """执行定期更新"""
        while self.monitoring_active:
            try:
                self.last_update_time = datetime.now()
                
                # 保存性能数据到文件
                await self._save_performance_data()
                
                # 清理旧的警报历史
                await self._cleanup_alert_history()
                
                logger.info(f"性能数据已更新: {self.last_update_time}")
                
                await asyncio.sleep(self.update_interval)  # 按配置间隔更新
                
            except Exception as e:
                logger.error(f"定期更新错误: {e}")
                await asyncio.sleep(self.update_interval)
                
    async def _check_system_alerts(self):
        """检查系统警报"""
        system_metrics = self.performance_metrics.get('system_metrics', {})
        
        alerts = []
        
        # CPU使用率警报
        cpu_usage = system_metrics.get('cpu_percent', 0)
        if cpu_usage > self.alert_thresholds['cpu_usage']:
            alerts.append({
                'type': 'system',
                'severity': 'warning',
                'message': f'CPU使用率过高: {cpu_usage:.1f}%',
                'timestamp': datetime.now().isoformat()
            })
            
        # 内存使用率警报
        memory_usage = system_metrics.get('memory_percent', 0)
        if memory_usage > self.alert_thresholds['memory_usage']:
            alerts.append({
                'type': 'system',
                'severity': 'warning',
                'message': f'内存使用率过高: {memory_usage:.1f}%',
                'timestamp': datetime.now().isoformat()
            })
            
        # 磁盘使用率警报
        disk_usage = system_metrics.get('disk_percent', 0)
        if disk_usage > self.alert_thresholds['disk_usage']:
            alerts.append({
                'type': 'system',
                'severity': 'critical',
                'message': f'磁盘使用率过高: {disk_usage:.1f}%',
                'timestamp': datetime.now().isoformat()
            })
            
        # 记录警报
        for alert in alerts:
            await self._record_alert(alert)
            
    async def _check_trading_alerts(self, trading_stats: Dict[str, Any]):
        """检查交易警报"""
        alerts = []
        
        # 检查风险指标
        risk_metrics = trading_stats.get('risk_metrics', {})
        if risk_metrics.get('circuit_breaker_status', False):
            alerts.append({
                'type': 'trading',
                'severity': 'critical',
                'message': '熔断机制已触发，交易暂停',
                'timestamp': datetime.now().isoformat()
            })
            
        # 检查日亏损
        daily_pnl = risk_metrics.get('daily_pnl', 0)
        if daily_pnl < -self.alert_thresholds['daily_loss']:
            alerts.append({
                'type': 'trading',
                'severity': 'warning',
                'message': f'日亏损过高: {daily_pnl:.4f}',
                'timestamp': datetime.now().isoformat()
            })
            
        # 检查错误率
        exec_stats = trading_stats.get('order_execution', {})
        if exec_stats.get('total_orders', 0) > 0:
            error_rate = 1 - exec_stats.get('success_rate', 1)
            if error_rate > self.alert_thresholds['error_rate']:
                alerts.append({
                    'type': 'trading',
                    'severity': 'warning',
                    'message': f'订单错误率过高: {error_rate:.2%}',
                    'timestamp': datetime.now().isoformat()
                })
                
        # 记录警报
        for alert in alerts:
            await self._record_alert(alert)
            
    async def _record_alert(self, alert: Dict[str, Any]):
        """记录警报
        
        Args:
            alert: 警报信息
        """
        self.performance_metrics['alert_history'].append(alert)
        
        # 根据严重程度记录日志
        if alert['severity'] == 'critical':
            logger.critical(f"[ALERT] {alert['message']}")
        elif alert['severity'] == 'warning':
            logger.warning(f"[ALERT] {alert['message']}")
        else:
            logger.info(f"[ALERT] {alert['message']}")
            
    def _calculate_performance_summary(self, trading_stats: Dict[str, Any]) -> Dict[str, Any]:
        """计算性能摘要
        
        Args:
            trading_stats: 交易统计
            
        Returns:
            性能摘要
        """
        summary = {
            'total_decisions': 0,
            'total_orders': 0,
            'success_rate': 0.0,
            'daily_pnl': 0.0,
            'risk_score': 0.0,
            'overall_health': 'unknown'
        }
        
        # 汇总各项统计
        if 'ai_decisions' in trading_stats:
            ai_stats = trading_stats['ai_decisions']
            summary['total_decisions'] = ai_stats.get('total_decisions', 0)
            
        if 'order_execution' in trading_stats:
            exec_stats = trading_stats['order_execution']
            summary['total_orders'] = exec_stats.get('total_orders', 0)
            summary['success_rate'] = exec_stats.get('success_rate', 0)
            
        if 'risk_metrics' in trading_stats:
            risk_stats = trading_stats['risk_metrics']
            summary['daily_pnl'] = risk_stats.get('daily_pnl', 0)
            
        # 计算综合健康状态
        health_score = 0.0
        health_factors = 0
        
        if summary['success_rate'] > 0:
            health_score += summary['success_rate']
            health_factors += 1
            
        if summary['daily_pnl'] >= 0:
            health_score += 1.0
            health_factors += 1
        elif summary['daily_pnl'] > -0.02:  # 亏损小于2%
            health_score += 0.5
            health_factors += 1
            
        if health_factors > 0:
            health_score = health_score / health_factors
            
        if health_score > 0.8:
            summary['overall_health'] = 'excellent'
        elif health_score > 0.6:
            summary['overall_health'] = 'good'
        elif health_score > 0.4:
            summary['overall_health'] = 'fair'
        else:
            summary['overall_health'] = 'poor'
            
        return summary
        
    async def _save_performance_data(self):
        """保存性能数据"""
        try:
            import json
            import os
            
            # 创建数据目录
            data_dir = 'data'
            os.makedirs(data_dir, exist_ok=True)
            
            # 保存性能数据
            filename = f"performance_{datetime.now().strftime('%Y%m%d')}.json"
            filepath = os.path.join(data_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.performance_metrics, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"保存性能数据错误: {e}")
            
    async def _cleanup_alert_history(self):
        """清理旧的警报历史"""
        try:
            alert_history = self.performance_metrics['alert_history']
            cutoff_time = datetime.now() - timedelta(days=7)  # 保留7天
            
            filtered_alerts = []
            for alert in alert_history:
                alert_time = datetime.fromisoformat(alert['timestamp'])
                if alert_time > cutoff_time:
                    filtered_alerts.append(alert)
                    
            self.performance_metrics['alert_history'] = filtered_alerts
            
        except Exception as e:
            logger.error(f"清理警报历史错误: {e}")
            
    def get_performance_summary(self) -> Dict[str, Any]:
        """获取性能摘要
        
        Returns:
            性能摘要字典
        """
        return {
            'system_metrics': self.performance_metrics.get('system_metrics', {}),
            'trading_metrics': self.performance_metrics.get('trading_metrics', {}),
            'module_metrics': self.performance_metrics.get('module_metrics', {}),
            'last_update': self.last_update_time.isoformat() if self.last_update_time else None,
            'monitoring_active': self.monitoring_active
        }
        
    def get_alert_history(self, severity: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """获取警报历史
        
        Args:
            severity: 严重程度筛选
            limit: 记录限制
            
        Returns:
            警报历史列表
        """
        alerts = self.performance_metrics.get('alert_history', [])
        
        if severity:
            alerts = [a for a in alerts if a.get('severity') == severity]
            
        return alerts[-limit:]
        
    def get_real_time_status(self) -> Dict[str, Any]:
        """获取实时状态
        
        Returns:
            实时状态字典
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'system_status': self.performance_metrics.get('system_metrics', {}),
            'trading_status': self.performance_metrics.get('trading_metrics', {}),
            'module_status': self.performance_metrics.get('module_metrics', {}),
            'active_alerts': len(self.performance_metrics.get('alert_history', [])),
            'uptime': time.time() - getattr(self, 'start_time', time.time())
        }