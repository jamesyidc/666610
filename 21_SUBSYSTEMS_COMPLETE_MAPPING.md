# 21个子系统完整映射文档
## Complete Mapping Document for 21 Subsystems

**备份时间 / Backup Time:** 2024-12-24 14:00:03  
**系统版本 / System Version:** v2.2  
**文档目的 / Purpose:** 详细记录每个子系统的文件列表、数据库表、PM2进程、依赖关系

---

## 映射总览 / Mapping Overview

| 子系统ID | 子系统名称 | 源文件数 | 数据库表数 | PM2进程数 | 依赖关系 |
|---------|-----------|---------|-----------|----------|----------|
| 1 | 历史数据查询系统 | 10 | 6 | 1 | 依赖所有采集器 |
| 2 | 交易信号监控系统 | 5 | 3 | 2 | 依赖系统14 |
| 3 | 恐慌清洗指数系统 | 3 | 1 | 1 | 独立系统 |
| 4 | 比价系统 | 2 | 1 | 1 | 独立系统 |
| 5 | 星星系统 | 4 | 2 | 1 | 依赖多个系统 |
| 6 | 币种池系统 | 3 | 1 | 1 | 基础系统 |
| 7 | 实时市场原始数据 | 3 | 3 | 1 | 基础系统 |
| 8 | 数据采集监控 | 3 | 2 | 1 | 监控所有采集器 |
| 9 | 深度图得分 | 3 | 2 | 1 | 依赖系统7 |
| 10 | 深度图可视化 | 3 | 1 | 1 | 依赖系统9 |
| 11 | 平均分页面 | 2 | 1 | 1 | 依赖系统5 |
| 12 | OKEx加密指数 | 2 | 1 | 1 | 独立系统 |
| 13 | 位置系统 | 3 | 1 | 1 | 独立系统 |
| 14 | 支撑压力线系统 | 4 | 2 | 2 | 基础系统 |
| 15 | 决策交易信号系统 | 4 | 2 | 1 | 依赖多个系统 |
| 16 | 决策-K线指标系统 | 4 | 2 | 1 | 依赖系统7 |
| 17 | V1V2成交系统 | 3 | 2 | 1 | 独立系统 |
| 18 | 1分钟涨跌幅系统 | 3 | 2 | 1 | 依赖系统7 |
| 19 | Google Drive监控系统 | 5 | 2 | 2 | 独立系统 |
| 20 | TG消息推送系统 | 4 | 0 | 1 | 依赖系统2,14 |
| 21 | 资金监控系统 | 3 | 2 | 1 | 独立系统 |

---

## 【1. 历史数据查询系统】

### 基本信息 / Basic Info
- **系统ID:** 1
- **中文名称:** 历史数据查询系统
- **英文名称:** Historical Data Query System
- **系统类型:** Web展示系统
- **重要程度:** ★★★★★

### 完整文件列表 / Complete File List

#### 源代码文件 / Source Files (10 files)
```
source_code/
├── app.py                                    # Flask主应用 (核心)
├── query_history.py                          # 历史查询逻辑
├── export_history_data.py                    # 导出历史数据
├── backfill_today_data.py                    # 回填今日数据
├── backfill_missing_data.py                  # 回填缺失数据
├── backfill_indicators.py                    # 回填指标数据
├── add_demo_history.py                       # 添加演示数据
├── analyze_structure.py                      # 分析数据结构
├── analyze_uni_rsi.py                        # 分析统一RSI
└── batch_import_all_txt.py                   # 批量导入TXT数据
```

#### 模板文件 / Template Files (6 files)
```
templates/
├── history.html                               # 历史查询主页
├── sar_history.html                           # SAR历史页
├── support_resistance_history.html            # 支撑压力历史页
├── indicators_history.html                    # 指标历史页
├── depth_history.html                         # 深度历史页
└── position_history.html                      # 位置历史页
```

#### 静态资源 / Static Files (3 files)
```
static/
├── js/history_chart.js                        # 历史图表JS
├── css/history.css                            # 历史页样式
└── images/history_icon.png                    # 图标
```

### 数据库表映射 / Database Tables (6 tables)

#### crypto_data.db
```sql
-- 1. 1分钟K线历史数据
binance_1m_data
字段: id, symbol, timestamp, open, high, low, close, volume, quote_volume, created_at
数据量: ~5,000,000 条
索引: symbol, timestamp
备注: 核心历史数据表

-- 2. SAR斜率历史数据
sar_slope_data
字段: id, symbol, timestamp, sar_value, slope, trend, created_at
数据量: ~500,000 条
索引: symbol, timestamp
备注: SAR指标历史

-- 3. 支撑压力线历史数据
support_resistance_data
字段: id, symbol, timestamp, support_s1, support_s2, resistance_r1, resistance_r2,
      s1_touch_count, s2_touch_count, r1_touch_count, r2_touch_count, created_at
数据量: ~1,000,000 条
索引: symbol, timestamp
备注: 支撑压力历史记录

-- 4. 技术指标历史数据
indicators_data
字段: id, symbol, timestamp, rsi_6, rsi_12, rsi_24, macd, macd_signal, macd_histogram,
      kdj_k, kdj_d, kdj_j, boll_upper, boll_middle, boll_lower, ema_7, ema_25, ema_99, created_at
数据量: ~1,000,000 条
索引: symbol, timestamp
备注: 技术指标历史

-- 5. 深度图历史数据
depth_chart_data
字段: id, symbol, timestamp, bids_json, asks_json, bid_total_volume, ask_total_volume, created_at
数据量: ~500,000 条
索引: symbol, timestamp
备注: 订单簿深度历史

-- 6. 位置系统历史数据
position_data
字段: id, symbol, timestamp, current_price, high_7d, low_7d, high_30d, low_30d,
      position_7d, position_30d, position_level, created_at
数据量: ~500,000 条
索引: symbol, timestamp
备注: 价格位置历史
```

### PM2进程配置 / PM2 Process (1 process)
```javascript
{
  name: "flask-app",
  script: "app.py",
  interpreter: "python3",
  instances: 1,
  exec_mode: "fork",
  watch: false,
  max_memory_restart: "500M",
  env: {
    FLASK_APP: "app.py",
    FLASK_ENV: "production"
  }
}
```

### 依赖关系 / Dependencies
**依赖的子系统:**
- 系统7: 实时市场原始数据（提供K线数据）
- 系统13: 位置系统（提供位置数据）
- 系统14: 支撑压力线系统（提供支撑压力数据）
- 系统16: 决策-K线指标系统（提供指标数据）

**被依赖的子系统:**
- 系统2: 交易信号监控系统（查询历史信号）
- 系统15: 决策交易信号系统（查询历史决策）

