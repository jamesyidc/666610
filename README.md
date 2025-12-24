# 🎯 加密货币监控系统完整备份 - 快速导航

**备份日期**: 2025-12-24 14:00:03  
**备份路径**: `/tmp/crypto_system_full_backup_20251224_140003`  
**备份大小**: 3.1GB  
**系统版本**: v2.3  
**最新提交**: b9791e1 - 逃顶信号逻辑优化

---

## 📋 备份内容清单

本备份包含一个完整的**21个子系统**的加密货币监控与分析平台的所有核心资产：

✅ 源代码 (Source Code) - ~150+ Python文件  
✅ 数据库 (Databases) - 2.1GB (4个数据库, 26张表)  
✅ 配置文件 (Configuration Files)  
✅ 模板文件 (HTML Templates) - ~30+ 文件  
✅ 静态资源 (Static Assets)  
✅ 依赖清单 (Dependencies)  
✅ PM2配置 (PM2 Configuration)  
✅ Git仓库 (Complete Git Repository)  
✅ 日志文件 (Log Files)  
✅ 完整文档 (Complete Documentation)

---

## 🚀 快速恢复步骤

### 前置要求
- 操作系统: Ubuntu 20.04+ / Debian 11+
- Python: 3.12+
- Node.js: 18+
- PM2: 最新版本
- Git: 2.x+
- 磁盘空间: 至少10GB可用

### 一键恢复命令

```bash
#!/bin/bash
# 设置备份路径
BACKUP_DIR="/tmp/crypto_system_full_backup_20251224_140003"
TARGET_DIR="/home/user/webapp"

# 1. 创建目标目录
mkdir -p $TARGET_DIR
cd $TARGET_DIR

# 2. 恢复源代码
echo "恢复源代码..."
cp -r $BACKUP_DIR/source_code/* $TARGET_DIR/
cp -r $BACKUP_DIR/templates $TARGET_DIR/
cp -r $BACKUP_DIR/static $TARGET_DIR/

# 3. 恢复配置文件
echo "恢复配置文件..."
cp $BACKUP_DIR/configs/* $TARGET_DIR/

# 4. 恢复数据库
echo "恢复数据库..."
cp $BACKUP_DIR/databases/*.db $TARGET_DIR/

# 5. 恢复 Git 仓库
echo "恢复 Git 仓库..."
cp -r $BACKUP_DIR/git/.git $TARGET_DIR/

# 6. 安装 Python 依赖
echo "安装 Python 依赖..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 7. 安装 Node.js 依赖
echo "安装 Node.js 依赖..."
npm install

# 8. 恢复 PM2 配置
echo"恢复 PM2 配置..."
pm2 kill
cp $BACKUP_DIR/pm2/dump.pm2 ~/.pm2/
pm2 resurrect

# 9. 启动所有服务
echo "启动所有服务..."
pm2 start ecosystem.config.js
pm2 save

# 10. 验证服务状态
echo "验证服务状态..."
pm2 status
curl -I http://localhost:5000/health

echo "✅ 系统恢复完成！"
```

---

## 📚 完整文档列表

本备份包含以下详细文档：

1. **README.md** (本文件)
   - 备份导航和快速入门指南
   - 快速恢复命令

2. **FULL_RESTORATION_GUIDE.md**
   - 完整系统恢复部署详细指南
   - 21个子系统完整说明
   - 数据库表映射关系
   - 依赖关系图
   - 故障排查指南

3. **SUBSYSTEMS_REFERENCE.md**
   - 21个子系统快速参考手册
   - 文件匹配关系速查
   - 快速启动命令
   - 常用运维命令

4. **DATABASE_SCHEMA.md**
   - 数据库完整Schema文档
   - 26张表的详细结构
   - 字段说明和索引
   - 示例数据

---

## 🎯 21个子系统列表

