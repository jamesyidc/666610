# SAR斜率数据导出导入系统使用指南

## 📋 概述

本文档介绍SAR斜率数据的完整导出导入解决方案，解决数据库损坏或迁移时的数据恢复问题。

## 🔧 系统组件

### 1. 数据库表结构

#### `sar_slope_v2` - SAR斜率V2主表
```sql
- id: 主键
- symbol: 币种符号
- timestamp: Unix时间戳
- datetime_beijing: 北京时间
- sar_value: SAR值
- sar_direction: SAR方向 (多/空)
- sequence_number: 连续序号
- sar_diff: SAR差值
- sar_diff_percent: SAR差值百分比
- avg_1day, avg_3day, avg_7day, avg_15day: 平均值
- is_anomaly: 是否异常
- anomaly_type: 异常类型
- is_extreme: 是否极值
- extreme_type: 极值类型
- price_open, price_close, price_high, price_low: 价格数据
```

#### `kline_technical_markers` - K线技术指标表
```sql
- symbol: 币种符号
- timeframe: 时间周期 (如 5m)
- timestamp: Unix时间戳
- sar: SAR指标值
- sar_position: SAR位置
- sar_quadrant: SAR象限
```

#### `okex_kline_ohlc` - OKEX K线OHLC数据
```sql
- symbol: 币种符号
- timeframe: 时间周期
- timestamp: Unix时间戳
- open, high, low, close: OHLC价格
- volume: 交易量
```

### 2. 命令行工具

**脚本**: `sar_export_import.py`

#### 使用方法

```bash
# 导出SAR数据到JSON (从备份提取)
python3 sar_export_import.py export

# 从JSON导入SAR数据
python3 sar_export_import.py import [json_file]

# 直接复制表 (最快，推荐)
python3 sar_export_import.py copy

# 查看当前SAR数据摘要
python3 sar_export_import.py summary
```

#### 导出说明
- **export**: 从备份tar.gz中提取数据库，导出SAR相关表到JSON
- **导出文件**: `/home/user/webapp/exports/sar_data_export.json`
- **包含表**: `sar_slope_v2`, `sar_slope_data`, `sar_position_stats`, `kline_technical_markers`, `okex_kline_ohlc`

#### 导入说明
- **import**: 从JSON文件批量导入数据到当前数据库
- **特性**: 使用 `INSERT OR REPLACE` 避免重复
- **批量处理**: 每批1000条记录，提升效率

#### 直接复制说明
- **copy**: 使用 ATTACH 数据库直接复制表
- **速度**: 最快的数据恢复方式
- **适用**: 大数据量快速恢复

### 3. Web API 接口

#### 📤 导出API

**端点**: `GET /api/sar-slope/export`

**参数**:
- `symbol` (可选): 指定币种，如 `BTC-USDT-SWAP`
- `days` (可选): 导出天数，默认7天

**示例**:
```bash
# 导出所有币种最近7天数据
curl "http://localhost:5000/api/sar-slope/export"

# 导出BTC最近30天数据
curl "http://localhost:5000/api/sar-slope/export?symbol=BTC-USDT-SWAP&days=30"

# 保存到文件
curl "http://localhost:5000/api/sar-slope/export" -o sar_data.json
```

**响应格式**:
```json
{
  "success": true,
  "export": {
    "export_time": "2025-12-25 00:00:00",
    "days": 7,
    "symbol": "ALL",
    "symbol_count": 27,
    "record_count": 15000,
    "data": [
      {
        "id": 1,
        "symbol": "BTC-USDT-SWAP",
        "timestamp": 1735084800,
        "datetime_beijing": "2025-12-25 00:00:00",
        "sar_value": 95000.5,
        "sar_direction": "多",
        ...
      }
    ]
  }
}
```

#### 📥 导入API

**端点**: `POST /api/sar-slope/import`

**请求体**:
```json
{
  "data": [
    {
      "symbol": "BTC-USDT-SWAP",
      "timestamp": 1735084800,
      "datetime_beijing": "2025-12-25 00:00:00",
      "sar_value": 95000.5,
      ...
    }
  ]
}
```

**示例**:
```bash
# 从JSON文件导入
curl -X POST http://localhost:5000/api/sar-slope/import \
  -H "Content-Type: application/json" \
  -d @sar_data.json

# 或使用jq处理导出结果
curl "http://localhost:5000/api/sar-slope/export" | \
  jq '.export' | \
  curl -X POST http://localhost:5000/api/sar-slope/import \
    -H "Content-Type: application/json" \
    -d @-
```

**响应格式**:
```json
{
  "success": true,
  "imported": 14500,
  "skipped": 500,
  "total": 15000
}
```

#### 📊 统计API

**端点**: `GET /api/sar-slope/stats`

**示例**:
```bash
curl "http://localhost:5000/api/sar-slope/stats"
```

**响应格式**:
```json
{
  "success": true,
  "stats": {
    "total_records": 150000,
    "symbol_count": 27,
    "earliest_record": "2025-12-18 00:00:00",
    "latest_record": "2025-12-25 00:00:00",
    "symbols": [
      {"symbol": "BTC-USDT-SWAP", "count": 5600},
      {"symbol": "ETH-USDT-SWAP", "count": 5580},
      ...
    ]
  }
}
```