### API接口列表 / API Endpoints
```
GET  /history                              # 历史查询主页
GET  /api/history/kline?symbol=BTC&start=&end=   # 获取K线历史
GET  /api/history/sar?symbol=BTC&start=&end=     # 获取SAR历史
GET  /api/history/support_resistance?symbol=     # 获取支撑压力历史
GET  /api/history/indicators?symbol=             # 获取指标历史
POST /api/history/export                         # 导出历史数据
```

### 恢复验证命令 / Verification Commands
```bash
# 1. 验证源文件存在
ls -lh /home/user/webapp/app.py
ls -lh /home/user/webapp/templates/history*.html

# 2. 验证数据库表
sqlite3 /home/user/webapp/crypto_data.db "SELECT count(*) FROM binance_1m_data;"
sqlite3 /home/user/webapp/crypto_data.db ".schema binance_1m_data"

# 3. 验证Flask应用
pm2 list | grep flask-app
curl http://localhost:5000/history

# 4. 测试历史查询
curl "http://localhost:5000/api/history/kline?symbol=BTCUSDT&start=2024-12-23&end=2024-12-24"
```

---

## 【2. 交易信号监控系统】

### 基本信息 / Basic Info
- **系统ID:** 2
- **中文名称:** 交易信号监控系统
- **英文名称:** Trading Signal Monitoring System
- **系统类型:** 信号检测与推送系统
- **重要程度:** ★★★★★

### 完整文件列表 / Complete File List

#### 源代码文件 / Source Files (5 files)
```
source_code/
├── telegram_notifier.py                      # Telegram推送核心 (最新修复: b9791e1)
├── signal_detector.py                        # 信号检测逻辑
├── signal_analyzer.py                        # 信号分析器
├── message_formatter.py                      # 消息格式化
└── test_telegram_signal.py                   # 测试脚本
```

#### 模板文件 / Template Files (3 files)
```
templates/
├── signals.html                               # 信号监控主页
├── support_resistance.html                    # 支撑压力实时页 (核心页面)
└── signal_history.html                        # 信号历史页
```

#### 配置文件 / Config Files (2 files)
```
configs/
├── telegram_config.json                       # Telegram配置
└── .env                                       # 环境变量 (包含Bot Token)
```

### 数据库表映射 / Database Tables (3 tables)

#### crypto_data.db
```sql
-- 1. 支撑压力实时数据 (核心表)
support_resistance_data
字段: id, symbol, timestamp, current_price, support_s1, support_s2, resistance_r1, resistance_r2,
      s1_touch_count, s2_touch_count, r1_touch_count, r2_touch_count, signal_type, created_at
数据量: ~1,000,000 条
索引: symbol, timestamp, signal_type
备注: 支撑压力实时数据，信号生成依据

-- 2. 支撑压力快照 (历史快照)
support_resistance_snapshot
字段: id, snapshot_time, total_coins, buy_signal_coins, sell_signal_coins,
      double_buy_coins, double_sell_coins, snapshot_data, created_at
数据量: ~50,000 条
索引: snapshot_time
备注: 定期快照，用于历史回溯

-- 3. 信号历史记录
signal_history
字段: id, signal_id, symbol, signal_type, signal_strength, confidence_score,
      entry_price, exit_price, profit_loss, status, signal_datetime, exit_datetime, created_at
数据量: ~100,000 条
索引: symbol, signal_type, signal_datetime
备注: 信号历史与执行结果
```

### PM2进程配置 / PM2 Process (2 processes)
```javascript
[
  {
    name: "telegram-notifier",
    script: "telegram_notifier.py",
    interpreter: "python3",
    instances: 1,
    exec_mode: "fork",
    watch: false,
    max_memory_restart: "100M",
    restart_delay: 3000,
    env: {
      TELEGRAM_BOT_TOKEN: "from .env",
      CHAT_ID: "-1003227444260"
    }
  },
  {
    name: "flask-app",
    script: "app.py",
    interpreter: "python3"
  }
]
```

### 信号规则配置 / Signal Rules

#### telegram_config.json
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
  },
  
  "signals": {
    "strong_buy": {
      "name": "强势抄底信号",
      "condition": "S1 >= 8 AND S2 >= 8",
      "emoji": "🚀",
      "priority": "high"
    },
    "strong_sell": {
      "name": "最强逃顶信号",
      "condition": "R1 >= 1 AND R2 >= 1 AND (R1+R2) >= 8",
      "emoji": "⚠️",
      "priority": "high"
    },
    "double_buy": {
      "name": "双重抄底信号",
      "condition": "双重触碰S1和S2",
      "emoji": "💰",
      "priority": "critical"
    },
    "double_sell": {
      "name": "双重逃顶信号",
      "condition": "双重触碰R1和R2",
      "emoji": "🔔",
      "priority": "critical"
    }
  }
}
```

### 依赖关系 / Dependencies
**依赖的子系统:**
- 系统14: 支撑压力线系统（核心依赖，提供支撑压力数据）

**被依赖的子系统:**
- 系统20: TG消息推送系统（发送信号通知）

### API接口列表 / API Endpoints
```
GET  /support-resistance                   # 支撑压力实时监控页
GET  /signals                               # 信号列表页
GET  /api/signals/latest                    # 获取最新信号
GET  /api/signals/history                   # 获取信号历史
POST /api/signals/test                      # 测试信号推送
```

### 最新修复记录 / Latest Fixes
```
Commit: b9791e1
Date: 2024-12-24
Author: jamesyi
Title: fix: 逃顶信号增加压力线1和压力线2都>=1的条件

修改内容:
1. 强势逃顶信号判断逻辑优化
   原逻辑: (R1 + R2) >= 8
   新逻辑: (R1 >= 1 AND R2 >= 1 AND (R1+R2) >= 8)
   
2. 强势抄底信号判断逻辑
   条件: (S1 >= 8 AND S2 >= 8)
   
3. 确保双重确认机制
   - 两条线都必须有触碰
   - 避免单线触碰误判
   
影响范围:
- telegram_notifier.py (Line 460-474)
- 提高信号准确性
- 降低误报率
```

### 恢复验证命令 / Verification Commands
```bash
# 1. 验证源文件
ls -lh /home/user/webapp/telegram_notifier.py

# 2. 检查最新修复
cd /home/user/webapp && git log --oneline -1
# 应该看到: b9791e1 fix: 逃顶信号增加压力线1和压力线2都>=1的条件

# 3. 验证配置文件
cat /home/user/webapp/telegram_config.json
cat /home/user/webapp/.env | grep TELEGRAM

