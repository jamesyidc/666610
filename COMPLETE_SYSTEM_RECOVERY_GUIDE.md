# 完整系统恢复指南
## Complete System Recovery Guide for 21 Subsystems

**备份时间 / Backup Time:** 2024-12-24 14:00:03  
**系统版本 / System Version:** v2.2  
**备份大小 / Backup Size:** 3.1GB  
**Git Commit:** b9791e1

---

## 目录 / Table of Contents

1. [系统概述 / System Overview](#系统概述)
2. [前置要求 / Prerequisites](#前置要求)
3. [21个子系统详细恢复指南 / 21 Subsystems Recovery Guide](#21个子系统详细恢复指南)
4. [数据库表映射关系 / Database Table Mappings](#数据库表映射关系)
5. [完整恢复步骤 / Complete Recovery Steps](#完整恢复步骤)
6. [验证清单 / Verification Checklist](#验证清单)

---

## 系统概述 / System Overview

本备份包含完整的加密货币交易监控系统，包括21个独立子系统，用于实时数据采集、信号分析、智能通知和可视化展示。

### 技术栈 / Technology Stack
- **后端 / Backend:** Python 3.12+ (Flask, SQLAlchemy)
- **数据库 / Database:** SQLite3 (4个数据库文件)
- **进程管理 / Process Manager:** PM2
- **前端 / Frontend:** HTML5, JavaScript, Bootstrap, Chart.js
- **外部服务 / External Services:** Telegram Bot, Google Drive API

### 系统架构 / System Architecture
```
├── Flask Web Application (flask-app)
├── Data Collection Layer (10+ collectors)
├── Signal Processing Layer (telegram-notifier)
├── Database Layer (4 SQLite databases)
├── Monitoring & Maintenance (3 monitors)
└── External Integration (Google Drive, Telegram)
```

---

## 前置要求 / Prerequisites

### 1. 系统环境 / System Environment
```bash
# 操作系统 / Operating System
Ubuntu 20.04+ / Debian 11+ / RHEL 8+

# Python
Python 3.12 or higher

# Node.js (for PM2)
Node.js 18+ and npm 9+

# 数据库 / Database
SQLite3 3.31+

# 系统工具 / System Tools
git, curl, wget, tar, gzip
```

### 2. 必需的包 / Required Packages
```bash
# 安装 Python 依赖 / Install Python dependencies
pip install -r requirements.txt

# 主要依赖包括 / Key dependencies include:
# - Flask 3.0.0
# - flask-socketio 5.3.5
# - requests 2.31.0
# - ccxt 4.2.25
# - google-api-python-client 2.111.0
# - python-telegram-bot 20.7
```

### 3. PM2 安装 / PM2 Installation
```bash
npm install -g pm2
pm2 startup
```

### 4. 网络要求 / Network Requirements
- 外部API访问权限（Binance, OKX, Gate.io等交易所）
- Telegram Bot API 访问
- Google Drive API 访问（可选）

---

## 21个子系统详细恢复指南 / 21 Subsystems Recovery Guide

### 【1. 历史数据查询系统】 Historical Data Query System

#### 功能描述 / Description
提供Web界面查询历史K线数据、技术指标、交易信号等历史记录

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `app.py` - Flask主应用（核心路由）
- `templates/history.html` - 历史查询主页
- `templates/sar_history.html` - SAR历史查询页
- `templates/support_resistance_history.html` - 支撑压力历史页
- `templates/indicators_history.html` - 指标历史页

**数据库表 / Database Tables:**
- `crypto_data.db`:
  - `binance_1m_data` - 1分钟K线历史数据
  - `sar_slope_data` - SAR斜率历史数据
  - `support_resistance_data` - 支撑压力线历史数据
  - `indicators_data` - 技术指标历史数据
  - `depth_chart_data` - 深度图历史数据
  - `position_data` - 位置系统历史数据

**PM2进程 / PM2 Process:**
- `flask-app` (ID: 20)

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复源代码
cp source_code/app.py /home/user/webapp/
cp templates/history*.html /home/user/webapp/templates/
cp templates/sar_history.html /home/user/webapp/templates/
cp templates/support_resistance_history.html /home/user/webapp/templates/
cp templates/indicators_history.html /home/user/webapp/templates/

# 2. 恢复数据库
cp databases/crypto_data.db /home/user/webapp/

# 3. 验证数据库表
sqlite3 /home/user/webapp/crypto_data.db "SELECT count(*) FROM binance_1m_data;"

# 4. 重启Flask应用
pm2 restart flask-app

# 5. 访问测试
curl http://localhost:5000/history
```

#### 验证清单 / Verification
- [ ] 历史查询页面可访问
- [ ] 能够查询不同时间范围的数据
- [ ] 图表正常显示
- [ ] 数据分页功能正常

---

### 【2. 交易信号监控系统】 Trading Signal Monitoring System

#### 功能描述 / Description
实时监控交易信号，包括抄底信号、逃顶信号、双重信号等

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `telegram_notifier.py` - Telegram消息推送核心逻辑
- `app.py` - 信号查询API接口
- `templates/signals.html` - 信号监控页面
- `templates/support_resistance.html` - 支撑压力实时页面

**配置文件 / Config Files:**
- `configs/telegram_config.json` - Telegram Bot配置
- `configs/.env` - 环境变量配置

**数据库表 / Database Tables:**
- `crypto_data.db`:
  - `support_resistance_data` - 支撑压力实时数据
  - `support_resistance_snapshot` - 支撑压力快照
  - `signal_history` - 信号历史记录

**PM2进程 / PM2 Process:**
- `telegram-notifier` (ID: 13)
- `flask-app` (ID: 20)

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复源代码
cp source_code/telegram_notifier.py /home/user/webapp/

# 2. 恢复配置文件
cp configs/telegram_config.json /home/user/webapp/
cp configs/.env /home/user/webapp/

# 3. 恢复模板
cp templates/signals.html /home/user/webapp/templates/
cp templates/support_resistance.html /home/user/webapp/templates/

# 4. 启动服务
pm2 start telegram_notifier.py --name telegram-notifier

# 5. 查看日志验证
pm2 logs telegram-notifier --lines 50
```

#### 信号类型说明 / Signal Types
1. **强势抄底信号 (Strong Buy Signal)**
   - 条件: 支撑线S1 >= 8 AND 支撑线S2 >= 8
   
2. **最强逃顶信号 (Strong Sell Signal)**
   - 条件: 压力线R1 >= 1 AND 压力线R2 >= 1 AND (R1+R2) >= 8
   
3. **双重抄底信号 (Double Buy Signal)**
   - 条件: 同时触碰S1和S2，且数量 >= 配置阈值
   
4. **双重逃顶信号 (Double Sell Signal)**
   - 条件: 同时触碰R1和R2，且数量 >= 配置阈值

#### 验证清单 / Verification
- [ ] Telegram Bot连接正常
- [ ] 信号检测逻辑运行正常
- [ ] 消息推送成功
- [ ] 冷却时间机制正常

---

### 【3. 恐慌清洗指数系统】 Panic Wash Index System

#### 功能描述 / Description
监控市场恐慌情绪和清洗指数，用于判断市场超卖超买状态

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `panic_wash_collector.py` - 恐慌清洗数据采集器
- `templates/panic_wash.html` - 恐慌清洗指数页面
- `templates/panic_wash_history.html` - 历史数据页面

**数据库表 / Database Tables:**
- `crypto_data.db`:
  - `panic_wash_index` - 恐慌清洗指数数据

**PM2进程 / PM2 Process:**
- `panic-wash-collector` (ID: 11)

#### 数据字段 / Data Fields
```sql
CREATE TABLE panic_wash_index (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    panic_index REAL,        -- 恐慌指数 (0-100)
    wash_index REAL,          -- 清洗指数 (0-100)
    market_sentiment TEXT,    -- 市场情绪 (extreme_fear, fear, neutral, greed, extreme_greed)
    volume_ratio REAL,        -- 成交量比率
    price_change_24h REAL,    -- 24小时涨跌幅
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复采集器
cp source_code/panic_wash_collector.py /home/user/webapp/

# 2. 恢复页面模板
cp templates/panic_wash*.html /home/user/webapp/templates/

# 3. 启动采集器
pm2 start panic_wash_collector.py --name panic-wash-collector

# 4. 验证数据采集
pm2 logs panic-wash-collector --lines 30
```

#### 验证清单 / Verification
- [ ] 采集器正常运行
- [ ] 数据库有新数据写入
- [ ] 页面能显示最新指数
- [ ] 历史数据查询正常

---

### 【4. 比价系统】 Price Comparison System

#### 功能描述 / Description
对比多个交易所的价格差异，发现套利机会

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `price_comparison_collector.py` - 价格对比采集器
- `templates/price_comparison.html` - 价格对比页面

**数据库表 / Database Tables:**
- `crypto_data.db`:
  - `price_comparison_data` - 价格对比数据

**PM2进程 / PM2 Process:**
- `price-comparison-collector` (ID: 12)

#### 数据字段 / Data Fields
```sql
CREATE TABLE price_comparison_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    binance_price REAL,
    okx_price REAL,
    gate_price REAL,
    bybit_price REAL,
    max_spread_percentage REAL,  -- 最大价差百分比
    best_buy_exchange TEXT,       -- 最佳买入交易所
    best_sell_exchange TEXT,      -- 最佳卖出交易所
    arbitrage_profit REAL,        -- 套利利润率
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复采集器
cp source_code/price_comparison_collector.py /home/user/webapp/

# 2. 恢复页面
cp templates/price_comparison.html /home/user/webapp/templates/

# 3. 启动采集器
pm2 start price_comparison_collector.py --name price-comparison-collector

# 4. 验证采集
pm2 logs price-comparison-collector
```

#### 验证清单 / Verification
- [ ] 多交易所价格采集正常
- [ ] 价差计算准确
- [ ] 套利机会识别正常
- [ ] 实时更新正常

---

### 【5. 星星系统】 Star Rating System

#### 功能描述 / Description
基于多维度评分给币种打星级，用于筛选优质交易标的

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `calculate_count_score.py` - 评分计算逻辑
- `calculate_priority.py` - 优先级计算
- `templates/star_rating.html` - 星级展示页面

**数据库表 / Database Tables:**
- `crypto_data.db`:
  - `star_ratings` - 星级评分数据
  - `count_score_data` - 计数评分数据

**PM2进程 / PM2 Process:**
- `flask-app` (ID: 20)

#### 评分维度 / Rating Dimensions
1. **技术指标得分** - RSI, MACD, KDJ等指标综合
2. **成交量得分** - 成交量变化趋势
3. **深度图得分** - 买卖盘深度分析
4. **位置得分** - 价格相对高低位置
5. **支撑压力得分** - 关键位支撑压力强度

#### 数据字段 / Data Fields
```sql
CREATE TABLE star_ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    total_score REAL,             -- 总分 (0-100)
    star_level INTEGER,           -- 星级 (1-5星)
    technical_score REAL,         -- 技术指标得分
    volume_score REAL,            -- 成交量得分
    depth_score REAL,             -- 深度得分
    position_score REAL,          -- 位置得分
    support_resistance_score REAL, -- 支撑压力得分
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复评分脚本
cp source_code/calculate_count_score.py /home/user/webapp/
cp source_code/calculate_priority.py /home/user/webapp/

# 2. 恢复页面
cp templates/star_rating.html /home/user/webapp/templates/

# 3. 执行评分计算
cd /home/user/webapp && python3 calculate_count_score.py

# 4. 重启Flask查看结果
pm2 restart flask-app
```

#### 验证清单 / Verification
- [ ] 评分计算脚本正常运行
- [ ] 数据库有评分数据
- [ ] 页面显示星级正常
- [ ] 排序功能正常

---

### 【6. 币种池系统】 Coin Pool System

#### 功能描述 / Description
管理交易币种池，动态添加/移除币种，维护币种列表

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `manage_coin_pool.py` - 币种池管理脚本
- `coin_pool_config.json` - 币种池配置文件
- `templates/coin_pool.html` - 币种池管理页面

**数据库表 / Database Tables:**
- `crypto_data.db`:
  - `coin_pool` - 币种池数据

**PM2进程 / PM2 Process:**
- `flask-app` (ID: 20)

#### 数据字段 / Data Fields
```sql
CREATE TABLE coin_pool (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL UNIQUE,
    exchange TEXT DEFAULT 'binance',
    status TEXT DEFAULT 'active',     -- active, inactive, monitoring
    added_date TEXT DEFAULT CURRENT_TIMESTAMP,
    market_cap REAL,
    daily_volume REAL,
    price REAL,
    priority_level INTEGER DEFAULT 1, -- 1-5 (1最高)
    notes TEXT,
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复管理脚本
cp source_code/manage_coin_pool.py /home/user/webapp/

# 2. 恢复配置文件
cp configs/coin_pool_config.json /home/user/webapp/

# 3. 恢复页面
cp templates/coin_pool.html /home/user/webapp/templates/

# 4. 验证币种池数据
sqlite3 /home/user/webapp/crypto_data.db "SELECT * FROM coin_pool WHERE status='active';"
```

#### 验证清单 / Verification
- [ ] 币种池数据完整
- [ ] 管理页面功能正常
- [ ] 添加/删除币种功能正常
- [ ] 币种状态更新正常

---

### 【7. 实时市场原始数据】 Real-time Market Raw Data

#### 功能描述 / Description
通过WebSocket实时采集交易所原始市场数据（K线、深度、成交）

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `websocket_collector.py` - WebSocket采集器
- `realtime_market_collector.py` - 实时市场数据采集

**数据库表 / Database Tables:**
- `crypto_data.db`:
  - `binance_1m_data` - 实时1分钟K线
  - `realtime_trades` - 实时成交数据
  - `realtime_orderbook` - 实时订单簿

**PM2进程 / PM2 Process:**
- `websocket-collector` (ID: 2)

#### 数据字段 / Data Fields
```sql
-- 1分钟K线数据
CREATE TABLE binance_1m_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    volume REAL NOT NULL,
    quote_volume REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, timestamp)
);

-- 实时成交数据
CREATE TABLE realtime_trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    trade_id TEXT NOT NULL,
    price REAL NOT NULL,
    quantity REAL NOT NULL,
    timestamp INTEGER NOT NULL,
    is_buyer_maker BOOLEAN,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 实时订单簿
CREATE TABLE realtime_orderbook (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    bids TEXT NOT NULL,  -- JSON格式买单
    asks TEXT NOT NULL,  -- JSON格式卖单
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复WebSocket采集器
cp source_code/websocket_collector.py /home/user/webapp/
cp source_code/realtime_market_collector.py /home/user/webapp/

# 2. 启动WebSocket采集
pm2 start websocket_collector.py --name websocket-collector

# 3. 验证数据采集
pm2 logs websocket-collector --lines 50

# 4. 检查数据库写入
sqlite3 /home/user/webapp/crypto_data.db "SELECT count(*) FROM binance_1m_data WHERE timestamp > strftime('%s', 'now', '-1 hour');"
```

#### 验证清单 / Verification
- [ ] WebSocket连接稳定
- [ ] K线数据实时更新
- [ ] 成交数据正常采集
- [ ] 订单簿数据完整

---

### 【8. 数据采集监控】 Data Collection Monitoring

#### 功能描述 / Description
监控所有数据采集器状态，自动重启失败的采集器，记录采集统计

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `collector_monitor.py` - 采集器监控主程序
- `auto_restart_collectors.py` - 自动重启脚本
- `templates/collector_status.html` - 监控状态页面

**数据库表 / Database Tables:**
- `crypto_data.db`:
  - `collector_status` - 采集器状态表
  - `collector_stats` - 采集统计表

**PM2进程 / PM2 Process:**
- `collector-monitor` (ID: 9)

#### 数据字段 / Data Fields
```sql
CREATE TABLE collector_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    collector_name TEXT NOT NULL UNIQUE,
    status TEXT DEFAULT 'unknown',    -- running, stopped, error, restarting
    last_heartbeat TEXT,
    last_data_time TEXT,
    error_message TEXT,
    restart_count INTEGER DEFAULT 0,
    uptime_seconds INTEGER,
    memory_usage REAL,
    cpu_usage REAL,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE collector_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    collector_name TEXT NOT NULL,
    date TEXT NOT NULL,
    records_collected INTEGER DEFAULT 0,
    errors_count INTEGER DEFAULT 0,
    avg_latency_ms REAL,
    success_rate REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(collector_name, date)
);
```

#### 监控的采集器列表 / Monitored Collectors
1. `websocket-collector` - WebSocket实时数据
2. `crypto-index-collector` - OKX加密指数
3. `support-resistance-collector` - 支撑压力线
4. `position-system-collector` - 位置系统
5. `v1v2-collector` - V1V2成交数据
6. `panic-wash-collector` - 恐慌清洗指数
7. `price-comparison-collector` - 价格对比
8. `fund-monitor-collector` - 资金监控
9. `sar-slope-collector` - SAR斜率

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复监控脚本
cp source_code/collector_monitor.py /home/user/webapp/
cp source_code/auto_restart_collectors.py /home/user/webapp/

# 2. 恢复监控页面
cp templates/collector_status.html /home/user/webapp/templates/

# 3. 启动监控服务
pm2 start collector_monitor.py --name collector-monitor

# 4. 查看监控状态
pm2 logs collector-monitor --lines 30

# 5. 访问监控页面
curl http://localhost:5000/collector_status
```

#### 验证清单 / Verification
- [ ] 监控服务正常运行
- [ ] 能检测到所有采集器状态
- [ ] 自动重启功能正常
- [ ] 监控页面显示正确

---

### 【9. 深度图得分】 Depth Chart Scoring

#### 功能描述 / Description
分析订单簿深度图，计算买卖盘强度得分，用于判断价格支撑压力

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `depth_chart_analyzer.py` - 深度图分析器
- `calculate_depth_score.py` - 深度得分计算
- `templates/depth_score.html` - 深度得分页面

**数据库表 / Database Tables:**
- `crypto_data.db`:
  - `depth_chart_data` - 深度图原始数据
  - `depth_score_data` - 深度得分数据

**PM2进程 / PM2 Process:**
- `flask-app` (ID: 20)

#### 数据字段 / Data Fields
```sql
CREATE TABLE depth_chart_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    bids_json TEXT NOT NULL,          -- 买单深度JSON
    asks_json TEXT NOT NULL,          -- 卖单深度JSON
    bid_total_volume REAL,            -- 买单总量
    ask_total_volume REAL,            -- 卖单总量
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, timestamp)
);

CREATE TABLE depth_score_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    buy_strength_score REAL,          -- 买盘强度得分 (0-100)
    sell_strength_score REAL,         -- 卖盘强度得分 (0-100)
    depth_balance_score REAL,         -- 深度平衡得分 (0-100)
    support_level REAL,               -- 支撑位价格
    resistance_level REAL,            -- 压力位价格
    bid_ask_ratio REAL,               -- 买卖比
    total_score REAL,                 -- 综合得分
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### 评分算法 / Scoring Algorithm
```python
# 买盘强度得分
buy_strength = (bid_volume_total / (bid_volume_total + ask_volume_total)) * 100

# 卖盘强度得分
sell_strength = (ask_volume_total / (bid_volume_total + ask_volume_total)) * 100

# 深度平衡得分 (越接近50越平衡)
balance_score = 100 - abs(50 - buy_strength)

# 综合得分
total_score = (buy_strength * 0.4 + sell_strength * 0.4 + balance_score * 0.2)
```

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复分析脚本
cp source_code/depth_chart_analyzer.py /home/user/webapp/
cp source_code/calculate_depth_score.py /home/user/webapp/

# 2. 恢复页面
cp templates/depth_score.html /home/user/webapp/templates/

# 3. 执行得分计算
cd /home/user/webapp && python3 calculate_depth_score.py

# 4. 验证数据
sqlite3 /home/user/webapp/crypto_data.db "SELECT symbol, total_score FROM depth_score_data ORDER BY total_score DESC LIMIT 10;"
```

#### 验证清单 / Verification
- [ ] 深度数据采集正常
- [ ] 得分计算脚本运行正常
- [ ] 得分数据存入数据库
- [ ] 页面显示得分排行

---

### 【10. 深度图可视化】 Depth Chart Visualization

#### 功能描述 / Description
Web界面可视化展示订单簿深度图，实时更新买卖盘分布

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `app.py` - 深度图API接口
- `templates/depth_chart.html` - 深度图可视化页面
- `static/js/depth_chart.js` - 深度图图表逻辑

**数据库表 / Database Tables:**
- `crypto_data.db`:
  - `depth_chart_data` - 深度图数据

**PM2进程 / PM2 Process:**
- `flask-app` (ID: 20)

#### 页面功能 / Page Features
1. **实时深度图** - Chart.js绘制买卖盘分布
2. **动态更新** - WebSocket推送最新深度
3. **多币种切换** - 下拉选择不同币种
4. **数据统计** - 显示买卖盘总量、买卖比等

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复页面和JS
cp templates/depth_chart.html /home/user/webapp/templates/
cp static/js/depth_chart.js /home/user/webapp/static/js/

# 2. 确保Flask运行
pm2 restart flask-app

# 3. 访问深度图页面
curl http://localhost:5000/depth_chart

# 4. 测试WebSocket连接
# 浏览器访问并检查实时更新
```

#### 验证清单 / Verification
- [ ] 页面加载正常
- [ ] 深度图渲染正确
- [ ] 实时数据更新正常
- [ ] 币种切换功能正常

---

### 【11. 平均分页面】 Average Score Page

#### 功能描述 / Description
展示所有币种的综合评分平均值，用于判断整体市场强弱

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `app.py` - 平均分计算API
- `templates/average_score.html` - 平均分展示页面
- `calculate_average_score.py` - 平均分计算脚本

**数据库表 / Database Tables:**
- `crypto_data.db`:
  - `average_score_data` - 平均分历史数据

**PM2进程 / PM2 Process:**
- `flask-app` (ID: 20)

#### 数据字段 / Data Fields
```sql
CREATE TABLE average_score_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL UNIQUE,
    total_coins INTEGER,                -- 总币种数
    avg_total_score REAL,               -- 平均总分
    avg_technical_score REAL,           -- 平均技术得分
    avg_volume_score REAL,              -- 平均成交量得分
    avg_depth_score REAL,               -- 平均深度得分
    market_sentiment TEXT,              -- 市场情绪 (strong, weak, neutral)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复计算脚本
cp source_code/calculate_average_score.py /home/user/webapp/

# 2. 恢复页面
cp templates/average_score.html /home/user/webapp/templates/

# 3. 执行计算
cd /home/user/webapp && python3 calculate_average_score.py

# 4. 访问页面
curl http://localhost:5000/average_score
```

#### 验证清单 / Verification
- [ ] 平均分计算正确
- [ ] 历史数据保存正常
- [ ] 页面图表显示正确
- [ ] 市场情绪判断准确

---

### 【12. OKEx加密指数】 OKEx Crypto Index

#### 功能描述 / Description
采集OKEx交易所的加密货币指数数据

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `crypto_index_collector.py` - OKX指数采集器
- `templates/crypto_index.html` - 指数展示页面

**数据库表 / Database Tables:**
- `crypto_data.db`:
  - `crypto_index_data` - 加密指数数据

**PM2进程 / PM2 Process:**
- `crypto-index-collector` (ID: 8)

#### 数据字段 / Data Fields
```sql
CREATE TABLE crypto_index_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    index_name TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    index_value REAL NOT NULL,
    change_24h REAL,
    change_percentage_24h REAL,
    volume_24h REAL,
    high_24h REAL,
    low_24h REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(index_name, timestamp)
);
```

#### 支持的指数 / Supported Indices
- `BTC-INDEX` - 比特币指数
- `ETH-INDEX` - 以太坊指数
- `CRYPTO-100` - 加密货币100指数
- `DEFI-INDEX` - DeFi指数

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复采集器
cp source_code/crypto_index_collector.py /home/user/webapp/

# 2. 恢复页面
cp templates/crypto_index.html /home/user/webapp/templates/

# 3. 启动采集器
pm2 start crypto_index_collector.py --name crypto-index-collector

# 4. 查看日志
pm2 logs crypto-index-collector --lines 30
```

#### 验证清单 / Verification
- [ ] 采集器连接OKX API正常
- [ ] 指数数据采集正常
- [ ] 数据库写入正常
- [ ] 页面显示最新指数

---

### 【13. 位置系统】 Position System

#### 功能描述 / Description
计算币种当前价格在历史价格区间中的相对位置（高位、中位、低位）

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `position_system_collector.py` - 位置系统采集器
- `templates/position_system.html` - 位置展示页面
- `calculate_position.py` - 位置计算脚本

**数据库表 / Database Tables:**
- `crypto_data.db`:
  - `position_data` - 位置系统数据

**PM2进程 / PM2 Process:**
- `position-system-collector` (ID: 7)

#### 数据字段 / Data Fields
```sql
CREATE TABLE position_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    current_price REAL NOT NULL,
    high_7d REAL,                    -- 7天最高价
    low_7d REAL,                     -- 7天最低价
    high_30d REAL,                   -- 30天最高价
    low_30d REAL,                    -- 30天最低价
    position_7d REAL,                -- 7天位置 (0-100)
    position_30d REAL,               -- 30天位置 (0-100)
    position_level TEXT,             -- 位置等级 (low, medium, high)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, timestamp)
);
```

#### 位置计算公式 / Position Calculation
```python
# 7天位置
position_7d = ((current_price - low_7d) / (high_7d - low_7d)) * 100

# 30天位置
position_30d = ((current_price - low_30d) / (high_30d - low_30d)) * 100

# 位置等级
if position < 30:
    level = 'low'      # 低位 - 适合买入
elif position < 70:
    level = 'medium'   # 中位 - 观望
else:
    level = 'high'     # 高位 - 考虑卖出
```

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复采集器
cp source_code/position_system_collector.py /home/user/webapp/
cp source_code/calculate_position.py /home/user/webapp/

# 2. 恢复页面
cp templates/position_system.html /home/user/webapp/templates/

# 3. 启动采集器
pm2 start position_system_collector.py --name position-system-collector

# 4. 验证数据
sqlite3 /home/user/webapp/crypto_data.db "SELECT symbol, current_price, position_7d, position_level FROM position_data ORDER BY position_7d LIMIT 10;"
```

#### 验证清单 / Verification
- [ ] 位置数据采集正常
- [ ] 位置计算准确
- [ ] 位置等级分类正确
- [ ] 页面展示低位币种

---

### 【14. 支撑压力线系统】 Support & Resistance System

#### 功能描述 / Description
识别关键支撑位和压力位，监控价格触碰情况，生成交易信号

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `support_resistance_collector.py` - 支撑压力采集器
- `support_resistance_snapshot_collector.py` - 快照采集器
- `templates/support_resistance.html` - 实时监控页面
- `templates/support_resistance_history.html` - 历史页面

**数据库表 / Database Tables:**
- `crypto_data.db`:
  - `support_resistance_data` - 支撑压力实时数据
  - `support_resistance_snapshot` - 历史快照

**PM2进程 / PM2 Process:**
- `support-resistance-collector` (ID: 5)
- `support-resistance-snapshot-collector` (ID: 6)

#### 数据字段 / Data Fields
```sql
CREATE TABLE support_resistance_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    current_price REAL NOT NULL,
    support_s1 REAL,                 -- 支撑线S1
    support_s2 REAL,                 -- 支撑线S2
    resistance_r1 REAL,              -- 压力线R1
    resistance_r2 REAL,              -- 压力线R2
    s1_touch_count INTEGER DEFAULT 0, -- S1触碰次数
    s2_touch_count INTEGER DEFAULT 0, -- S2触碰次数
    r1_touch_count INTEGER DEFAULT 0, -- R1触碰次数
    r2_touch_count INTEGER DEFAULT 0, -- R2触碰次数
    signal_type TEXT,                 -- 信号类型 (buy, sell, neutral)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, timestamp)
);

CREATE TABLE support_resistance_snapshot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_time TEXT NOT NULL,
    total_coins INTEGER,
    buy_signal_coins INTEGER,         -- 抄底信号币种数
    sell_signal_coins INTEGER,        -- 逃顶信号币种数
    double_buy_coins INTEGER,         -- 双重抄底币种数
    double_sell_coins INTEGER,        -- 双重逃顶币种数
    snapshot_data TEXT,               -- JSON格式完整数据
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### 触碰判断逻辑 / Touch Detection Logic
```python
# 支撑线S1触碰
if abs(current_price - support_s1) / support_s1 < 0.005:  # 0.5%误差范围
    s1_touch_count += 1

# 支撑线S2触碰
if abs(current_price - support_s2) / support_s2 < 0.005:
    s2_touch_count += 1

# 压力线R1触碰
if abs(current_price - resistance_r1) / resistance_r1 < 0.005:
    r1_touch_count += 1

# 压力线R2触碰
if abs(current_price - resistance_r2) / resistance_r2 < 0.005:
    r2_touch_count += 1
```

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复采集器
cp source_code/support_resistance_collector.py /home/user/webapp/
cp source_code/support_resistance_snapshot_collector.py /home/user/webapp/

# 2. 恢复页面
cp templates/support_resistance*.html /home/user/webapp/templates/

# 3. 启动采集器
pm2 start support_resistance_collector.py --name support-resistance-collector
pm2 start support_resistance_snapshot_collector.py --name support-resistance-snapshot-collector

# 4. 查看实时数据
pm2 logs support-resistance-collector --lines 50

# 5. 访问监控页面
curl http://localhost:5000/support-resistance
```

#### 验证清单 / Verification
- [ ] 支撑压力线计算正确
- [ ] 触碰计数准确
- [ ] 信号生成正常
- [ ] 快照保存完整
- [ ] 页面实时更新正常

---

### 【15. 决策交易信号系统】 Decision Trading Signal System

#### 功能描述 / Description
综合多个指标生成最终交易决策信号，包括买入、卖出、持有建议

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `decision_signal_generator.py` - 决策信号生成器
- `templates/decision_signals.html` - 决策信号页面
- `signal_rules_config.json` - 信号规则配置

**数据库表 / Database Tables:**
- `crypto_data.db`:
  - `decision_signals` - 决策信号数据
  - `signal_history` - 信号历史记录

**PM2进程 / PM2 Process:**
- `flask-app` (ID: 20)

#### 数据字段 / Data Fields
```sql
CREATE TABLE decision_signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    signal_type TEXT NOT NULL,        -- BUY, SELL, HOLD
    signal_strength INTEGER,          -- 信号强度 (1-5)
    confidence_score REAL,            -- 置信度 (0-100)
    
    -- 各维度得分
    technical_signal TEXT,            -- 技术指标信号
    volume_signal TEXT,               -- 成交量信号
    support_resistance_signal TEXT,   -- 支撑压力信号
    position_signal TEXT,             -- 位置信号
    depth_signal TEXT,                -- 深度信号
    
    -- 决策依据
    decision_reasons TEXT,            -- JSON格式决策理由
    risk_level TEXT,                  -- 风险等级 (low, medium, high)
    
    -- 建议
    entry_price REAL,                 -- 建议入场价格
    stop_loss REAL,                   -- 止损价格
    take_profit REAL,                 -- 止盈价格
    
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, timestamp)
);

CREATE TABLE signal_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    signal_id INTEGER,
    signal_type TEXT,
    entry_price REAL,
    exit_price REAL,
    profit_loss REAL,                 -- 盈亏
    profit_percentage REAL,           -- 盈亏百分比
    signal_datetime TEXT,
    exit_datetime TEXT,
    status TEXT,                      -- active, closed, cancelled
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### 信号生成规则 / Signal Generation Rules
```json
{
  "BUY_RULES": {
    "strong_buy": {
      "support_resistance": "双重抄底信号",
      "position": "位置 < 30",
      "depth": "买盘强度 > 60",
      "technical": "RSI < 30 AND MACD金叉"
    },
    "buy": {
      "support_resistance": "抄底信号",
      "position": "位置 < 40",
      "depth": "买盘强度 > 50"
    }
  },
  "SELL_RULES": {
    "strong_sell": {
      "support_resistance": "双重逃顶信号",
      "position": "位置 > 70",
      "depth": "卖盘强度 > 60",
      "technical": "RSI > 70 AND MACD死叉"
    },
    "sell": {
      "support_resistance": "逃顶信号",
      "position": "位置 > 60",
      "depth": "卖盘强度 > 50"
    }
  }
}
```

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复决策生成器
cp source_code/decision_signal_generator.py /home/user/webapp/

# 2. 恢复配置文件
cp configs/signal_rules_config.json /home/user/webapp/

# 3. 恢复页面
cp templates/decision_signals.html /home/user/webapp/templates/

# 4. 生成决策信号
cd /home/user/webapp && python3 decision_signal_generator.py

# 5. 查看信号
sqlite3 /home/user/webapp/crypto_data.db "SELECT symbol, signal_type, signal_strength, confidence_score FROM decision_signals WHERE signal_type IN ('BUY', 'SELL') ORDER BY confidence_score DESC LIMIT 20;"
```

#### 验证清单 / Verification
- [ ] 决策信号生成正常
- [ ] 信号强度计算准确
- [ ] 置信度评估合理
- [ ] 止损止盈建议正确
- [ ] 历史信号记录完整

---

### 【16. 决策-K线指标系统】 Decision K-line Indicator System

#### 功能描述 / Description
基于K线形态和技术指标（RSI, MACD, KDJ, BOLL等）生成交易信号

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `indicators_calculator.py` - 指标计算器
- `kline_pattern_detector.py` - K线形态识别
- `templates/indicators.html` - 指标展示页面
- `templates/indicators_history.html` - 指标历史页面

**数据库表 / Database Tables:**
- `crypto_data.db`:
  - `indicators_data` - 技术指标数据
  - `kline_patterns` - K线形态数据

**PM2进程 / PM2 Process:**
- `flask-app` (ID: 20)

#### 数据字段 / Data Fields
```sql
CREATE TABLE indicators_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    
    -- RSI指标
    rsi_6 REAL,
    rsi_12 REAL,
    rsi_24 REAL,
    rsi_signal TEXT,              -- overbought, oversold, neutral
    
    -- MACD指标
    macd REAL,
    macd_signal REAL,
    macd_histogram REAL,
    macd_cross TEXT,              -- golden_cross, death_cross, none
    
    -- KDJ指标
    kdj_k REAL,
    kdj_d REAL,
    kdj_j REAL,
    kdj_signal TEXT,              -- buy, sell, neutral
    
    -- BOLL指标
    boll_upper REAL,
    boll_middle REAL,
    boll_lower REAL,
    boll_width REAL,
    boll_position TEXT,           -- upper, middle, lower
    
    -- EMA均线
    ema_7 REAL,
    ema_25 REAL,
    ema_99 REAL,
    ema_trend TEXT,               -- bullish, bearish, neutral
    
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, timestamp)
);

CREATE TABLE kline_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    pattern_name TEXT,            -- 形态名称
    pattern_type TEXT,            -- bullish, bearish
    reliability INTEGER,          -- 可靠度 (1-5)
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### 支持的K线形态 / Supported Patterns
1. **看涨形态 (Bullish)**
   - 锤子线 (Hammer)
   - 早晨之星 (Morning Star)
   - 三只乌鸦 (Three White Soldiers)
   - 看涨吞没 (Bullish Engulfing)

2. **看跌形态 (Bearish)**
   - 上吊线 (Hanging Man)
   - 黄昏之星 (Evening Star)
   - 三只乌鸦 (Three Black Crows)
   - 看跌吞没 (Bearish Engulfing)

#### 指标信号规则 / Indicator Signal Rules
```python
# RSI信号
if rsi < 30:
    rsi_signal = 'oversold'  # 超卖 - 买入信号
elif rsi > 70:
    rsi_signal = 'overbought'  # 超买 - 卖出信号
else:
    rsi_signal = 'neutral'

# MACD金叉死叉
if macd > macd_signal and prev_macd <= prev_macd_signal:
    macd_cross = 'golden_cross'  # 金叉 - 买入
elif macd < macd_signal and prev_macd >= prev_macd_signal:
    macd_cross = 'death_cross'  # 死叉 - 卖出

# KDJ信号
if kdj_j < 20 and kdj_k < 20:
    kdj_signal = 'buy'  # 低位 - 买入
elif kdj_j > 80 and kdj_k > 80:
    kdj_signal = 'sell'  # 高位 - 卖出

# BOLL带突破
if current_price < boll_lower:
    boll_position = 'lower'  # 下轨 - 超卖
elif current_price > boll_upper:
    boll_position = 'upper'  # 上轨 - 超买
```

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复计算器
cp source_code/indicators_calculator.py /home/user/webapp/
cp source_code/kline_pattern_detector.py /home/user/webapp/

# 2. 恢复页面
cp templates/indicators*.html /home/user/webapp/templates/

# 3. 计算指标
cd /home/user/webapp && python3 indicators_calculator.py

# 4. 识别K线形态
cd /home/user/webapp && python3 kline_pattern_detector.py

# 5. 访问页面
curl http://localhost:5000/indicators
```

#### 验证清单 / Verification
- [ ] 指标计算准确
- [ ] K线形态识别正确
- [ ] 信号生成及时
- [ ] 页面图表显示正常
- [ ] 历史数据完整

---

### 【17. V1V2成交系统】 V1V2 Trading Volume System

#### 功能描述 / Description
监控大额成交（V1）和超大额成交（V2），用于识别主力资金动向

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `v1v2_collector.py` - V1V2成交采集器
- `templates/v1v2.html` - V1V2监控页面
- `analyze_v1v2.py` - V1V2分析脚本

**数据库表 / Database Tables:**
- `v1v2_data.db`:
  - `v1_trades` - V1大额成交数据
  - `v2_trades` - V2超大额成交数据

**PM2进程 / PM2 Process:**
- `v1v2-collector` (ID: 4)

#### 数据字段 / Data Fields
```sql
-- V1大额成交表
CREATE TABLE v1_trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    trade_id TEXT NOT NULL,
    price REAL NOT NULL,
    quantity REAL NOT NULL,
    amount REAL NOT NULL,            -- 成交金额
    side TEXT,                       -- buy, sell
    is_buyer_maker BOOLEAN,
    trade_type TEXT DEFAULT 'V1',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- V2超大额成交表
CREATE TABLE v2_trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    trade_id TEXT NOT NULL,
    price REAL NOT NULL,
    quantity REAL NOT NULL,
    amount REAL NOT NULL,
    side TEXT,
    is_buyer_maker BOOLEAN,
    trade_type TEXT DEFAULT 'V2',
    alert_sent BOOLEAN DEFAULT 0,    -- 是否已发送提醒
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### V1V2定义 / V1V2 Definition
```python
# V1定义：单笔成交金额 >= $10,000
V1_THRESHOLD = 10000  # USD

# V2定义：单笔成交金额 >= $100,000
V2_THRESHOLD = 100000  # USD

# 判断逻辑
trade_amount = price * quantity
if trade_amount >= V2_THRESHOLD:
    trade_type = 'V2'
elif trade_amount >= V1_THRESHOLD:
    trade_type = 'V1'
else:
    trade_type = 'normal'
```

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复采集器
cp source_code/v1v2_collector.py /home/user/webapp/

# 2. 恢复V1V2数据库
cp databases/v1v2_data.db /home/user/webapp/

# 3. 恢复页面
cp templates/v1v2.html /home/user/webapp/templates/

# 4. 启动采集器
pm2 start v1v2_collector.py --name v1v2-collector

# 5. 查看V1V2数据
sqlite3 /home/user/webapp/v1v2_data.db "SELECT symbol, price, quantity, amount, side FROM v2_trades ORDER BY amount DESC LIMIT 10;"
```

#### 验证清单 / Verification
- [ ] V1V2数据采集正常
- [ ] 成交金额计算准确
- [ ] 数据库写入正常
- [ ] 页面显示大额成交
- [ ] 提醒功能正常

---

### 【18. 1分钟涨跌幅系统】 1-Minute Price Change System

#### 功能描述 / Description
监控币种1分钟涨跌幅，识别快速拉升或快速下跌的异常行情

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `price_speed_monitor.py` - 价格速度监控器
- `templates/price_speed.html` - 涨跌幅监控页面
- `alert_price_speed.py` - 异常涨跌提醒脚本

**数据库表 / Database Tables:**
- `price_speed_data.db`:
  - `price_changes` - 价格变化数据
  - `speed_alerts` - 速度提醒记录

**PM2进程 / PM2 Process:**
- `flask-app` (ID: 20)
- 使用 `websocket-collector` 采集实时价格

#### 数据字段 / Data Fields
```sql
CREATE TABLE price_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    price_1m_ago REAL,
    current_price REAL,
    change_amount REAL,          -- 价格变化量
    change_percentage REAL,      -- 涨跌幅百分比
    volume_1m REAL,              -- 1分钟成交量
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, timestamp)
);

CREATE TABLE speed_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    alert_type TEXT,             -- pump (拉升), dump (砸盘)
    change_percentage REAL,
    trigger_price REAL,
    volume_1m REAL,
    alert_sent BOOLEAN DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### 提醒阈值 / Alert Thresholds
```python
# 快速拉升提醒
PUMP_THRESHOLD = 3.0  # 1分钟涨幅 >= 3%

# 快速下跌提醒
DUMP_THRESHOLD = -3.0  # 1分钟跌幅 <= -3%

# 极端行情提醒
EXTREME_PUMP = 5.0     # 1分钟涨幅 >= 5%
EXTREME_DUMP = -5.0    # 1分钟跌幅 <= -5%
```

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复监控器
cp source_code/price_speed_monitor.py /home/user/webapp/
cp source_code/alert_price_speed.py /home/user/webapp/

# 2. 恢复数据库
cp databases/price_speed_data.db /home/user/webapp/

# 3. 恢复页面
cp templates/price_speed.html /home/user/webapp/templates/

# 4. 确保WebSocket采集器运行
pm2 restart websocket-collector

# 5. 访问监控页面
curl http://localhost:5000/price_speed
```

#### 验证清单 / Verification
- [ ] 1分钟涨跌幅计算准确
- [ ] 异常行情识别及时
- [ ] 提醒触发正常
- [ ] 页面实时更新
- [ ] 历史提醒记录完整

---

### 【19. Google Drive监控系统】 Google Drive Monitoring System

#### 功能描述 / Description
监控Google Drive文件夹，自动下载最新文件并更新到系统

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `gdrive_monitor.py` - Google Drive监控主程序
- `gdrive_auto_trigger.py` - 自动触发器
- `auto_update_daily_folder.py` - 自动更新文件夹
- `access_latest_files.py` - 访问最新文件

**配置文件 / Config Files:**
- `configs/google_drive_config.json` - Google Drive配置
- `configs/credentials.json` - Google API凭证
- `configs/token.pickle` - 访问令牌

**数据库表 / Database Tables:**
- `crypto_data.db`:
  - `gdrive_files` - Google Drive文件记录
  - `gdrive_sync_log` - 同步日志

**PM2进程 / PM2 Process:**
- `gdrive-monitor` (ID: 3)
- `gdrive-auto-trigger` (ID: 10)

#### 数据字段 / Data Fields
```sql
CREATE TABLE gdrive_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id TEXT NOT NULL UNIQUE,
    file_name TEXT NOT NULL,
    file_size INTEGER,
    mime_type TEXT,
    created_time TEXT,
    modified_time TEXT,
    download_status TEXT DEFAULT 'pending',  -- pending, downloaded, failed
    local_path TEXT,
    sync_time TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE gdrive_sync_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sync_time TEXT NOT NULL,
    action TEXT,                    -- download, upload, delete
    file_name TEXT,
    status TEXT,                    -- success, failed
    error_message TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### 监控的文件夹 / Monitored Folders
- `/crypto_data/daily/` - 每日数据文件
- `/crypto_data/indicators/` - 指标数据文件
- `/crypto_data/reports/` - 分析报告文件

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复监控脚本
cp source_code/gdrive_monitor.py /home/user/webapp/
cp source_code/gdrive_auto_trigger.py /home/user/webapp/
cp source_code/auto_update_daily_folder.py /home/user/webapp/
cp source_code/access_latest_files.py /home/user/webapp/

# 2. 恢复配置文件
cp configs/google_drive_config.json /home/user/webapp/
cp configs/credentials.json /home/user/webapp/
cp configs/token.pickle /home/user/webapp/

# 3. 安装Google API依赖
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

# 4. 启动监控服务
pm2 start gdrive_monitor.py --name gdrive-monitor
pm2 start gdrive_auto_trigger.py --name gdrive-auto-trigger

# 5. 查看同步日志
pm2 logs gdrive-monitor --lines 50
```

#### 验证清单 / Verification
- [ ] Google Drive API连接正常
- [ ] 文件监控正常运行
- [ ] 自动下载功能正常
- [ ] 同步日志记录完整
- [ ] 本地文件更新及时

---

### 【20. TG消息推送系统】 Telegram Message Push System

#### 功能描述 / Description
通过Telegram Bot推送交易信号、价格提醒、异常行情等消息

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `telegram_notifier.py` - Telegram消息推送主程序
- `telegram_bot.py` - Telegram Bot交互逻辑
- `message_formatter.py` - 消息格式化

**配置文件 / Config Files:**
- `configs/telegram_config.json` - Telegram配置
- `configs/.env` - 环境变量（包含Bot Token）

**PM2进程 / PM2 Process:**
- `telegram-notifier` (ID: 13)

#### 配置文件格式 / Config Format
```json
{
  "bot_token": "YOUR_BOT_TOKEN",
  "chat_id": "-1003227444260",
  "check_interval_seconds": 30,
  "cooldown_minutes": {
    "double_buy": 30,
    "buy": 60,
    "double_sell": 30,
    "sell": 60
  },
  "thresholds": {
    "min_coins_double_buy": 1,
    "min_coins_buy": 8,
    "min_coins_double_sell": 1,
    "min_coins_sell": 8
  }
}
```

#### 推送的消息类型 / Message Types
1. **双重抄底信号** (Double Buy Signal)
   - 触发条件：双重抄底币种数 >= 1
   - 冷却时间：30分钟
   
2. **强势抄底信号** (Strong Buy Signal)
   - 触发条件：S1 >= 8 AND S2 >= 8
   - 冷却时间：60分钟
   
3. **双重逃顶信号** (Double Sell Signal)
   - 触发条件：双重逃顶币种数 >= 1
   - 冷却时间：30分钟
   
4. **最强逃顶信号** (Strong Sell Signal)
   - 触发条件：R1 >= 1 AND R2 >= 1 AND (R1+R2) >= 8
   - 冷却时间：60分钟

5. **异常涨跌提醒** (Price Speed Alert)
   - 1分钟涨跌幅 >= 3%

6. **V2大额成交提醒** (V2 Trade Alert)
   - 单笔成交 >= $100,000

#### 消息格式示例 / Message Format Example
```
🚀 【强势抄底信号】
━━━━━━━━━━━━━━━
📊 总币种数：8个
   支撑线S1：5个
   支撑线S2：3个

💡 信号强度：★★★★☆
⏰ 时间：2024-12-24 14:30:25

🔑 关键提示：
• 多个币种同时触及关键支撑位
• 建议关注支撑位反弹机会
• 注意风险控制，设置止损

📈 实时监控：https://5000-xxx.sandbox.novita.ai/support-resistance

⚠️ 本信号仅供参考，不构成投资建议
```

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复推送程序
cp source_code/telegram_notifier.py /home/user/webapp/
cp source_code/telegram_bot.py /home/user/webapp/
cp source_code/message_formatter.py /home/user/webapp/

# 2. 恢复配置
cp configs/telegram_config.json /home/user/webapp/
cp configs/.env /home/user/webapp/

# 3. 安装Telegram Bot依赖
pip install python-telegram-bot==20.7

# 4. 启动推送服务
pm2 start telegram_notifier.py --name telegram-notifier

# 5. 测试消息推送
cd /home/user/webapp && python3 -c "from telegram_notifier import send_test_message; send_test_message()"

# 6. 查看推送日志
pm2 logs telegram-notifier --lines 50
```

#### 最新修复记录 / Latest Fixes
**Commit: b9791e1**
- 修复：逃顶信号增加压力线1和压力线2都>=1的条件
- 优化：双重逃顶信号判断逻辑
- 改进：强势抄底信号判断逻辑（S1 >= 8 AND S2 >= 8）

#### 验证清单 / Verification
- [ ] Telegram Bot连接正常
- [ ] 消息推送功能正常
- [ ] 冷却时间机制正常
- [ ] 信号触发准确
- [ ] 消息格式正确
- [ ] 错误日志完整

---

### 【21. 资金监控系统】 Fund Monitoring System

#### 功能描述 / Description
监控币种资金流入流出，分析主力资金动向

#### 包含文件 / Included Files
**源代码 / Source Code:**
- `fund_monitor_collector.py` - 资金监控采集器
- `templates/fund_monitor.html` - 资金监控页面
- `analyze_fund_flow.py` - 资金流向分析脚本

**数据库表 / Database Tables:**
- `fund_monitor.db`:
  - `fund_flow_data` - 资金流向数据
  - `fund_alerts` - 资金异常提醒

**PM2进程 / PM2 Process:**
- `fund-monitor-collector` (ID: 18)

#### 数据字段 / Data Fields
```sql
CREATE TABLE fund_flow_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    
    -- 资金流向
    net_inflow REAL,              -- 净流入（正值为流入，负值为流出）
    large_order_inflow REAL,      -- 大单流入
    large_order_outflow REAL,     -- 大单流出
    medium_order_inflow REAL,     -- 中单流入
    medium_order_outflow REAL,    -- 中单流出
    small_order_inflow REAL,      -- 小单流入
    small_order_outflow REAL,     -- 小单流出
    
    -- 资金比率
    large_order_ratio REAL,       -- 大单比率
    buy_sell_ratio REAL,          -- 买卖比
    
    -- 资金强度
    fund_strength TEXT,           -- strong_inflow, weak_inflow, neutral, weak_outflow, strong_outflow
    
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, timestamp)
);

