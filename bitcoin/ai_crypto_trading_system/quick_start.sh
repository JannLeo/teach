#!/bin/bash

# AI交易系统快速启动脚本

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    AI驱动加密货币交易系统                    ║"
echo "║                                                              ║"
echo "║                 快速启动和配置向导                          ║"
echo "╚══════════════════════════════════════════════════════════════╝"

# 检查Python版本
echo "检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "错误: Python3 未安装"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python版本: $PYTHON_VERSION"

# 创建虚拟环境
echo "创建虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "升级pip..."
pip install --upgrade pip

# 安装依赖
echo "安装项目依赖..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "警告: requirements.txt 不存在"
fi

# 创建必要目录
echo "创建必要目录..."
mkdir -p logs data config tests

# 检查配置文件
echo "检查配置文件..."
if [ ! -f "config/config.yaml" ]; then
    echo "创建默认配置文件..."
    cat > config/config.yaml << 'EOF'
# AI驱动加密货币自动化交易系统配置文件

# 系统基本配置
system:
  name: "AI Crypto Trading System"
  version: "1.0.0"
  mode: "development"  # development, production, paper_trading
  log_level: "INFO"
  
# 数据源配置
data_sources:
  gmgn:
    base_url: "https://gmgn.ai"
    api_key: ""  # 需要从GMGN获取
    enabled: true
    
  exchange:
    name: "binance"  # 支持多个交易所
    api_key: ""      # 交易所API密钥
    secret_key: ""   # 交易所密钥
    testnet: true    # 使用测试网
    
# AI模型配置
ai_model:
  provider: "deepseek"  # deepseek, openai等
  api_key: ""           # AI服务API密钥
  model_name: "deepseek-chat"
  max_tokens: 2000
  temperature: 0.1      # 降低随机性，提高决策一致性
  
# 风险管理配置
risk_management:
  max_position_size: 0.1      # 最大仓位比例
  stop_loss_percentage: 0.05  # 止损百分比
  take_profit_percentage: 0.1 # 止盈百分比
  max_daily_loss: 0.02       # 最大日亏损比例
  max_drawdown: 0.05         # 最大回撤比例
  
# 交易配置
trading:
  base_currency: "USDT"
  trading_pairs:
    - "BTC/USDT"
    - "ETH/USDT"
    - "SOL/USDT"
  order_type: "limit"  # limit, market
  order_timeout: 60    # 订单超时时间（秒）
  
# 监控配置
monitoring:
  enabled: true
  metrics_port: 8080
  web_interface_port: 8081
  performance_update_interval: 300  # 性能更新间隔（秒）
  
# 数据库配置
database:
  type: "sqlite"  # sqlite, mysql, postgresql
  connection_string: "sqlite:///data/trading_system.db"
  
# 通知配置
notifications:
  enabled: false
  telegram:
    bot_token: ""
    chat_id: ""
EOF
fi

# 设置文件权限
chmod +x run.py test_modules.py deploy.py

# 显示菜单
echo ""
echo "系统配置完成！请选择启动模式:"
echo ""
echo "1) 开发模式 (推荐测试)"
echo "2) 模拟交易模式"
echo "3) 生产模式"
echo "4) 仅Web界面"
echo "5) 运行模块测试"
echo "6) 退出"
echo ""

read -p "请选择 [1-6]: " choice

case $choice in
    1)
        echo "启动开发模式..."
        python run.py --mode development
        ;;
    2)
        echo "启动模拟交易模式..."
        python run.py --mode paper
        ;;
    3)
        echo "警告: 生产模式将使用真实资金交易！"
        read -p "确定要继续吗? (y/N): " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            python run.py --mode production
        else
            echo "已取消"
        fi
        ;;
    4)
        echo "启动Web界面..."
        python run.py --web-only
        ;;
    5)
        echo "运行模块测试..."
        python test_modules.py
        ;;
    6)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选择，退出"
        exit 1
        ;;
esac