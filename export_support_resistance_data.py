#!/usr/bin/env python3
"""
支撑/阻力位系统 - 趋势图数据导出工具
导出内容: support_resistance_snapshots (趋势图快照数据)

这个工具专门用于导出/备份趋势图数据
导出格式: JSON（包含完整数据和元数据）
"""
import sqlite3
import json
import os
from datetime import datetime
import pytz

DB_PATH = "/home/user/webapp/databases/support_resistance.db"
EXPORT_DIR = "/home/user/webapp/exports"
BEIJING_TZ = pytz.timezone('Asia/Shanghai')

def log(message):
    """打印带时间戳的日志"""
    timestamp = datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}", flush=True)

def ensure_export_dir():
    """确保导出目录存在"""
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)
        log(f"✅ 创建导出目录: {EXPORT_DIR}")

def export_snapshots_data():
    """导出趋势图快照数据"""
    log("")
    log("=" * 80)
    log("📊 趋势图数据导出工具")
    log("=" * 80)
    log("")
    
    # 确保导出目录存在
    ensure_export_dir()
    
    # 连接数据库
    log("🔌 连接数据库...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    log(f"✅ 数据库连接成功: {DB_PATH}")
    log("")
    
    # 导出快照数据
    log("📊 开始导出 support_resistance_snapshots 表...")
    
    # 获取表结构
    cursor.execute("PRAGMA table_info(support_resistance_snapshots)")
    columns_info = cursor.fetchall()
    columns = [col[1] for col in columns_info]
    log(f"   字段数: {len(columns)}")
    
    # 获取所有快照数据
    cursor.execute("SELECT * FROM support_resistance_snapshots ORDER BY snapshot_time")
    rows = cursor.fetchall()
    log(f"   记录数: {len(rows)}")
    
    # 获取时间范围
    if rows:
        cursor.execute("""
            SELECT 
                MIN(snapshot_time) as earliest,
                MAX(snapshot_time) as latest
            FROM support_resistance_snapshots
        """)
        time_range = cursor.fetchone()
        log(f"   时间范围: {time_range[0]} ~ {time_range[1]}")
    
    # 转换为字典列表
    data = []
    for row in rows:
        record = {}
        for i, value in enumerate(row):
            record[columns[i]] = value
        data.append(record)
    
    conn.close()
    
    # 构建导出数据
    export_data = {
        'export_info': {
            'export_time': datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S'),
            'export_timestamp': int(datetime.now(BEIJING_TZ).timestamp()),
            'database_path': DB_PATH,
            'table_name': 'support_resistance_snapshots',
            'record_count': len(rows),
            'time_range': f"{time_range[0]} ~ {time_range[1]}" if rows else "无数据",
            'version': '2.0',
            'description': '趋势图快照数据备份'
        },
        'data': data
    }
    
    # 生成导出文件名
    export_filename = f"support_resistance_snapshots_backup_{datetime.now(BEIJING_TZ).strftime('%Y%m%d_%H%M%S')}.json"
    export_path = os.path.join(EXPORT_DIR, export_filename)
    
    # 保存为JSON文件
    log("")
    log("💾 保存导出数据...")
    with open(export_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    # 获取文件大小
    file_size = os.path.getsize(export_path)
    file_size_kb = file_size / 1024
    
    log("")
    log("=" * 80)
    log("✅ 趋势图数据导出完成！")
    log("=" * 80)
    log("")
    log(f"📁 导出文件: {export_path}")
    log(f"📊 文件大小: {file_size_kb:.2f} KB ({file_size:,} bytes)")
    log(f"📈 导出统计:")
    log(f"   快照记录数: {len(rows):,}")
    if rows:
        log(f"   时间范围: {time_range[0]} ~ {time_range[1]}")
    log("")
    log("💡 说明: 此文件包含趋势图的所有快照数据")
    log("   可用于趋势图数据的备份和恢复")
    log("")
    log("🎉 导出成功！")
    log("")
    
    return export_path

if __name__ == '__main__':
    export_snapshots_data()