# 4. 验证PM2进程
pm2 list | grep telegram-notifier
pm2 logs telegram-notifier --lines 30

# 5. 测试信号检测
cd /home/user/webapp
python3 -c "from telegram_notifier import get_latest_signals; print(get_latest_signals())"

# 6. 测试Telegram推送
python3 -c "from telegram_notifier import send_test_message; send_test_message()"

# 7. 验证数据库数据
sqlite3 /home/user/webapp/crypto_data.db "SELECT symbol, s1_touch_count, s2_touch_count, r1_touch_count, r2_touch_count FROM support_resistance_data WHERE r1_touch_count >= 1 AND r2_touch_count >= 1 ORDER BY timestamp DESC LIMIT 10;"

# 8. 访问监控页面
curl http://localhost:5000/support-resistance
```

---

## 【3. 恐慌清洗指数系统】

### 基本信息 / Basic Info
- **系统ID:** 3
- **中文名称:** 恐慌清洗指数系统
- **英文名称:** Panic Wash Index System
- **系统类型:** 情绪指标系统
- **重要程度:** ★★★★☆

### 完整文件列表 / Complete File List

#### 源代码文件 / Source Files (3 files)
```
source_code/
├── panic_wash_collector.py                   # 恐慌清洗采集器
├── calculate_panic_index.py                  # 恐慌指数计算
└── calculate_wash_index.py                   # 清洗指数计算
```

#### 模板文件 / Template Files (2 files)
```
templates/
├── panic_wash.html                            # 恐慌清洗主页
└── panic_wash_history.html                    # 历史数据页
```

### 数据库表映射 / Database Tables (1 table)

#### crypto_data.db
```sql
-- 恐慌清洗指数数据
panic_wash_index
字段: id, symbol, timestamp, panic_index, wash_index, market_sentiment,
      volume_ratio, price_change_24h, fear_greed_score, created_at
数据量: ~200,000 条
索引: symbol, timestamp, market_sentiment
备注: 市场情绪指标

索引优化:
CREATE INDEX idx_panic_wash_symbol_time ON panic_wash_index(symbol, timestamp DESC);
CREATE INDEX idx_panic_wash_sentiment ON panic_wash_index(market_sentiment);
```

### PM2进程配置 / PM2 Process (1 process)
```javascript
{
  name: "panic-wash-collector",
  script: "panic_wash_collector.py",
  interpreter: "python3",
  instances: 1,
  exec_mode: "fork",
  cron_restart: "0 */1 * * *",
  max_memory_restart: "50M"
}
```

### 计算公式 / Calculation Formula
```python
# 恐慌指数 (0-100)
panic_index = (
    rsi_deviation * 0.3 +
    volume_spike * 0.3 +
    price_volatility * 0.2 +
    depth_imbalance * 0.2
)

# 清洗指数 (0-100)
wash_index = (
    rapid_price_change * 0.4 +
    volume_concentration * 0.3 +
    large_order_ratio * 0.3
)

# 市场情绪
if panic_index >= 80:
    sentiment = 'extreme_fear'  # 极度恐慌
elif panic_index >= 60:
    sentiment = 'fear'           # 恐慌
elif panic_index >= 40:
    sentiment = 'neutral'        # 中性
elif panic_index >= 20:
    sentiment = 'greed'          # 贪婪
else:
    sentiment = 'extreme_greed'  # 极度贪婪
```

### 恢复验证命令 / Verification Commands
```bash
# 验证采集器
pm2 list | grep panic-wash-collector
pm2 logs panic-wash-collector --lines 30

# 验证数据
sqlite3 /home/user/webapp/crypto_data.db "SELECT symbol, panic_index, wash_index, market_sentiment FROM panic_wash_index ORDER BY timestamp DESC LIMIT 10;"

# 访问页面
curl http://localhost:5000/panic_wash
```

---

## 【14. 支撑压力线系统】（核心系统，详细展开）

### 基本信息 / Basic Info
- **系统ID:** 14
- **中文名称:** 支撑压力线系统
- **英文名称:** Support & Resistance System
- **系统类型:** 核心技术分析系统
- **重要程度:** ★★★★★ (最高)

### 完整文件列表 / Complete File List

#### 源代码文件 / Source Files (4 files)
```
source_code/
├── support_resistance_collector.py           # 实时采集器 (核心)
├── support_resistance_snapshot_collector.py  # 快照采集器
├── calculate_support_resistance.py           # 支撑压力计算
└── detect_touch_points.py                    # 触碰点检测
```

#### 模板文件 / Template Files (3 files)
```
templates/
├── support_resistance.html                    # 实时监控页 (核心页面)
├── support_resistance_history.html            # 历史数据页
└── support_resistance_analysis.html           # 分析报告页
```

#### 静态资源 / Static Files (2 files)
```
static/
├── js/support_resistance_chart.js             # 图表JS
└── css/support_resistance.css                 # 样式
```

### 数据库表映射 / Database Tables (2 tables)

#### crypto_data.db
```sql
-- 1. 支撑压力实时数据 (核心表)
support_resistance_data
CREATE TABLE support_resistance_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    current_price REAL NOT NULL,
    
    -- 支撑线
    support_s1 REAL,                           -- 支撑线1
    support_s2 REAL,                           -- 支撑线2
    support_s3 REAL,                           -- 支撑线3 (备用)
    
    -- 压力线
    resistance_r1 REAL,                        -- 压力线1
    resistance_r2 REAL,                        -- 压力线2
    resistance_r3 REAL,                        -- 压力线3 (备用)
    
    -- 触碰计数
    s1_touch_count INTEGER DEFAULT 0,         -- S1触碰次数
    s2_touch_count INTEGER DEFAULT 0,         -- S2触碰次数
    r1_touch_count INTEGER DEFAULT 0,         -- R1触碰次数
    r2_touch_count INTEGER DEFAULT 0,         -- R2触碰次数
    
    -- 信号类型
    signal_type TEXT,                          -- buy, sell, neutral, double_buy, double_sell
    signal_strength INTEGER,                   -- 信号强度 (1-5)
    
    -- 距离百分比
    s1_distance_percent REAL,                  -- 当前价格距S1的百分比
    s2_distance_percent REAL,
    r1_distance_percent REAL,
    r2_distance_percent REAL,
    
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, timestamp)
);

-- 索引优化
CREATE INDEX idx_sr_symbol_time ON support_resistance_data(symbol, timestamp DESC);
CREATE INDEX idx_sr_signal ON support_resistance_data(signal_type, signal_strength);
CREATE INDEX idx_sr_touch ON support_resistance_data(s1_touch_count, s2_touch_count, r1_touch_count, r2_touch_count);