| # | 系统名称 | PM2进程 | 访问地址 | 主要数据表 |
|---|---------|---------|---------|-----------|
| 1 | 历史数据查询系统 | flask-app | /historical-query | crypto_snapshots |
| 2 | 交易信号监控系统 | flask-app | /trading-signals | trading_signals |
| 3 | 恐慌清洗指数系统 | panic-wash-collector | /panic-wash | panic_wash_index |
| 4 | 比价系统 | price-comparison-collector | /price-comparison | price_comparison |
| 5 | 星星系统 | flask-app | /star-rating | star_ratings |
| 6 | 币种池系统 | flask-app | /coin-pool | coin_pool |
| 7 | 实时市场原始数据 | websocket-collector | ws://localhost:8765 | market_ticker |
| 8 | 数据采集监控 | collector-monitor | /collector-monitor | collector_status |
| 9 | 深度图得分 | flask-app | /depth-score | depth_scores |
| 10 | 深度图可视化 | flask-app | /depth-chart | - |
| 11 | 平均分页面 | flask-app | /average-score | average_scores |
| 12 | OKEx加密指数 | crypto-index-collector | /crypto-index | crypto_index |
| 13 | 位置系统 | position-system-collector | /position-system | position_data |
| 14 | 支撑压力线系统 | support-resistance-collector | /support-resistance | support_resistance |
| 15 | 决策交易信号系统 | flask-app | /decision-signals | decision_signals |
| 16 | 决策-K线指标系统 | flask-app | /kline-indicators | kline_patterns |
| 17 | V1V2成交系统 | v1v2-collector | /v1v2-monitor | v1_transactions |
| 18 | 1分钟涨跌幅系统 | flask-app | /price-change-1m | price_change_1m |
| 19 | Google Drive监控系统 | gdrive-monitor | /gdrive-monitor | - |
| 20 | TG消息推送系统 | telegram-notifier | (后台服务) | - |
| 21 | 资金监控系统 | fund-monitor-collector | /fund-monitor | fund_flow |

---

## 📂 备份目录结构

```
crypto_system_full_backup_20251224_140003/
├── README.md                              # 本导航文档
├── FULL_RESTORATION_GUIDE.md              # 完整恢复指南
├── SUBSYSTEMS_REFERENCE.md                # 子系统快速参考
├── DATABASE_SCHEMA.md                     # 数据库Schema文档
│
├── source_code/                           # 源代码 (~150个文件)
│   ├── app_new.py                        # Flask主应用
│   ├── websocket_collector.py            # WebSocket采集器
│   ├── support_resistance_collector.py   # 支撑压力采集器
│   ├── sar_slope_collector.py            # SAR斜率采集器
│   ├── telegram_notifier.py              # Telegram通知器
│   └── ... (其他Python源文件)
│
├── templates/                             # HTML模板 (~30个文件)
│   ├── support_resistance.html           # 支撑压力线页面
│   ├── sar_slope_v2.html                 # SAR斜率页面
│   ├── fund_monitor.html                 # 资金监控页面
│   └── ... (其他模板文件)
│
├── static/                                # 静态资源
│   ├── css/                              # CSS样式
│   ├── js/                               # JavaScript
│   └── images/                           # 图片资源
│
├── databases/                             # 数据库文件 (2.1GB)
│   ├── crypto_data.db                    # 主数据库 (2.1GB)
│   ├── fund_monitor.db                   # 资金监控数据库 (6.7MB)
│   ├── v1v2_data.db                      # V1V2成交数据库 (12MB)
│   └── price_speed_data.db               # 价格速度数据库
│
├── configs/                               # 配置文件
│   ├── ecosystem.config.js               # PM2配置
│   ├── telegram_config.json              # Telegram配置
│   ├── daily_folder_config.json          # Google Drive配置
│   ├── .env                              # 环境变量
│   └── google_credentials.json           # Google API凭证
│
├── dependencies/                          # 依赖清单
│   ├── requirements.txt                  # Python依赖
│   ├── package.json                      # Node.js依赖
│   ├── package-lock.json                 # 版本锁定
│   └── pip_freeze.txt                    # 完整Python包列表
│
├── pm2/                                   # PM2配置和状态
│   ├── dump.pm2                          # PM2进程快照
│   ├── ecosystem.config.js               # PM2生态配置
│   ├── pm2_list.txt                      # 进程列表
│   └── pm2_prettylist.json               # 进程详细信息
│
├── git/                                   # Git仓库 (完整)
│   ├── .git/                             # Git目录
│   ├── git_history.txt                   # 提交历史
│   ├── git_status.txt                    # 仓库状态
│   ├── git_branches.txt                  # 分支列表
│   ├── git_remotes.txt                   # 远程仓库
│   └── git_latest_commit.txt             # 最新提交
│
├── logs/                                  # 日志文件
│   ├── flask-app.log
│   ├── websocket-collector.log
│   ├── support-resistance-collector.log
│   └── ... (其他日志文件)
│
└── docs/                                  # 系统文档
    └── system_info.txt                   # 系统信息
```

