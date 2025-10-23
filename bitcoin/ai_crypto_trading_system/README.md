# AI驱动加密货币自动化交易系统

基于深度研究报告实现的分层模块化交易系统，采用管道-过滤器架构，实现端到端自动化交易流程。

## 项目概述

本项目是一个完全由AI驱动的加密货币自动化交易工具，旨在为个人投资者提供一个可定制、可理解的自动化交易平台。系统采用六大核心模块构成完整的数据处理到交易执行的端到端自动化流程。

### 核心特性

- **AI驱动决策**: 基于大型语言模型(DeepSeek API)的智能交易决策
- **模块化架构**: 采用管道-过滤器架构，高内聚低耦合
- **实时数据处理**: 支持多源数据采集和实时特征工程
- **智能风险管理**: 动态风险评估和仓位管理
- **Web界面监控**: 实时系统状态监控和性能分析
- **异步处理**: 支持高并发的异步数据处理

## 系统架构

### 六大核心模块

1. **数据采集模块 (Data Collection)**
   - 从交易所和GMGN等平台获取实时市场数据
   - 支持K线、订单簿、交易量等多维度数据
   - 集成聪明钱动向等链上信号

2. **特征工程模块 (Feature Engineering)**
   - 数据清洗和预处理
   - 技术指标计算(RSI, MACD, 布林带等)
   - 市场情绪特征提取

3. **AI决策模块 (AI Decision)**
   - 基于DeepSeek API的智能决策引擎
   - 结构化输出和规则验证
   - 置信度评估和决策解释

4. **风险管理模块 (Risk Management)**
   - 多维风险评估(市场、流动性、波动性等)
   - 动态仓位管理和止损策略
   - 熔断机制和亏损保护

5. **订单执行模块 (Order Execution)**
   - 支持多个交易所的API集成
   - 智能订单路由和执行监控
   - 交易历史和性能统计

6. **监控与性能模块 (Monitoring)**
   - 实时系统资源监控
   - 交易性能分析和警报
   - Web界面数据展示

## 安装和配置

### 环境要求

- Python 3.8+
- 支持异步的Python环境
- 网络连接(用于API调用)

### 安装步骤

1. 克隆项目
```bash
git clone <repository-url>
cd ai_crypto_trading_system
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置系统
```bash
cp config/config.yaml config/config.local.yaml
# 编辑 config/config.local.yaml 文件，配置API密钥等参数
```

### 配置文件说明

`config/config.yaml` 主要配置项：

```yaml
# 系统基本配置
system:
  name: "AI Crypto Trading System"
  version: "1.0.0"
  mode: "development"  # development, production, paper_trading

# 数据源配置
data_sources:
  exchange:
    api_key: "YOUR_EXCHANGE_API_KEY"
    secret_key: "YOUR_EXCHANGE_SECRET"
    testnet: true

# AI模型配置
ai_model:
  provider: "deepseek"
  api_key: "YOUR_DEEPSEEK_API_KEY"
  model_name: "deepseek-chat"

# 风险管理配置
risk_management:
  max_position_size: 0.1      # 最大仓位比例
  stop_loss_percentage: 0.05  # 止损百分比
  max_daily_loss: 0.02       # 最大日亏损比例
```

## 使用方法

### 启动系统

```bash
# 启动完整系统
python run.py

# 启动模拟交易模式
python run.py --mode paper

# 仅启动Web界面
python run.py --web-only

# 仅启动交易系统
python run.py --system-only

# 查看更多选项
python run.py --help
```

### Web界面访问

系统启动后，可以通过浏览器访问Web界面：
- 地址: `http://localhost:8081`
- 功能: 实时监控、性能分析、系统控制

### API接口

系统提供RESTful API接口：

- `GET /api/system/status` - 获取系统状态
- `GET /api/performance` - 获取性能数据
- `GET /api/trading/stats` - 获取交易统计
- `POST /api/control/shutdown` - 关闭系统

## 开发指南

### 添加新的数据源

1. 在 `modules/data_collection.py` 中添加新的数据获取方法
2. 更新特征工程模块以处理新数据
3. 在配置文件中添加相应的配置项

### 自定义AI决策逻辑

1. 修改 `modules/ai_decision.py` 中的决策模板
2. 调整提示词工程以优化决策质量
3. 添加新的验证规则

### 扩展风险管理策略

1. 在 `modules/risk_management.py` 中添加新的风险评估方法
2. 更新风险评分算法
3. 配置新的风险限制参数

## 安全注意事项

1. **API密钥安全**
   - 不要在代码中硬编码API密钥
   - 使用环境变量或配置文件
   - 定期轮换密钥

2. **交易安全**
   - 始终使用测试网进行测试
   - 设置合理的风险控制参数
   - 监控异常交易行为

3. **系统安全**
   - 限制Web界面访问权限
   - 定期更新依赖包
   - 监控系统资源使用

## 性能优化

### 系统调优

1. **异步优化**
   - 合理设置异步任务数量
   - 避免阻塞操作
   - 使用连接池管理API连接

2. **内存管理**
   - 定期清理历史数据
   - 限制缓冲区大小
   - 监控内存使用情况

3. **网络优化**
   - 使用本地缓存减少API调用
   - 实现请求重试机制
   - 监控网络延迟

### 监控指标

- 系统响应时间
- API调用成功率
- 交易执行延迟
- 资源使用情况

## 故障排除

### 常见问题

1. **API连接失败**
   - 检查API密钥配置
   - 验证网络连接
   - 查看API服务状态

2. **交易执行失败**
   - 检查账户余额
   - 验证交易对支持
   - 查看交易所限制

3. **系统性能问题**
   - 监控CPU和内存使用
   - 检查日志文件
   - 优化配置参数

### 日志分析

日志文件位于 `logs/` 目录：
- `trading_system_YYYYMMDD.log` - 主要系统日志
- 根据日志级别过滤信息
- 使用日志分析工具进行监控

## 贡献指南

欢迎提交Issue和Pull Request来改进项目：

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 创建Pull Request

### 代码规范

- 遵循PEP 8编码规范
- 添加适当的注释和文档
- 编写单元测试
- 保持代码整洁

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 免责声明

本项目仅用于教育和研究目的。加密货币交易存在高风险，可能导致资金损失。使用本系统进行交易前，请确保：

1. 充分了解相关风险
2. 仅在可承受损失范围内投资
3. 遵守当地法律法规
4. 进行充分的测试和验证

开发者不对因使用本系统造成的任何损失负责。

## 更新日志

### v1.0.0 (2025-10-23)
- 初始版本发布
- 实现六大核心模块
- 支持Web界面监控
- 集成DeepSeek AI决策
- 完整的风险管理系统