CREATE TABLE fund_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    alert_type TEXT,              -- large_inflow, large_outflow, abnormal
    net_inflow REAL,
    large_order_amount REAL,
    alert_sent BOOLEAN DEFAULT 0,
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### 资金流向计算 / Fund Flow Calculation
```python
# 大中小单划分
LARGE_ORDER_THRESHOLD = 50000   # >= $50,000
MEDIUM_ORDER_THRESHOLD = 10000  # >= $10,000
# SMALL_ORDER: < $10,000

# 净流入计算
net_inflow = total_buy_amount - total_sell_amount

# 大单流入流出
large_order_inflow = sum(买单 where amount >= LARGE_ORDER_THRESHOLD)
large_order_outflow = sum(卖单 where amount >= LARGE_ORDER_THRESHOLD)

# 资金强度判断
if net_inflow > 0 and large_order_ratio > 0.4:
    fund_strength = 'strong_inflow'  # 主力流入
elif net_inflow < 0 and large_order_ratio > 0.4:
    fund_strength = 'strong_outflow' # 主力流出
```

#### 提醒规则 / Alert Rules
```python
# 大额流入提醒
if large_order_inflow > 1000000:  # >= $1M
    alert_type = 'large_inflow'

# 大额流出提醒
if large_order_outflow > 1000000:  # >= $1M
    alert_type = 'large_outflow'

# 异常资金流向
if abs(net_inflow) > 5000000:  # >= $5M
    alert_type = 'abnormal'
```