---

## 🔑 关键配置说明

### 数据库文件
- `crypto_data.db` (2.1GB) - 主数据库, 20张表
- `fund_monitor.db` (6.7MB) - 资金监控, 2张表
- `v1v2_data.db` (12MB) - V1V2成交, 2张表
- `price_speed_data.db` - 价格速度, 2张表

### Telegram配置
- Bot: `@jamesyi9999_bot`
- Chat ID: `-1003227444260`
- 冷却时间: 300秒
- 抄底信号: 支撑1 >= 8 AND 支撑2 >= 8
- 逃顶信号: (压力1 >= 1 AND 压力2 >= 1) AND (压力1+压力2 >= 8)

### 重要修复记录
1. **SAR Slope V2.2 API字段修正** (dcd5318)
   - 修正API字段名不匹配
   - 新增avg_1day, avg_7day, avg_15day

2. **强势抄底信号逻辑修正** (502a183)
   - 从"总和>=8"改为"都>=8"
   - 提高信号可靠性

3. **逃顶信号逻辑优化** (b9791e1)
   - 新增压力线1>=1 AND 压力线2>=1条件
   - 避免单线触碰误判

---

## ✅ 恢复验证清单

恢复完成后，请逐项验证：

### 基础环境
- [ ] Python 3.12+ 安装
- [ ] Node.js 18+ 安装
- [ ] PM2 安装
- [ ] 数据库文件存在且大小正确

### PM2进程
- [ ] 所有进程状态为 'online'
- [ ] websocket-collector 正常运行
- [ ] flask-app 正常运行
- [ ] 无进程频繁重启

### API端点
- [ ] `http://localhost:5000/health` 返回 200
- [ ] `/api/support-resistance/latest` 有数据
- [ ] `/api/sar-slope/latest` 有数据
- [ ] `/api/fund-monitor/flow?symbol=BTC-USDT-SWAP` 有数据

### Web页面
- [ ] http://localhost:5000/ (主页加载)
- [ ] /support-resistance (支撑压力线页面)
- [ ] /sar-slope (SAR斜率页面)
- [ ] /fund-monitor (资金监控页面)

### Telegram
- [ ] telegram-notifier 进程运行
- [ ] 日志显示 "Bot: jamesyi9999_bot"
- [ ] 日志显示 "Chat ID: -1003227444260"

---

## 📞 联系和支持

**开发者**: jamesyi  
**GitHub**: https://github.com/jamesyidc/66661  
**分支**: genspark_ai_developer  
**Telegram Bot**: @jamesyi9999_bot  
**Chat ID**: -1003227444260

---

## ⚠️ 重要提示

1. **安全建议**:
   - 不要上传敏感文件到公开仓库
   - `.env`, `telegram_config.json`, `google_credentials.json` 需保密
   - 定期更新备份

2. **磁盘空间**: 至少需要10GB可用空间

3. **依赖版本**: 严格按照 `requirements.txt` 和 `package-lock.json` 安装

4. **数据库**: 恢复后可能需要VACUUM优化

---

**备份创建时间**: 2025-12-24 14:00:03  
**备份有效期**: 永久（建议定期更新备份）  
**文档版本**: v2.3

---

**✨ 完整备份已创建！所有21个子系统可完全1:1还原。**