数据量: ~1,000,000 条
更新频率: 每30秒
数据保留: 30天


-- 2. 支撑压力快照 (历史快照)
support_resistance_snapshot
CREATE TABLE support_resistance_snapshot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_time TEXT NOT NULL UNIQUE,
    
    -- 统计数据
    total_coins INTEGER,                       -- 总币种数
    buy_signal_coins INTEGER,                  -- 抄底信号币种数
    sell_signal_coins INTEGER,                 -- 逃顶信号币种数
    double_buy_coins INTEGER,                  -- 双重抄底币种数
    double_sell_coins INTEGER,                 -- 双重逃顶币种数
    neutral_coins INTEGER,                     -- 中性币种数
    
    -- 触碰统计
    total_s1_touches INTEGER,                  -- 总S1触碰次数
    total_s2_touches INTEGER,                  -- 总S2触碰次数
    total_r1_touches INTEGER,                  -- 总R1触碰次数
    total_r2_touches INTEGER,                  -- 总R2触碰次数
    
    -- 完整快照数据 (JSON)
    snapshot_data TEXT,                        -- 所有币种的完整数据
    
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_snapshot_time ON support_resistance_snapshot(snapshot_time DESC);

数据量: ~50,000 条
快照频率: 每5分钟
数据保留: 永久
```

### PM2进程配置 / PM2 Process (2 processes)
```javascript
[
  {
    name: "support-resistance-collector",
    script: "support_resistance_collector.py",
    interpreter: "python3",
    instances: 1,
    exec_mode: "fork",
    watch: false,
    max_memory_restart: "100M",
    restart_delay: 5000,
    env: {
      COLLECTION_INTERVAL: "30",
      TOUCH_THRESHOLD: "0.005"
    }
  },
  {
    name: "support-resistance-snapshot-collector",
    script: "support_resistance_snapshot_collector.py",
    interpreter: "python3",
    instances: 1,
    exec_mode: "fork",
    cron_restart: "*/5 * * * *",
    max_memory_restart: "50M"
  }
]
```

### 支撑压力计算逻辑 / Calculation Logic

#### 1. 支撑压力线识别
```python
def calculate_support_resistance(symbol, period='7d'):
    """
    计算支撑压力线
    
    算法:
    1. 获取近期K线数据（7天）
    2. 识别局部极值点（高点和低点）
    3. 聚类分析找到关键价格区间
    4. 计算支撑线S1, S2和压力线R1, R2
    """
    
    # 获取K线数据
    klines = get_klines(symbol, period)
    
    # 识别局部极值
    highs = find_local_maxima(klines)
    lows = find_local_minima(klines)
    
    # 聚类分析
    resistance_clusters = cluster_prices(highs, threshold=0.01)
    support_clusters = cluster_prices(lows, threshold=0.01)
    
    # 排序并选择前2条线
    resistance_r1, resistance_r2 = sorted(resistance_clusters, reverse=True)[:2]
    support_s1, support_s2 = sorted(support_clusters)[:2]
    
    return {
        'support_s1': support_s1,
        'support_s2': support_s2,
        'resistance_r1': resistance_r1,
        'resistance_r2': resistance_r2
    }
```

#### 2. 触碰检测逻辑
```python
def detect_touch(current_price, support_resistance_lines):
    """
    检测价格是否触碰支撑压力线
    
    触碰定义: 价格与支撑压力线的偏差 <= 0.5%
    """
    TOUCH_THRESHOLD = 0.005  # 0.5%
    
    touches = {
        's1': False,
        's2': False,
        'r1': False,
        'r2': False
    }
    
    # 检测S1触碰
    if abs(current_price - support_s1) / support_s1 < TOUCH_THRESHOLD:
        touches['s1'] = True
        s1_touch_count += 1
    
    # 检测S2触碰
    if abs(current_price - support_s2) / support_s2 < TOUCH_THRESHOLD:
        touches['s2'] = True
        s2_touch_count += 1
    
    # 检测R1触碰
    if abs(current_price - resistance_r1) / resistance_r1 < TOUCH_THRESHOLD:
        touches['r1'] = True
        r1_touch_count += 1
    
    # 检测R2触碰
    if abs(current_price - resistance_r2) / resistance_r2 < TOUCH_THRESHOLD:
        touches['r2'] = True
        r2_touch_count += 1
    
    return touches
```

#### 3. 信号生成逻辑 (最新版本 - b9791e1)
```python
def generate_signal(s1_count, s2_count, r1_count, r2_count):
    """
    生成交易信号
    
    信号类型:
    1. 双重抄底信号 (double_buy): 同时触碰S1和S2
    2. 强势抄底信号 (strong_buy): S1 >= 8 AND S2 >= 8
    3. 双重逃顶信号 (double_sell): 同时触碰R1和R2
    4. 最强逃顶信号 (strong_sell): R1 >= 1 AND R2 >= 1 AND (R1+R2) >= 8
    5. 中性 (neutral): 无明确信号
    """
    
    # 双重抄底信号 (最高优先级)
    if s1_count >= 1 and s2_count >= 1:
        return {
            'signal_type': 'double_buy',
            'signal_strength': 5,
            'description': '双重抄底信号'
        }
    
    # 双重逃顶信号 (最高优先级)
    if r1_count >= 1 and r2_count >= 1:
        return {
            'signal_type': 'double_sell',
            'signal_strength': 5,
            'description': '双重逃顶信号'
        }
    
    # 强势抄底信号 (v2.2修复)
    if s1_count >= 8 and s2_count >= 8:
        return {
            'signal_type': 'strong_buy',
            'signal_strength': 4,
            'description': '强势抄底信号'
        }
    
    # 最强逃顶信号 (v2.2修复 - Commit b9791e1)
    # 新逻辑: R1 >= 1 AND R2 >= 1 AND (R1+R2) >= 8
    if r1_count >= 1 and r2_count >= 1 and (r1_count + r2_count) >= 8:
        return {
            'signal_type': 'strong_sell',
            'signal_strength': 4,
            'description': '最强逃顶信号'
        }
    
    # 中性
    return {
        'signal_type': 'neutral',
        'signal_strength': 1,
        'description': '无明确信号'
    }
```

### API接口列表 / API Endpoints
```
GET  /support-resistance                          # 实时监控页面 (核心)
GET  /support-resistance/history                  # 历史数据页面
GET  /api/support-resistance/current              # 获取当前支撑压力数据
GET  /api/support-resistance/signals              # 获取最新信号
GET  /api/support-resistance/snapshot             # 获取最新快照
GET  /api/support-resistance/history?symbol=&start=&end=  # 历史数据查询
POST /api/support-resistance/calculate            # 手动触发计算
```

### 监控页面URL / Monitoring Page URL
```
实时监控页面:
https://5000-ilsitop6yown44mau7vd7-c07dda5e.sandbox.novita.ai/support-resistance