#### 恢复步骤 / Recovery Steps
```bash
# 1. 恢复采集器
cp source_code/fund_monitor_collector.py /home/user/webapp/
cp source_code/analyze_fund_flow.py /home/user/webapp/

# 2. 恢复数据库
cp databases/fund_monitor.db /home/user/webapp/

# 3. 恢复页面
cp templates/fund_monitor.html /home/user/webapp/templates/

# 4. 启动采集器
pm2 start fund_monitor_collector.py --name fund-monitor-collector

# 5. 查看资金流向
sqlite3 /home/user/webapp/fund_monitor.db "SELECT symbol, net_inflow, large_order_ratio, fund_strength FROM fund_flow_data ORDER BY ABS(net_inflow) DESC LIMIT 20;"

# 6. 访问监控页面
curl http://localhost:5000/fund_monitor
```

#### 验证清单 / Verification
- [ ] 资金数据采集正常
- [ ] 资金流向计算准确
- [ ] 大中小单划分正确
- [ ] 提醒触发及时
- [ ] 页面显示资金排行

---

## 数据库表映射关系 / Database Table Mappings

### crypto_data.db (2.1GB, 20 tables)

| 表名 / Table Name | 所属子系统 / Subsystem | 数据量 / Records | 说明 / Description |
|-------------------|------------------------|------------------|---------------------|
| `binance_1m_data` | 1, 7, 16 | ~500万 | 1分钟K线历史数据 |
| `sar_slope_data` | 1 | ~50万 | SAR斜率数据 |
| `support_resistance_data` | 1, 2, 14 | ~100万 | 支撑压力线实时数据 |
| `support_resistance_snapshot` | 2, 14 | ~5万 | 支撑压力快照 |
| `indicators_data` | 1, 16 | ~100万 | 技术指标数据 |
| `kline_patterns` | 16 | ~10万 | K线形态数据 |
| `depth_chart_data` | 9, 10 | ~50万 | 深度图原始数据 |
| `depth_score_data` | 9 | ~30万 | 深度得分数据 |
| `panic_wash_index` | 3 | ~20万 | 恐慌清洗指数 |
| `price_comparison_data` | 4 | ~100万 | 价格对比数据 |
| `star_ratings` | 5 | ~20万 | 星级评分数据 |
| `count_score_data` | 5 | ~30万 | 计数评分数据 |
| `coin_pool` | 6 | ~500 | 币种池数据 |
| `realtime_trades` | 7 | ~100万 | 实时成交数据 |
| `realtime_orderbook` | 7 | ~50万 | 实时订单簿 |
| `crypto_index_data` | 12 | ~10万 | OKX加密指数 |
| `position_data` | 13 | ~50万 | 位置系统数据 |
| `decision_signals` | 15 | ~30万 | 决策信号数据 |
| `signal_history` | 2, 15 | ~10万 | 信号历史记录 |
| `average_score_data` | 11 | ~5万 | 平均分历史数据 |

