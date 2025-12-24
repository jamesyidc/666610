#!/usr/bin/env python3
"""
Support Resistance Snapshots 导入工具
功能：从JSON备份文件导入快照数据到数据库
"""
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
import decimal

def float_converter(obj):
    """转换Decimal和其他非JSON兼容类型为float"""
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    return obj

def import_snapshots(json_file, db_path='databases/support_resistance.db'):
    """导入快照数据"""
    print(f"开始导入快照数据...")
    print(f"数据库: {db_path}")
    print(f"导入文件: {json_file}\n")
    
    if not Path(json_file).exists():
        print(f"❌ 错误：文件不存在: {json_file}")
        sys.exit(1)
    
    # 读取JSON数据
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    export_info = data.get('export_info', {})
    snapshots = data.get('data', [])
    
    print(f"📊 备份文件信息:")
    print(f"  导出时间: {export_info.get('export_time', 'unknown')}")
    print(f"  记录数: {export_info.get('record_count', 0)}")
    print(f"  时间范围: {export_info.get('time_range', 'unknown')}\n")
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查表是否存在
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='support_resistance_snapshots'
    """)
    if not cursor.fetchone():
        print("❌ 错误：表 support_resistance_snapshots 不存在")
        conn.close()
        sys.exit(1)
    
    # 询问是否清空现有数据
    cursor.execute("SELECT COUNT(*) FROM support_resistance_snapshots")
    existing_count = cursor.fetchone()[0]
    
    if existing_count > 0:
        print(f"⚠️  数据库中已有 {existing_count} 条记录")
        response = input("是否清空现有数据？(y/n): ")
        if response.lower() == 'y':
            cursor.execute("DELETE FROM support_resistance_snapshots")
            print("✅ 已清空现有数据\n")
    
    # 导入数据
    imported = 0
    errors = 0
    
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
    
    print("开始导入...")
    for record in snapshots:
        try:
            # 转换Decimal为float
            values = [float_converter(v) if isinstance(v, decimal.Decimal) else v 
                     for v in [
                record['snapshot_time'],
                record['snapshot_date'],
                record['scenario_1_count'],
                record['scenario_1_coins'],
                record['scenario_2_count'],
                record['scenario_2_coins'],
                record['scenario_3_count'],
                record['scenario_3_coins'],
                record['scenario_4_count'],
                record['scenario_4_coins'],
                record['total_coins'],
                record['created_at']
            ]]
            
            cursor.execute(insert_sql, values)
            imported += 1
            
            if imported % 50 == 0:
                print(f"  已导入 {imported} 条...")
                
        except Exception as e:
            errors += 1
            print(f"  ❌ 导入失败: {record.get('snapshot_time', 'unknown')} - {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ 导入完成！")
    print(f"  成功: {imported} 条")
    print(f"  失败: {errors} 条")
    
    if imported > 0:
        # 验证导入
        conn = sqlite3.connect(db_path)
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
        
        print(f"\n📊 数据库验证:")
        print(f"  总记录数: {result[0]}")
        print(f"  时间范围: {result[1]} ~ {result[2]}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使用方法: python3 import_snapshots.py <json_file>")
        print("示例: python3 import_snapshots.py support_resistance_snapshots_backup_20251224_153758.json")
        sys.exit(1)
    
    json_file = sys.argv[1]
    import_snapshots(json_file)