功能:
- 实时显示所有币种的支撑压力线
- 显示触碰计数
- 高亮显示信号币种
- 自动刷新（30秒）
- 支持搜索和过滤
```

### 依赖关系 / Dependencies
**依赖的子系统:**
- 系统7: 实时市场原始数据（提供实时价格）

**被依赖的子系统:**
- 系统2: 交易信号监控系统（核心依赖）
- 系统15: 决策交易信号系统
- 系统20: TG消息推送系统

### 恢复验证命令 / Verification Commands
```bash
# 1. 验证源文件
ls -lh /home/user/webapp/support_resistance_collector.py
ls -lh /home/user/webapp/support_resistance_snapshot_collector.py

# 2. 验证PM2进程
pm2 list | grep support-resistance
pm2 logs support-resistance-collector --lines 50

# 3. 验证数据库表
sqlite3 /home/user/webapp/crypto_data.db ".schema support_resistance_data"
sqlite3 /home/user/webapp/crypto_data.db "SELECT count(*) FROM support_resistance_data;"

# 4. 查看最新数据
sqlite3 /home/user/webapp/crypto_data.db "SELECT symbol, current_price, support_s1, support_s2, resistance_r1, resistance_r2, s1_touch_count, s2_touch_count, r1_touch_count, r2_touch_count, signal_type FROM support_resistance_data ORDER BY timestamp DESC LIMIT 20;"

# 5. 验证信号逻辑 (v2.2最新修复)
sqlite3 /home/user/webapp/crypto_data.db "SELECT symbol, r1_touch_count, r2_touch_count, signal_type FROM support_resistance_data WHERE r1_touch_count >= 1 AND r2_touch_count >= 1 AND (r1_touch_count + r2_touch_count) >= 8 ORDER BY timestamp DESC;"

# 6. 访问监控页面
curl http://localhost:5000/support-resistance

# 7. 测试API
curl http://localhost:5000/api/support-resistance/current
curl http://localhost:5000/api/support-resistance/signals

# 8. 验证快照数据
sqlite3 /home/user/webapp/crypto_data.db "SELECT snapshot_time, total_coins, buy_signal_coins, sell_signal_coins, double_buy_coins, double_sell_coins FROM support_resistance_snapshot ORDER BY snapshot_time DESC LIMIT 10;"
```

---

## 【20. TG消息推送系统】（核心通知系统，详细展开）

### 基本信息 / Basic Info
- **系统ID:** 20
- **中文名称:** TG消息推送系统
- **英文名称:** Telegram Message Push System
- **系统类型:** 通知推送系统
- **重要程度:** ★★★★★ (最高)

### 完整文件列表 / Complete File List

#### 源代码文件 / Source Files (4 files)
```
source_code/
├── telegram_notifier.py                      # 核心推送程序 (最新: b9791e1)
├── telegram_bot.py                            # Bot交互逻辑
├── message_formatter.py                       # 消息格式化
└── test_telegram.py                           # 测试脚本
```

#### 配置文件 / Config Files (2 files)
```
configs/
├── telegram_config.json                       # Telegram配置
└── .env                                       # 环境变量配置
```

### 配置文件详解 / Config Files Details

#### telegram_config.json (完整配置)
```json
{
  "bot_token": "YOUR_BOT_TOKEN_HERE",
  "chat_id": "-1003227444260",
  "bot_username": "jamesyi9999_bot",
  
  "check_interval_seconds": 30,
  
  "cooldown_minutes": {
    "double_buy": 30,
    "buy": 60,
    "double_sell": 30,
    "sell": 60,
    "v2_trade": 15,
    "price_alert": 10
  },
  
  "thresholds": {
    "min_coins_double_buy": 1,
    "min_coins_buy": 8,
    "min_coins_double_sell": 1,
    "min_coins_sell": 8,
    "v2_trade_amount": 100000,
    "price_change_percent": 3.0
  },
  
  "signals": {
    "double_buy": {
      "name": "双重抄底信号",
      "emoji": "💰",
      "priority": "critical",
      "cooldown": 30,
      "enabled": true
    },
    "strong_buy": {
      "name": "强势抄底信号",
      "emoji": "🚀",
      "priority": "high",
      "cooldown": 60,
      "enabled": true
    },
    "double_sell": {
      "name": "双重逃顶信号",
      "emoji": "🔔",
      "priority": "critical",
      "cooldown": 30,
      "enabled": true
    },
    "strong_sell": {
      "name": "最强逃顶信号",
      "emoji": "⚠️",
      "priority": "high",
      "cooldown": 60,
      "enabled": true
    }
  },
  
  "message_templates": {
    "strong_buy": "🚀 【强势抄底信号】\n━━━━━━━━━━━━━━━\n📊 总币种数：{total_count}个\n   支撑线S1：{s1_count}个\n   支撑线S2：{s2_count}个\n\n💡 信号强度：{'★' * strength}\n⏰ 时间：{timestamp}\n\n🔑 关键提示：\n• 多个币种同时触及关键支撑位\n• 建议关注支撑位反弹机会\n• 注意风险控制，设置止损\n\n📈 实时监控：{monitor_url}\n\n⚠️ 本信号仅供参考，不构成投资建议",
    
    "strong_sell": "⚠️ 【最强逃顶信号】\n━━━━━━━━━━━━━━━\n📊 总币种数：{total_count}个\n   压力线R1：{r1_count}个\n   压力线R2：{r2_count}个\n\n💡 信号强度：{'★' * strength}\n⏰ 时间：{timestamp}\n\n🔑 关键提示：\n• 多个币种触及关键压力位\n• 建议考虑减仓或止盈\n• 注意回调风险\n\n📈 实时监控：{monitor_url}\n\n⚠️ 本信号仅供参考，不构成投资建议"
  },
  
  "monitoring_url": "https://5000-ilsitop6yown44mau7vd7-c07dda5e.sandbox.novita.ai/support-resistance"
}
```

#### .env (环境变量)
```bash
# Telegram Bot配置
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=-1003227444260

# 数据库配置
DATABASE_PATH=/home/user/webapp/crypto_data.db

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=/home/user/webapp/logs/telegram_notifier.log