### fund_monitor.db (6.7MB, 2 tables)

| 表名 / Table Name | 所属子系统 / Subsystem | 数据量 / Records | 说明 / Description |
|-------------------|------------------------|------------------|---------------------|
| `fund_flow_data` | 21 | ~10万 | 资金流向数据 |
| `fund_alerts` | 21 | ~2万 | 资金异常提醒 |

### v1v2_data.db (12MB, 2 tables)

| 表名 / Table Name | 所属子系统 / Subsystem | 数据量 / Records | 说明 / Description |
|-------------------|------------------------|------------------|---------------------|
| `v1_trades` | 17 | ~5万 | V1大额成交 |
| `v2_trades` | 17 | ~1万 | V2超大额成交 |

### price_speed_data.db (动态, 2 tables)

| 表名 / Table Name | 所属子系统 / Subsystem | 数据量 / Records | 说明 / Description |
|-------------------|------------------------|------------------|---------------------|
| `price_changes` | 18 | ~50万 | 价格变化数据 |
| `speed_alerts` | 18 | ~5万 | 速度提醒记录 |

---

## 完整恢复步骤 / Complete Recovery Steps

### 第一步：环境准备 / Step 1: Environment Preparation

```bash
# 1. 创建工作目录
mkdir -p /home/user/webapp
cd /home/user/webapp

# 2. 检查Python版本
python3 --version  # 应该 >= 3.12

# 3. 检查Node.js和PM2
node --version  # 应该 >= 18
npm --version   # 应该 >= 9
pm2 --version

# 如果没有PM2，安装它
if ! command -v pm2 &> /dev/null; then
    npm install -g pm2
    pm2 startup
fi

# 4. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate
```

