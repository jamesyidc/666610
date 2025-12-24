#!/usr/bin/env python3
"""
支撑/阻力位系统 - 趋势图数据导入工具
导入内容: support_resistance_snapshots (趋势图快照数据)

这个工具专门用于导入/恢复趋势图数据
支持命令行参数: --clear (清空现有数据)
"""
import sqlite3
import json
import sys
import os
from datetime import datetime
import pytz
import decimal

DB_PATH = "/home/user/webapp/databases/support_resistance.db"
BEIJING_TZ = pytz.timezone('Asia/Shanghai')

def log(message):
    """打印带时间戳的日志"""
    timestamp = datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}", flush=True)

def float_converter(obj):
    """转换Decimal和其他非JSON兼容类型为float"""
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    return obj

def import_snapshots(json_file, clear_existing=False):
    """导入趋势图快照数据"""
    log("")
    log("=" * 80)
    log("📊 趋势图数据导入工具")
    log("=" * 80)
    log("")
    log(f"数据库: {DB_PATH}")
    log(f"导入文件: {json_file}")
    log("")
    
    if not os.path.exists(json_file):
        log(f"❌ 错误：文件不存在: {json_file}")
        sys.exit(1)
    
    # 读取JSON数据
    log("📖 读取导入文件...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    export_info = data.get('export_info', {})
    snapshots = data.get('data', [])
    
    log(f"✅ 文件读取成功")
    log("")
    log(f"📊 备份文件信息:")
    log(f"   导出时间: {export_info.get('export_time', 'unknown')}")
    log(f"   记录数: {export_info.get('record_count', 0)}")
    log(f"   时间范围: {export_info.get('time_range', 'unknown')}")
    log(f"   版本: {export_info.get('version', '1.0')}")
    log("")
    
    # 连接数据库
    log("🔌 连接数据库...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    log("✅ 数据库连接成功")
    log("")
    
    # 检查表是否存在
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='support_resistance_snapshots'
    """)
    if not cursor.fetchone():
        log("❌ 错误：表 support_resistance_snapshots 不存在")
        conn.close()
        sys.exit(1)
    
    # 检查现有数据
    cursor.execute("SELECT COUNT(*) FROM support_resistance_snapshots")
    existing_count = cursor.fetchone()[0]
    
    if existing_count > 0:
        log(f"⚠️  数据库中已有 {existing_count} 条快照记录")
        if clear_existing:
            log("⚠️  --clear 参数已指定，将清空现有数据")
            cursor.execute("DELETE FROM support_resistance_snapshots")
            log("✅ 已清空现有数据")
        else:
            log("⚠️  将追加导入（不清空现有数据）")
        log("")
    
    # 导入数据
    imported = 0
    errors = 0
    skipped = 0
    
    insert_sql = """
        INSERT INTO support_resistance_snapshots (
            snapshot_time, snapshot_date,
            scenario_1_count, scenario_1_coins,
            scenario_2_count, scenario_2_coins,
            scenario_3_count, scenario_3_coins,
            scenario_4_count, scenario_4_coins,
            total_coins, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    log("📥 开始导入数据...")
    log("")
    
    for record in snapshots:
        try:
            # 检查是否已存在
            cursor.execute(
                "SELECT COUNT(*) FROM support_resistance_snapshots WHERE snapshot_time = ?",
                (record['snapshot_time'],)
            )
            if cursor.fetchone()[0] > 0 and not clear_existing:
                skipped += 1
                continue
            
            # 转换Decimal为float
            values = [
                record['snapshot_time'],
                record['snapshot_date'],
                record['scenario_1_count'],
                record.get('scenario_1_coins', ''),
                record['scenario_2_count'],
                record.get('scenario_2_coins', ''),
                record['scenario_3_count'],
                record.get('scenario_3_coins', ''),
                record['scenario_4_count'],
                record.get('scenario_4_coins', ''),
                record['total_coins'],
                record.get('created_at', datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S'))
            ]
            
            cursor.execute(insert_sql, values)
            imported += 1
            
            if imported % 50 == 0:
                log(f"  已导入 {imported} 条...")
                
        except Exception as e:
            errors += 1
            log(f"  ❌ 导入失败: {record.get('snapshot_time', 'unknown')} - {e}")
    
    conn.commit()
    conn.close()
    
    log("")
    log("=" * 80)
    log("✅ 趋势图数据导入完成！")
    log("=" * 80)
    log("")
    log(f"📊 导入统计:")
    log(f"   成功导入: {imported} 条")
    if skipped > 0:
        log(f"   跳过重复: {skipped} 条")
    if errors > 0:
        log(f"   导入失败: {errors} 条")
    log("")
    
    if imported > 0:
        # 验证导入
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                MIN(snapshot_time) as earliest,
                MAX(snapshot_time) as latest
            FROM support_resistance_snapshots
        """)
        result = cursor.fetchone()
        conn.close()
        
        log(f"📈 数据库验证:")
        log(f"   总记录数: {result[0]}")
        log(f"   时间范围: {result[1]} ~ {result[2]}")
        log("")
    
    log("🎉 导入成功！")
    log("")
    
    return imported

if __name__ == '__main__':
    if len(sys.argv) < 2:
        log("使用方法: python3 import_support_resistance_data.py <json_file> [--clear]")
        log("示例: python3 import_support_resistance_data.py backup.json --clear")
        sys.exit(1)
    
    json_file = sys.argv[1]
    clear_existing = '--clear' in sys.argv
    
    import_snapshots(json_file, clear_existing)
