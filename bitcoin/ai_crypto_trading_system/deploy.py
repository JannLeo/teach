#!/usr/bin/env python3
"""部署脚本

用于部署AI交易系统到生产环境
"""

import os
import subprocess
import shutil
import sys
from pathlib import Path


def create_deployment_package():
    """创建部署包"""
    print("创建部署包...")
    
    # 创建部署目录
    deploy_dir = Path("deployment")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    # 复制必要文件
    files_to_copy = [
        "main.py",
        "run.py",
        "requirements.txt",
        "config/config.yaml",
        "README.md",
        "modules/",
        "utils/",
        "web_interface/",
        "__init__.py"
    ]
    
    for item in files_to_copy:
        source = Path(item)
        dest = deploy_dir / item
        
        if source.is_file():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
        elif source.is_dir():
            shutil.copytree(source, dest, dirs_exist_ok=True)
    
    # 创建启动脚本
    startup_script = deploy_dir / "start.sh"
    startup_script.write_text("""#!/bin/bash
# AI交易系统启动脚本

echo "启动AI交易系统..."

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建必要的目录
mkdir -p logs data

# 启动系统
python run.py --mode production
""")
    startup_script.chmod(0o755)
    
    print(f"部署包已创建: {deploy_dir}")


def setup_production_environment():
    """设置生产环境"""
    print("设置生产环境...")
    
    # 创建生产配置
    prod_config = """# 生产环境配置
system:
  name: "AI Crypto Trading System"
  version: "1.0.0"
  mode: "production"
  log_level: "WARNING"

# 数据源配置
data_sources:
  exchange:
    testnet: false  # 生产环境使用真实交易
    
# 监控配置
monitoring:
  enabled: true
  web_interface_port: 80  # 使用80端口
"""
    
    with open("config/production.yaml", "w") as f:
        f.write(prod_config)
    
    print("生产环境配置已创建")


def create_docker_config():
    """创建Docker配置"""
    print("创建Docker配置...")
    
    dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# 复制文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 创建必要的目录
RUN mkdir -p logs data

# 暴露端口
EXPOSE 8081

# 启动应用
CMD ["python", "run.py", "--mode", "production"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    docker_compose_content = """version: '3.8'

services:
  ai-trading-system:
    build: .
    ports:
      - "8081:8081"
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
      - ./config:/app/config
    environment:
      - PYTHONPATH=/app
    restart: unless-stopped
    
  monitoring:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    restart: unless-stopped
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose_content)
    
    print("Docker配置已创建")


def create_systemd_service():
    """创建systemd服务配置"""
    print("创建systemd服务...")
    
    service_content = """[Unit]
Description=AI Crypto Trading System
After=network.target

[Service]
Type=simple
User=ai-trading
WorkingDirectory=/opt/ai-trading-system
ExecStart=/opt/ai-trading-system/venv/bin/python run.py --mode production
Restart=always
RestartSec=10
Environment=PYTHONPATH=/opt/ai-trading-system

[Install]
WantedBy=multi-user.target
"""
    
    with open("ai-trading-system.service", "w") as f:
        f.write(service_content)
    
    print("systemd服务配置已创建")
    print("安装命令:")
    print("sudo cp ai-trading-system.service /etc/systemd/system/")
    print("sudo systemctl daemon-reload")
    print("sudo systemctl enable ai-trading-system")
    print("sudo systemctl start ai-trading-system")


def create_monitoring_config():
    """创建监控配置"""
    print("创建监控配置...")
    
    # Prometheus配置
    prometheus_config = """global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ai-trading-system'
    static_configs:
      - targets: ['localhost:8081']
"""
    
    os.makedirs("monitoring", exist_ok=True)
    with open("monitoring/prometheus.yml", "w") as f:
        f.write(prometheus_config)
    
    # Grafana仪表板配置
    dashboard_json = {
        "dashboard": {
            "title": "AI Trading System",
            "panels": [
                {
                    "title": "系统状态",
                    "type": "stat",
                    "targets": [
                        {
                            "expr": "up{job=\"ai-trading-system\"}",
                            "legendFormat": "系统在线"
                        }
                    ]
                },
                {
                    "title": "CPU使用率",
                    "type": "graph",
                    "targets": [
                        {
                            "expr": "cpu_usage_percent",
                            "legendFormat": "CPU使用率"
                        }
                    ]
                }
            ]
        }
    }
    
    with open("monitoring/grafana-dashboard.json", "w") as f:
        import json
        json.dump(dashboard_json, f, indent=2)
    
    print("监控配置已创建")


def main():
    """主部署函数"""
    print("AI交易系统部署工具")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python deploy.py package    # 创建部署包")
        print("  python deploy.py docker     # 创建Docker配置")
        print("  python deploy.py systemd    # 创建systemd服务")
        print("  python deploy.py all        # 创建所有配置")
        return
    
    command = sys.argv[1]
    
    if command == "package":
        create_deployment_package()
    elif command == "docker":
        create_docker_config()
    elif command == "systemd":
        create_systemd_service()
    elif command == "monitoring":
        create_monitoring_config()
    elif command == "production":
        setup_production_environment()
    elif command == "all":
        create_deployment_package()
        create_docker_config()
        create_systemd_service()
        create_monitoring_config()
        setup_production_environment()
        print("\n所有部署配置已创建完成！")
        print("请查看生成的文件并根据需要修改配置。")
    else:
        print(f"未知命令: {command}")
        print("使用 'python deploy.py' 查看帮助")


if __name__ == "__main__":
    main()