# 调试模式
DEBUG_MODE=false
```

### PM2进程配置 / PM2 Process (1 process)
```javascript
{
  name: "telegram-notifier",
  script: "telegram_notifier.py",
  interpreter: "python3",
  instances: 1,
  exec_mode: "fork",
  watch: false,
  max_memory_restart: "100M",
  restart_delay: 3000,
  autorestart: true,
  env: {
    TELEGRAM_BOT_TOKEN: "from .env",
    TELEGRAM_CHAT_ID: "-1003227444260",
    DATABASE_PATH: "/home/user/webapp/crypto_data.db"
  },
  log_date_format: "YYYY-MM-DD HH:mm:ss",
  error_file: "/home/user/webapp/logs/telegram-notifier-error.log",
  out_file: "/home/user/webapp/logs/telegram-notifier-out.log"
}
```

### 核心代码逻辑 / Core Code Logic

#### telegram_notifier.py (核心文件 - 最新版本 b9791e1)
```python
#!/usr/bin/env python3
"""
Telegram消息推送系统 - 核心文件
版本: v2.2
最新修复: b9791e1 (2024-12-24)
"""

import time
import json
import sqlite3
from datetime import datetime, timedelta
import requests
from telegram import Bot
from telegram.error import TelegramError

# 配置加载
def load_config():
    with open('telegram_config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

CONFIG = load_config()
BOT_TOKEN = CONFIG['bot_token']
CHAT_ID = CONFIG['chat_id']
CHECK_INTERVAL = CONFIG['check_interval_seconds']

# Telegram Bot实例
bot = Bot(token=BOT_TOKEN)

# 冷却时间管理
last_signal_time = {
    'double_buy': None,
    'strong_buy': None,
    'double_sell': None,
    'strong_sell': None
}

def get_latest_signals():
    """
    从数据库获取最新信号
    """
    conn = sqlite3.connect('/home/user/webapp/crypto_data.db')
    cursor = conn.cursor()
    
    # 获取最新的支撑压力数据
    query = """
    SELECT symbol, s1_touch_count, s2_touch_count, 
           r1_touch_count, r2_touch_count, signal_type,
           current_price, support_s1, support_s2,
           resistance_r1, resistance_r2
    FROM support_resistance_data
    WHERE timestamp >= strftime('%s', 'now', '-5 minutes')
    ORDER BY timestamp DESC
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    # 统计信号
    signals = {
        'double_buy_coins': [],
        'buy_signal_coins': [],
        'double_sell_coins': [],
        'sell_signal_coins': []
    }
    
    support_s1_count = 0
    support_s2_count = 0
    resistance_r1_count = 0
    resistance_r2_count = 0
    
    for row in results:
        symbol = row[0]
        s1_count = row[1]
        s2_count = row[2]
        r1_count = row[3]
        r2_count = row[4]
        
        # 双重抄底信号
        if s1_count >= 1 and s2_count >= 1:
            signals['double_buy_coins'].append(symbol)
        
        # 双重逃顶信号
        if r1_count >= 1 and r2_count >= 1:
            signals['double_sell_coins'].append(symbol)
        
        # 统计触碰计数
        if s1_count >= 1:
            support_s1_count += 1
        if s2_count >= 1:
            support_s2_count += 1
        if r1_count >= 1:
            resistance_r1_count += 1
        if r2_count >= 1:
            resistance_r2_count += 1
    
    # 强势抄底信号 (v2.2修复: S1 >= 8 AND S2 >= 8)
    buy_data = {
        'time': datetime.now(),
        'count': support_s1_count + support_s2_count,
        's1_count': support_s1_count,
        's2_count': support_s2_count,
        'coins': []
    }
    
    # 最强逃顶信号 (v2.2修复 - Commit b9791e1)
    # 新逻辑: R1 >= 1 AND R2 >= 1 AND (R1+R2) >= 8
    sell_data = {
        'time': datetime.now(),
        'count': resistance_r1_count + resistance_r2_count,
        'r1_count': resistance_r1_count,
        'r2_count': resistance_r2_count,
        'coins': []
    }
    
    return signals, buy_data, sell_data

def check_cooldown(signal_type):
    """
    检查冷却时间
    """
    if last_signal_time[signal_type] is None:
        return True
    
    cooldown_minutes = CONFIG['cooldown_minutes'][signal_type]
    time_diff = datetime.now() - last_signal_time[signal_type]
    
    return time_diff.total_seconds() >= cooldown_minutes * 60

def send_message(message):
    """
    发送Telegram消息
    """
    try:
        bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode='HTML',
            disable_web_page_preview=False
        )
        print(f"✅ 消息发送成功: {message[:50]}...")
        return True
    except TelegramError as e:
        print(f"❌ 消息发送失败: {e}")
        return False

def format_strong_buy_message(buy_data):
    """
    格式化强势抄底信号消息
    """
    template = CONFIG['message_templates']['strong_buy']
    
    message = template.format(
        total_count=buy_data['count'],
        s1_count=buy_data['s1_count'],
        s2_count=buy_data['s2_count'],
        strength=4,
        timestamp=buy_data['time'].strftime('%Y-%m-%d %H:%M:%S'),
        monitor_url=CONFIG['monitoring_url']
    )
    
    return message

def format_strong_sell_message(sell_data):
    """
    格式化最强逃顶信号消息 (v2.2修复版本)
    """
    template = CONFIG['message_templates']['strong_sell']
    
    message = template.format(
        total_count=sell_data['count'],
        r1_count=sell_data['r1_count'],
        r2_count=sell_data['r2_count'],
        strength=4,
        timestamp=sell_data['time'].strftime('%Y-%m-%d %H:%M:%S'),
        monitor_url=CONFIG['monitoring_url']
    )
    
    return message

def check_and_notify():
    """
    检查信号并发送通知
    """
    print(f"\n[{datetime.now()}] 检查信号...")
    
    signals, buy_data, sell_data = get_latest_signals()
    
    double_buy_count = len(signals['double_buy_coins'])
    double_sell_count = len(signals['double_sell_coins'])
    
    # 1. 双重抄底信号 (最高优先级)
    if double_buy_count >= CONFIG['thresholds']['min_coins_double_buy']:
        if check_cooldown('double_buy'):
            message = f"💰 【双重抄底信号】\n检测到 {double_buy_count} 个币种触发双重抄底\n\n"
            message += f"币种: {', '.join(signals['double_buy_coins'][:10])}\n"
            message += f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            message += f"📈 实时监控: {CONFIG['monitoring_url']}"
            
            if send_message(message):
                last_signal_time['double_buy'] = datetime.now()
                print(f"✅ 双重抄底信号已推送: {double_buy_count}个币种")
        else:
            print(f"⏳ 双重抄底信号在冷却中")
    
    # 2. 强势抄底信号 (v2.2修复: S1 >= 8 AND S2 >= 8)
    elif buy_data['s1_count'] >= 8 and buy_data['s2_count'] >= 8:
        if check_cooldown('strong_buy'):
            message = format_strong_buy_message(buy_data)
            
            if send_message(message):
                last_signal_time['strong_buy'] = datetime.now()
                print(f"✅ 强势抄底信号已推送: S1={buy_data['s1_count']}, S2={buy_data['s2_count']}")
        else:
            print(f"⏳ 强势抄底信号在冷却中")
    
    # 3. 双重逃顶信号 (最高优先级)
    if double_sell_count >= CONFIG['thresholds']['min_coins_double_sell']:
        if check_cooldown('double_sell'):
            message = f"🔔 【双重逃顶信号】\n检测到 {double_sell_count} 个币种触发双重逃顶\n\n"
            message += f"币种: {', '.join(signals['double_sell_coins'][:10])}\n"
            message += f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            message += f"📈 实时监控: {CONFIG['monitoring_url']}"
            
            if send_message(message):
                last_signal_time['double_sell'] = datetime.now()
                print(f"✅ 双重逃顶信号已推送: {double_sell_count}个币种")
        else:
            print(f"⏳ 双重逃顶信号在冷却中")
    
    # 4. 最强逃顶信号 (v2.2修复 - Commit b9791e1)
    # 新逻辑: R1 >= 1 AND R2 >= 1 AND (R1+R2) >= 8
    elif (sell_data['r1_count'] >= 1 and 
          sell_data['r2_count'] >= 1 and 
          (sell_data['r1_count'] + sell_data['r2_count']) >= 8):
        if check_cooldown('strong_sell'):
            message = format_strong_sell_message(sell_data)
            
            if send_message(message):
                last_signal_time['strong_sell'] = datetime.now()
                print(f"✅ 最强逃顶信号已推送: R1={sell_data['r1_count']}, R2={sell_data['r2_count']}, Total={(sell_data['r1_count'] + sell_data['r2_count'])}")
        else:
            print(f"⏳ 最强逃顶信号在冷却中")
    else:
        print(f"ℹ️ 暂无信号触发")

def main():
    """
    主循环
    """
    print(f"🤖 Telegram消息推送服务启动")
    print(f"📱 Bot: {CONFIG['bot_username']}")
    print(f"💬 Chat ID: {CHAT_ID}")
    print(f"⏱️ 检查间隔: {CHECK_INTERVAL}秒")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    while True:
        try:
            check_and_notify()
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f"❌ 错误: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
```

### 最新修复详情 / Latest Fix Details

#### Commit b9791e1 (2024-12-24)
```
标题: fix: 逃顶信号增加压力线1和压力线2都>=1的条件

修改文件: telegram_notifier.py (Line 460-474)

原逻辑:
if (sell_data['r1_count'] + sell_data['r2_count']) >= 8:
    # 触发逃顶信号

问题:
- 可能只有R1触碰8次，R2为0，就触发信号
- 或者R2触碰8次，R1为0，也触发信号
- 导致单线触碰误判

新逻辑:
if (sell_data['r1_count'] >= 1 and 
    sell_data['r2_count'] >= 1 and 
    (sell_data['r1_count'] + sell_data['r2_count']) >= 8):
    # 触发逃顶信号

优化:
- 确保R1和R2都至少触碰1次
- 总触碰次数仍需 >= 8
- 双重确认机制，提高准确性

影响:
- 降低误报率
- 提高信号可靠性
- 更符合实际交易逻辑

示例:
✅ 合格: R1=5, R2=3, Total=8 (两条线都有触碰)
✅ 合格: R1=1, R2=7, Total=8 (两条线都有触碰)
❌ 不合格: R1=8, R2=0, Total=8 (只有一条线)
❌ 不合格: R1=0, R2=8, Total=8 (只有一条线)
```

### 依赖关系 / Dependencies
**依赖的子系统:**
- 系统2: 交易信号监控系统（获取信号数据）
- 系统14: 支撑压力线系统（核心数据来源）
- 系统17: V1V2成交系统（大额成交提醒）
- 系统18: 1分钟涨跌幅系统（价格异常提醒）

**被依赖的子系统:**
- 无（终端通知系统）

### 恢复验证命令 / Verification Commands
```bash
# 1. 验证源文件和最新修复
ls -lh /home/user/webapp/telegram_notifier.py
cd /home/user/webapp && git log --oneline -1
# 应该看到: b9791e1 fix: 逃顶信号增加压力线1和压力线2都>=1的条件

# 2. 验证配置文件
cat /home/user/webapp/telegram_config.json | jq '.'
cat /home/user/webapp/.env | grep TELEGRAM

# 3. 验证PM2进程
pm2 list | grep telegram-notifier
pm2 show telegram-notifier

# 4. 查看实时日志
pm2 logs telegram-notifier --lines 50 --nostream

# 5. 测试Bot连接
cd /home/user/webapp
python3 << EOF
from telegram import Bot
bot = Bot(token='YOUR_BOT_TOKEN')
print(bot.get_me())
EOF

# 6. 测试消息发送
python3 << EOF
from telegram_notifier import send_message
send_message("🧪 测试消息: Telegram推送系统恢复成功")
EOF

# 7. 验证信号检测逻辑 (v2.2最新修复)
python3 << EOF
from telegram_notifier import get_latest_signals, check_and_notify
signals, buy_data, sell_data = get_latest_signals()
print(f"Buy signals: S1={buy_data['s1_count']}, S2={buy_data['s2_count']}")
print(f"Sell signals: R1={sell_data['r1_count']}, R2={sell_data['r2_count']}, Total={sell_data['count']}")
print(f"逃顶信号判断: R1>={ 1 AND R2>=1 AND (R1+R2)>=8")
EOF

# 8. 手动触发检查
pm2 restart telegram-notifier
pm2 logs telegram-notifier --lines 100

# 9. 验证冷却时间
sqlite3 /home/user/webapp/crypto_data.db "SELECT datetime('now', 'localtime');"
```

---

## 完整系统依赖关系图 / Complete System Dependency Graph

```
基础数据层 (Layer 1):
├── [6] 币种池系统
├── [7] 实时市场原始数据 ★
└── [12] OKEx加密指数

核心分析层 (Layer 2):
├── [3] 恐慌清洗指数系统
├── [4] 比价系统
├── [9] 深度图得分
├── [13] 位置系统
├── [14] 支撑压力线系统 ★★★ (核心)
├── [16] 决策-K线指标系统
├── [17] V1V2成交系统
└── [18] 1分钟涨跌幅系统

高级决策层 (Layer 3):
├── [2] 交易信号监控系统 ★★
├── [5] 星星系统
├── [15] 决策交易信号系统
└── [11] 平均分页面

展示与通知层 (Layer 4):
├── [1] 历史数据查询系统
├── [10] 深度图可视化
└── [20] TG消息推送系统 ★★

监控与集成层 (Layer 5):
├── [8] 数据采集监控
├── [19] Google Drive监控系统
└── [21] 资金监控系统

依赖关系:
Layer 1 (基础) → Layer 2 (分析) → Layer 3 (决策) → Layer 4 (展示) → Layer 5 (监控)

关键路径:
[7实时数据] → [14支撑压力] → [2交易信号] → [20TG推送]
```

---

## 快速参考表 / Quick Reference Table

### 数据库文件分布 / Database File Distribution

| 数据库文件 | 大小 | 表数量 | 所属子系统 | 重要程度 |
|-----------|------|--------|----------|----------|
| crypto_data.db | 2.1GB | 20 | 1,2,3,4,5,7,9,10,11,12,13,14,15,16 | ★★★★★ |
| fund_monitor.db | 6.7MB | 2 | 21 | ★★★☆☆ |
| v1v2_data.db | 12MB | 2 | 17 | ★★★★☆ |
| price_speed_data.db | 动态 | 2 | 18 | ★★★☆☆ |

### PM2进程映射表 / PM2 Process Mapping

| PM2 ID | 进程名 | 对应子系统 | 脚本文件 | 重要程度 |
|--------|--------|----------|---------|----------|
| 20 | flask-app | 1,2,5,6,9,10,11,13,15,16 | app.py | ★★★★★ |
| 2 | websocket-collector | 7 | websocket_collector.py | ★★★★★ |
| 8 | crypto-index-collector | 12 | crypto_index_collector.py | ★★★☆☆ |
| 5 | support-resistance-collector | 14 | support_resistance_collector.py | ★★★★★ |
| 6 | support-resistance-snapshot-collector | 14 | support_resistance_snapshot_collector.py | ★★★★☆ |
| 7 | position-system-collector | 13 | position_system_collector.py | ★★★☆☆ |
| 4 | v1v2-collector | 17 | v1v2_collector.py | ★★★★☆ |
| 11 | panic-wash-collector | 3 | panic_wash_collector.py | ★★★☆☆ |
| 12 | price-comparison-collector | 4 | price_comparison_collector.py | ★★★☆☆ |
| 18 | fund-monitor-collector | 21 | fund_monitor_collector.py | ★★★☆☆ |
| 21 | sar-slope-collector | 1 | sar_slope_collector.py | ★★★☆☆ |
| 9 | collector-monitor | 8 | collector_monitor.py | ★★★★☆ |
| 3 | gdrive-monitor | 19 | gdrive_monitor.py | ★★☆☆☆ |
| 10 | gdrive-auto-trigger | 19 | gdrive_auto_trigger.py | ★★☆☆☆ |
| 13 | telegram-notifier | 20 | telegram_notifier.py | ★★★★★ |

---

## 附录：完整文件清单 / Appendix: Complete File Inventory

### 源代码文件 (150+ files)
```
backup/source_code/
├── app.py                                     # Flask主应用 [系统1,2,5,6,9,10,11,13,15,16]
├── telegram_notifier.py                       # Telegram推送 [系统20] (b9791e1)
├── websocket_collector.py                     # WebSocket采集 [系统7]
├── support_resistance_collector.py            # 支撑压力采集 [系统14]
├── support_resistance_snapshot_collector.py   # 支撑压力快照 [系统14]
├── position_system_collector.py               # 位置系统 [系统13]
├── v1v2_collector.py                          # V1V2成交 [系统17]
├── panic_wash_collector.py                    # 恐慌清洗 [系统3]
├── price_comparison_collector.py              # 价格对比 [系统4]
├── fund_monitor_collector.py                  # 资金监控 [系统21]
├── crypto_index_collector.py                  # OKX指数 [系统12]
├── sar_slope_collector.py                     # SAR斜率 [系统1]
├── collector_monitor.py                       # 采集器监控 [系统8]
├── gdrive_monitor.py                          # Google Drive监控 [系统19]
├── gdrive_auto_trigger.py                     # Google Drive触发器 [系统19]
├── calculate_count_score.py                   # 评分计算 [系统5]
├── calculate_priority.py                      # 优先级计算 [系统5]
├── calculate_depth_score.py                   # 深度得分 [系统9]
├── calculate_average_score.py                 # 平均分计算 [系统11]
├── indicators_calculator.py                   # 指标计算 [系统16]
├── kline_pattern_detector.py                  # K线形态识别 [系统16]
├── decision_signal_generator.py               # 决策信号生成 [系统15]
├── price_speed_monitor.py                     # 价格速度监控 [系统18]
├── analyze_fund_flow.py                       # 资金流向分析 [系统21]
└── ... (130+ more files)
```

### 模板文件 (30+ files)
```
backup/templates/
├── history.html                               # [系统1]
├── sar_history.html                           # [系统1]
├── support_resistance.html                    # [系统2,14] (核心页面)
├── support_resistance_history.html            # [系统1,14]
├── indicators_history.html                    # [系统1,16]
├── signals.html                               # [系统2]
├── panic_wash.html                            # [系统3]
├── price_comparison.html                      # [系统4]
├── star_rating.html                           # [系统5]
├── coin_pool.html                             # [系统6]
├── depth_chart.html                           # [系统10]
├── depth_score.html                           # [系统9]
├── average_score.html                         # [系统11]
├── crypto_index.html                          # [系统12]
├── position_system.html                       # [系统13]
├── decision_signals.html                      # [系统15]
├── indicators.html                            # [系统16]
├── v1v2.html                                  # [系统17]
├── price_speed.html                           # [系统18]
├── fund_monitor.html                          # [系统21]
└── ... (10+ more files)
```

### 配置文件 (10+ files)
```
backup/configs/
├── .env                                       # 环境变量 [全局]
├── telegram_config.json                       # Telegram配置 [系统20]
├── google_drive_config.json                   # Google Drive配置 [系统19]
├── credentials.json                           # Google凭证 [系统19]
├── token.pickle                               # Google令牌 [系统19]
├── coin_pool_config.json                      # 币种池配置 [系统6]
├── signal_rules_config.json                   # 信号规则 [系统15]
└── ecosystem.config.js                        # PM2配置 [全局]
```

---

**文档版本 / Version:** 2.0  
**最后更新 / Last Updated:** 2024-12-24 15:00:00  
**文档大小 / Size:** ~90KB  
**适用系统版本 / System Version:** v2.2  
**Git Commit:** b9791e1

