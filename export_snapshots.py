#!/usr/bin/env python3
"""
导出 support_resistance_snapshots 表数据
"""
import sqlite3
import json
from datetime import datetime
import sys

def export_snapshots(db_path='databases/support_resistance.db', output_file=None):
    """导出快照数据到JSON文件"""
    
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'support_resistance_snapshots_backup_{timestamp}.json'
    
    print(f"开始导出快照数据...")
    print(f"数据库: {db_path}")
    print(f"输出文件: {output_file}")
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 获取表结构
    cursor.execute("PRAGMA table_info(support_resistance_snapshots)")
    columns = [row['name'] for row in cursor.fetchall()]
    
    # 获取所有数据
    cursor.execute("SELECT * FROM support_resistance_snapshots ORDER BY snapshot_time")
    rows = cursor.fetchall()
    
    # 转换为字典列表
    data = [dict(row) for row in rows]
    
    # 创建导出对象
    export_data = {
        'export_info': {
            'export_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'database_path': db_path,
            'table_name': 'support_resistance_snapshots',
            'version': '1.0'
        },
        'table': {
            'table_name': 'support_resistance_snapshots',
            'row_count': len(data),
            'columns': columns,
            'data': data
        }
    }
    
    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    conn.close()
    
    print(f"\n✅ 导出完成！")
    print(f"  记录数: {len(data)}")
    print(f"  时间范围: {data[0]['snapshot_time']} ~ {data[-1]['snapshot_time']}")
    print(f"  文件大小: {len(json.dumps(export_data)) / 1024:.1f} KB")
    
    return output_file

if __name__ == '__main__':
    output_file = sys.argv[1] if len(sys.argv) > 1 else None
    export_snapshots(output_file=output_file)