### 第二步：解压备份 / Step 2: Extract Backup

```bash
# 假设备份文件在 /tmp/crypto_system_full_backup_20251224_140003.tar.gz
cd /tmp
tar -xzf crypto_system_full_backup_20251224_140003.tar.gz
cd crypto_system_full_backup_20251224_140003

# 或者从目录直接恢复
BACKUP_DIR="/tmp/crypto_system_full_backup_20251224_140003"
```

### 第三步：恢复源代码 / Step 3: Restore Source Code

```bash
# 恢复所有Python源文件
cp ${BACKUP_DIR}/source_code/*.py /home/user/webapp/
cp ${BACKUP_DIR}/source_code/*.sh /home/user/webapp/

# 恢复模板文件
mkdir -p /home/user/webapp/templates
cp ${BACKUP_DIR}/templates/*.html /home/user/webapp/templates/

# 恢复静态资源
mkdir -p /home/user/webapp/static/{js,css,images}
cp -r ${BACKUP_DIR}/static/* /home/user/webapp/static/

# 设置执行权限
chmod +x /home/user/webapp/*.sh
```

### 第四步：恢复数据库 / Step 4: Restore Databases

```bash
# 恢复所有数据库文件
cp ${BACKUP_DIR}/databases/*.db /home/user/webapp/

# 验证数据库完整性
for db in /home/user/webapp/*.db; do
    echo "Checking $db..."
    sqlite3 "$db" "PRAGMA integrity_check;"
done

# 检查数据库大小
ls -lh /home/user/webapp/*.db
```