## 🚀 使用场景

### 场景1: 数据库损坏恢复

当 `crypto_data.db` 损坏时，需要从备份恢复SAR数据：

```bash
# 步骤1: 使用命令行工具导出
cd /home/user/webapp
python3 sar_export_import.py export

# 步骤2: 检查导出文件
ls -lh exports/sar_data_export.json

# 步骤3: 导入到新数据库
python3 sar_export_import.py import

# 步骤4: 验证数据
python3 sar_export_import.py summary
```

### 场景2: 定期备份

使用Web API定期备份SAR数据到外部存储：

```bash
# 每天备份一次
0 2 * * * curl "http://localhost:5000/api/sar-slope/export?days=30" \
  -o "/backups/sar_backup_$(date +\%Y\%m\%d).json"
```

### 场景3: 数据迁移

从旧服务器迁移SAR数据到新服务器：

```bash
# 旧服务器: 导出数据
curl "http://old-server:5000/api/sar-slope/export?days=90" -o sar_data.json

# 新服务器: 导入数据
curl -X POST http://new-server:5000/api/sar-slope/import \
  -H "Content-Type: application/json" \
  -d @sar_data.json
```

### 场景4: 单个币种数据管理

导出和导入特定币种的数据：

```bash
# 导出BTC数据
curl "http://localhost:5000/api/sar-slope/export?symbol=BTC-USDT-SWAP&days=365" \
  -o btc_sar_data.json

# 导入到另一个系统
curl -X POST http://other-server:5000/api/sar-slope/import \
  -H "Content-Type: application/json" \
  -d @btc_sar_data.json
```

## 📝 注意事项

### 1. 备份文件问题
- **当前备份已损坏**: `/home/user/uploaded_files/crypto_system_full_backup_20251224_140003.tar.gz` 中的 `crypto_data.db` 已损坏
- **原因**: 备份时数据库就已经损坏
- **教训**: 需要在备份前验证数据库完整性

### 2. 数据采集要求
- SAR斜率系统依赖 `kline_technical_markers` 和 `okex_kline_ohlc` 表
- 这些表需要其他采集器（websocket-collector等）正常运行
- 如果这些表为空，`sar-slope-collector` 无法生成新数据

### 3. 性能考虑
- 大数据量导出（>100万条）可能需要较长时间
- 建议使用 `days` 参数限制导出范围
- 导入时使用批量处理，每批1000条

### 4. 数据完整性
- 导入使用 `INSERT OR REPLACE`，会覆盖重复记录
- 导出前检查数据库状态：`python3 sar_export_import.py summary`
- 导入后验证记录数：`curl http://localhost:5000/api/sar-slope/stats`

## 🔍 故障排查

### 问题1: 导出时提示数据库损坏
```bash
❌ 复制 sar_slope_v2 失败: database disk image is malformed
```

**解决方案**:
- 备份本身已损坏，无法恢复
- 需要寻找其他备份文件
- 或从头开始重新采集数据

### 问题2: 导入失败
```bash
❌ 导入失败: no such table: sar_slope_v2
```

**解决方案**:
```bash
# 确保表已创建
python3 -c "
import sqlite3
conn = sqlite3.connect('/home/user/webapp/databases/crypto_data.db')
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\" AND name LIKE \"%sar%\"')
print(cursor.fetchall())
"
```

### 问题3: SAR页面显示空白
```bash
# 检查数据是否存在
curl "http://localhost:5000/api/sar-slope/stats"

# 检查采集器状态
pm2 logs sar-slope-collector --lines 50
```

**可能原因**:
- `sar_slope_v2` 表为空（无历史数据）
- `kline_technical_markers` 表为空（上游数据缺失）
- `sar-slope-collector` 未运行或报错

## 📊 相关文件

- **采集器脚本**: `/home/user/webapp/sar_slope_collector.py`
- **导出导入工具**: `/home/user/webapp/sar_export_import.py`
- **Flask应用**: `/home/user/webapp/app_new.py` (包含API接口)
- **PM2配置**: `/home/user/webapp/ecosystem.config.js`
- **数据库**: `/home/user/webapp/databases/crypto_data.db`
- **日志**: `/home/user/webapp/logs/sar-slope-collector-*.log`

## 🎯 总结

SAR斜率数据导出导入系统提供了三种数据管理方式：

1. **命令行工具** (`sar_export_import.py`): 适合一次性大批量数据恢复
2. **Web API** (`/api/sar-slope/export|import`): 适合自动化备份和远程数据同步
3. **直接复制** (`copy`命令): 适合快速数据库表迁移

根据您的使用场景选择合适的方式。建议：
- **日常备份**: 使用Web API的export接口
- **数据恢复**: 使用命令行工具的copy命令
- **数据同步**: 使用Web API的export + import组合

---

**最后更新**: 2025-12-25  
**版本**: v1.0  
**作者**: AI Assistant
