# 支撑压力线快照数据 - 导入导出指南

## 概述

本系统提供了独立的快照数据（`support_resistance_snapshots`）导入导出功能，用于备份和恢复趋势图数据。

## 快照数据说明

- **表名**: `support_resistance_snapshots`
- **用途**: 存储每小时的市场快照数据，用于生成全局趋势图和12小时趋势图
- **数据内容**: 
  - 4种告警场景的币种统计
  - 每小时的市场状态汇总
  - 支持时间范围查询

## 导出数据

### 基本用法

```bash
cd /home/user/webapp
python3 export_snapshots.py
```

### 输出示例

```
开始导出快照数据...
数据库: databases/support_resistance.db
输出文件: support_resistance_snapshots_backup_20251224_153758.json

✅ 导出完成！
  记录数: 152
  时间范围: 2025-12-12 21:00:00 ~ 2025-12-24 18:00:00
  文件大小: 55.2 KB
```

### 输出文件

- 文件名格式: `support_resistance_snapshots_backup_YYYYMMDD_HHMMSS.json`
- 存放位置: `/home/user/webapp/`
- 包含内容:
  - 导出时间和元信息
  - 完整的快照数据记录
  - 时间范围统计

## 导入数据

### 基本用法

```bash
cd /home/user/webapp
python3 import_snapshots.py <json_file>
```

### 示例

```bash
# 导入备份文件
python3 import_snapshots.py support_resistance_snapshots_backup_20251224_153758.json

# 导入后会询问是否清空现有数据
⚠️  数据库中已有 152 条记录
是否清空现有数据？(y/n): y
```

### 输出示例

```
开始导入快照数据...
数据库: databases/support_resistance.db
导入文件: support_resistance_snapshots_backup_20251224_153758.json

📊 备份文件信息:
  导出时间: 2025-12-24 15:37:58
  记录数: 152
  时间范围: 2025-12-12 21:00:00 ~ 2025-12-24 18:00:00

✅ 已清空现有数据

开始导入...
  已导入 50 条...
  已导入 100 条...
  已导入 150 条...

✅ 导入完成！
  成功: 152 条
  失败: 0 条

📊 数据库验证:
  总记录数: 152
  时间范围: 2025-12-12 21:00:00 ~ 2025-12-24 18:00:00
```

## 数据结构

### JSON备份文件格式

```json
{
  "export_info": {
    "export_time": "2025-12-24 15:37:58",
    "export_timestamp": 1703426278,
    "record_count": 152,
    "time_range": "2025-12-12 21:00:00 ~ 2025-12-24 18:00:00"
  },
  "data": [
    {
      "snapshot_time": "2025-12-12 21:00:00",
      "snapshot_date": "2025-12-12",
      "scenario_1_count": 0,
      "scenario_1_coins": "",
      "scenario_2_count": 0,
      "scenario_2_coins": "",
      "scenario_3_count": 0,
      "scenario_3_coins": "",
      "scenario_4_count": 0,
      "scenario_4_coins": "",
      "total_coins": 27,
      "created_at": "2025-12-24 15:29:16"
    }
  ]
}
```

### 数据字段说明

- `snapshot_time`: 快照时间（精确到小时）
- `snapshot_date`: 快照日期
- `scenario_X_count`: 场景X触发的币种数量
- `scenario_X_coins`: 场景X触发的币种列表（逗号分隔）
- `total_coins`: 参与统计的总币种数
- `created_at`: 记录创建时间

## 使用场景

### 1. 定期备份

建议每天导出一次快照数据作为备份：

```bash
# 添加到crontab
0 2 * * * cd /home/user/webapp && python3 export_snapshots.py
```

### 2. 数据迁移

在系统迁移或升级时，可以：

1. 导出旧系统的快照数据
2. 在新系统中导入数据
3. 验证数据完整性

### 3. 数据恢复

如果快照数据损坏或丢失：

1. 使用最近的备份文件
2. 运行导入命令
3. 选择清空现有数据
4. 验证恢复结果

## 注意事项

⚠️ **重要提示**:

1. **数据覆盖**: 导入时选择"y"会清空现有数据，请谨慎操作
2. **时间连续性**: 导入后的数据时间范围可能与当前不连续
3. **自动生成**: 系统会自动从`support_resistance_levels`生成新的快照数据
4. **备份频率**: 建议每日备份，保留最近7天的备份文件

## 验证数据

### 检查数据库

```bash
cd /home/user/webapp
python3 << 'EOF'
import sqlite3

conn = sqlite3.connect('databases/support_resistance.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT 
        COUNT(*) as total,
        MIN(snapshot_time) as earliest,
        MAX(snapshot_time) as latest
    FROM support_resistance_snapshots
""")

result = cursor.fetchone()
print(f"总记录数: {result[0]}")
print(f"时间范围: {result[1]} ~ {result[2]}")

conn.close()
EOF
```

### 测试API

```bash
# 测试快照API
curl "https://5000-i9bkvk3wxta0ezvqb4epz-b9b802c4.sandbox.novita.ai/api/support-resistance/snapshots?all=true"
```

## 故障排除

### 问题1: 导入失败 - Decimal类型错误

**解决方案**: 已在`import_snapshots.py`中自动处理Decimal转换

### 问题2: 导入后趋势图无数据

**检查步骤**:
1. 验证数据库中有记录
2. 检查时间范围是否正确
3. 重启Flask应用：`pm2 restart flask-app`

### 问题3: 快照数量为0

**生成快照数据**:
```bash
# 手动触发快照生成（如需要）
pm2 restart support-resistance-snapshot-collector
```

## 相关文件

- `export_snapshots.py` - 导出工具
- `import_snapshots.py` - 导入工具
- `databases/support_resistance.db` - 数据库文件
- `support_resistance_collector.py` - 原始数据采集器
- `support_resistance_routes.py` - API路由

## 技术支持

如有问题，请检查：

1. PM2服务状态: `pm2 list`
2. 日志文件: `pm2 logs telegram-notifier`
3. 数据库状态: 运行上述验证命令

---

**最后更新**: 2025-12-24
**版本**: 1.0