### 第五步：恢复配置文件 / Step 5: Restore Configurations

```bash
# 恢复配置文件
cp ${BACKUP_DIR}/configs/.env /home/user/webapp/
cp ${BACKUP_DIR}/configs/*.json /home/user/webapp/
cp ${BACKUP_DIR}/configs/credentials.json /home/user/webapp/
cp ${BACKUP_DIR}/configs/token.pickle /home/user/webapp/

# 恢复PM2配置
cp ${BACKUP_DIR}/pm2/ecosystem.config.js /home/user/webapp/
cp ${BACKUP_DIR}/pm2/pm2.json /home/user/webapp/

# 设置配置文件权限
chmod 600 /home/user/webapp/.env
chmod 600 /home/user/webapp/credentials.json
```

### 第六步：安装依赖 / Step 6: Install Dependencies

```bash
cd /home/user/webapp

# 激活虚拟环境
source venv/bin/activate

# 恢复依赖列表
cp ${BACKUP_DIR}/dependencies/requirements.txt /home/user/webapp/
cp ${BACKUP_DIR}/dependencies/package.json /home/user/webapp/

# 安装Python依赖
pip install --upgrade pip
pip install -r requirements.txt

# 安装Node.js依赖（如果有）
if [ -f package.json ]; then
    npm install
fi
```

### 第七步：恢复Git仓库 / Step 7: Restore Git Repository

```bash
# 恢复Git仓库
cd /home/user/webapp
rm -rf .git
cp -r ${BACKUP_DIR}/git/.git /home/user/webapp/

# 验证Git状态
git status
git log --oneline -5

# 如果需要，重新关联远程仓库
git remote -v
# git remote set-url origin https://github.com/jamesyidc/66661.git
```

### 第八步：恢复日志文件 / Step 8: Restore Logs

```bash
# 恢复日志目录
mkdir -p /home/user/webapp/logs
cp ${BACKUP_DIR}/logs/*.log /home/user/webapp/logs/

# 创建日志清理定时任务
echo "0 2 * * * find /home/user/webapp/logs -name '*.log' -mtime +7 -delete" | crontab -
```

### 第九步：启动所有服务 / Step 9: Start All Services

```bash
cd /home/user/webapp

# 方式1：使用PM2 ecosystem配置启动
pm2 start ecosystem.config.js

# 方式2：逐个启动（如果没有ecosystem配置）
pm2 start app.py --name flask-app --interpreter python3
pm2 start websocket_collector.py --name websocket-collector --interpreter python3
pm2 start crypto_index_collector.py --name crypto-index-collector --interpreter python3
pm2 start support_resistance_collector.py --name support-resistance-collector --interpreter python3
pm2 start support_resistance_snapshot_collector.py --name support-resistance-snapshot-collector --interpreter python3
pm2 start v1v2_collector.py --name v1v2-collector --interpreter python3
pm2 start position_system_collector.py --name position-system-collector --interpreter python3
pm2 start collector_monitor.py --name collector-monitor --interpreter python3
pm2 start gdrive_monitor.py --name gdrive-monitor --interpreter python3
pm2 start gdrive_auto_trigger.py --name gdrive-auto-trigger --interpreter python3
pm2 start panic_wash_collector.py --name panic-wash-collector --interpreter python3
pm2 start price_comparison_collector.py --name price-comparison-collector --interpreter python3
pm2 start telegram_notifier.py --name telegram-notifier --interpreter python3
pm2 start fund_monitor_collector.py --name fund-monitor-collector --interpreter python3
pm2 start sar_slope_collector.py --name sar-slope-collector --interpreter python3

# 保存PM2配置
pm2 save

# 设置PM2开机自启
pm2 startup
```

### 第十步：验证系统 / Step 10: Verify System

```bash
# 1. 检查所有PM2进程
pm2 list

# 2. 查看进程日志
pm2 logs --lines 50

# 3. 检查Flask应用
curl http://localhost:5000/
curl http://localhost:5000/support-resistance
curl http://localhost:5000/history

# 4. 验证数据库查询
sqlite3 /home/user/webapp/crypto_data.db "SELECT count(*) FROM binance_1m_data;"
sqlite3 /home/user/webapp/fund_monitor.db "SELECT count(*) FROM fund_flow_data;"
sqlite3 /home/user/webapp/v1v2_data.db "SELECT count(*) FROM v1_trades;"

# 5. 测试Telegram Bot连接
cd /home/user/webapp
python3 -c "from telegram_notifier import test_connection; test_connection()"

# 6. 检查采集器状态
pm2 logs collector-monitor --lines 30
```

---

## 验证清单 / Verification Checklist

### 系统层面 / System Level
- [ ] Python 3.12+ 已安装
- [ ] Node.js 18+ 已安装
- [ ] PM2 已安装并配置
- [ ] 虚拟环境已创建
- [ ] 所有依赖已安装

### 文件恢复 / File Restoration
- [ ] 源代码文件已恢复（150+ Python文件）
- [ ] HTML模板已恢复（30+ 文件）
- [ ] 静态资源已恢复
- [ ] 配置文件已恢复
- [ ] 数据库文件已恢复（4个数据库）
- [ ] Git仓库已恢复

### 数据库验证 / Database Verification
- [ ] crypto_data.db 完整性检查通过
- [ ] fund_monitor.db 完整性检查通过
- [ ] v1v2_data.db 完整性检查通过
- [ ] price_speed_data.db 完整性检查通过
- [ ] 所有表查询正常

### 服务验证 / Service Verification
- [ ] Flask应用运行正常（ID: 20）
- [ ] WebSocket采集器运行正常（ID: 2）
- [ ] 所有数据采集器运行正常
- [ ] Telegram推送服务运行正常（ID: 13）
- [ ] Google Drive监控运行正常（ID: 3, 10）

### 21个子系统验证 / 21 Subsystems Verification
- [ ] 1. 历史数据查询系统 - 页面可访问，数据查询正常
- [ ] 2. 交易信号监控系统 - 信号检测正常，Telegram推送成功
- [ ] 3. 恐慌清洗指数系统 - 数据采集正常，指数计算准确
- [ ] 4. 比价系统 - 多交易所价格对比正常
- [ ] 5. 星星系统 - 评分计算正常，星级显示正确
- [ ] 6. 币种池系统 - 币种列表完整，管理功能正常
- [ ] 7. 实时市场原始数据 - WebSocket连接稳定，数据实时更新
- [ ] 8. 数据采集监控 - 监控服务运行，自动重启功能正常
- [ ] 9. 深度图得分 - 得分计算准确，数据存储正常
- [ ] 10. 深度图可视化 - 图表渲染正常，实时更新正常
- [ ] 11. 平均分页面 - 平均分计算正确，历史数据完整
- [ ] 12. OKEx加密指数 - 指数数据采集正常，页面显示正确
- [ ] 13. 位置系统 - 位置计算准确，等级分类正确
- [ ] 14. 支撑压力线系统 - 支撑压力识别正常，触碰计数准确
- [ ] 15. 决策交易信号系统 - 决策信号生成正常，置信度评估合理
- [ ] 16. 决策-K线指标系统 - 指标计算准确，K线形态识别正确
- [ ] 17. V1V2成交系统 - V1V2数据采集正常，大额成交识别准确
- [ ] 18. 1分钟涨跌幅系统 - 涨跌幅计算准确，异常提醒及时
- [ ] 19. Google Drive监控系统 - Google Drive连接正常，文件同步正常
- [ ] 20. TG消息推送系统 - Telegram Bot连接正常，消息推送成功
- [ ] 21. 资金监控系统 - 资金数据采集正常，流向分析准确

### 功能验证 / Functional Verification
- [ ] Web页面全部可访问
- [ ] 实时数据更新正常
- [ ] 历史数据查询正常
- [ ] 交易信号生成正常
- [ ] Telegram推送正常
- [ ] 日志记录正常

---

## 故障排除 / Troubleshooting

### 常见问题 / Common Issues

#### 1. PM2进程启动失败
```bash
# 查看错误日志
pm2 logs <process-name> --err

# 手动测试Python脚本
cd /home/user/webapp
source venv/bin/activate
python3 <script-name>.py

# 检查依赖
pip list | grep -i flask
```

#### 2. 数据库查询失败
```bash
# 检查数据库文件权限
ls -l /home/user/webapp/*.db

# 修复权限
chmod 644 /home/user/webapp/*.db

# 检查数据库完整性
sqlite3 /home/user/webapp/crypto_data.db "PRAGMA integrity_check;"
```

#### 3. Telegram Bot连接失败
```bash
# 检查Bot Token
cat /home/user/webapp/.env | grep TELEGRAM

# 测试Bot API
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe

# 检查网络连接
ping api.telegram.org
```

#### 4. Google Drive同步失败
```bash
# 检查凭证文件
ls -l /home/user/webapp/credentials.json
ls -l /home/user/webapp/token.pickle

# 重新授权
cd /home/user/webapp
python3 -c "from gdrive_monitor import reauthorize; reauthorize()"
```

#### 5. 采集器数据停止更新
```bash
# 重启采集器监控
pm2 restart collector-monitor

# 手动重启所有采集器
pm2 restart all

# 检查数据库锁定
fuser /home/user/webapp/crypto_data.db
```

---

## 联系方式 / Contact Information

**开发者 / Developer:** jamesyi  
**GitHub:** https://github.com/jamesyidc/66661  
**Telegram Bot:** @jamesyi9999_bot  
**备份时间 / Backup Time:** 2024-12-24 14:00:03  
**系统版本 / System Version:** v2.2  
**Git Commit:** b9791e1

---

## 附录：快速恢复脚本 / Appendix: Quick Recovery Script

```bash
#!/bin/bash
# 快速恢复脚本 / Quick Recovery Script
# 使用方法: ./quick_restore.sh /path/to/backup

set -e

BACKUP_DIR="$1"
TARGET_DIR="/home/user/webapp"

if [ -z "$BACKUP_DIR" ]; then
    echo "用法: $0 <备份目录路径>"
    exit 1
fi

echo "开始恢复系统..."
echo "备份目录: $BACKUP_DIR"
echo "目标目录: $TARGET_DIR"

# 1. 恢复文件
echo "恢复源代码..."
cp ${BACKUP_DIR}/source_code/*.py $TARGET_DIR/
cp -r ${BACKUP_DIR}/templates $TARGET_DIR/
cp -r ${BACKUP_DIR}/static $TARGET_DIR/

echo "恢复数据库..."
cp ${BACKUP_DIR}/databases/*.db $TARGET_DIR/

echo "恢复配置..."
cp ${BACKUP_DIR}/configs/.env $TARGET_DIR/
cp ${BACKUP_DIR}/configs/*.json $TARGET_DIR/

# 2. 安装依赖
echo "安装依赖..."
cd $TARGET_DIR
source venv/bin/activate
pip install -r ${BACKUP_DIR}/dependencies/requirements.txt

# 3. 启动服务
echo "启动服务..."
pm2 start ${BACKUP_DIR}/pm2/ecosystem.config.js

echo "恢复完成！"
pm2 list
```

---

**文档版本 / Document Version:** 1.0  
**最后更新 / Last Updated:** 2024-12-24 14:30:00  
**文档大小 / Document Size:** ~60KB

