#!/usr/bin/env python3
"""
SAR斜率数据 - 专用导出导入工具
支持从备份中提取SAR相关数据并导入到当前数据库
"""
import sqlite3
import json
import os
import tarfile
import shutil
from datetime import datetime
from typing import Dict, List, Tuple

# 数据库路径
CURRENT_DB = '/home/user/webapp/databases/crypto_data.db'
BACKUP_TAR = '/home/user/uploaded_files/crypto_system_full_backup_20251224_140003.tar.gz'
TEMP_DIR = '/tmp/sar_backup_extract'

# SAR相关的所有表
SAR_TABLES = [
    'sar_slope_v2',              # SAR斜率V2主表
    'sar_slope_data',            # SAR斜率数据表
    'sar_position_stats',        # SAR位置统计表
    'kline_technical_markers',   # K线技术指标表（包含SAR数据）
    'okex_kline_ohlc'            # OKEX K线OHLC数据
]

def extract_backup_db():
    """从备份tar.gz中提取crypto_data.db"""
    print(f"📦 正在从备份中提取数据库...")
    
    # 清理临时目录
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)
    
    # 提取tar.gz
    with tarfile.open(BACKUP_TAR, 'r:gz') as tar:
        # 查找crypto_data.db文件
        for member in tar.getmembers():
            if 'crypto_data.db' in member.name and not member.name.endswith(('.backup', '.corrupted')):
                print(f"   找到数据库文件: {member.name}")
                tar.extract(member, TEMP_DIR)
                
                # 移动到标准位置
                extracted_path = os.path.join(TEMP_DIR, member.name)
                backup_db_path = os.path.join(TEMP_DIR, 'crypto_data.db')
                shutil.move(extracted_path, backup_db_path)
                
                print(f"   ✅ 数据库已提取到: {backup_db_path}")
                return backup_db_path
    
    raise FileNotFoundError("备份中未找到crypto_data.db文件")

def get_table_schema(conn, table_name):
    """获取表的创建语句"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_table_indexes(conn, table_name):
    """获取表的所有索引创建语句"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name=? AND sql IS NOT NULL", (table_name,))
    return [row[0] for row in cursor.fetchall()]

def export_sar_data_to_json(output_file='/home/user/webapp/exports/sar_data_export.json'):
    """导出SAR数据到JSON文件"""
    print(f"\n📤 导出SAR数据到JSON...")
    
    # 提取备份数据库
    backup_db = extract_backup_db()
    conn = sqlite3.connect(backup_db)
    cursor = conn.cursor()
    
    export_data = {
        'export_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'source': BACKUP_TAR,
        'tables': {}
    }
    
    # 获取每个表的数据
    for table in SAR_TABLES:
        try:
            # 检查表是否存在
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            if not cursor.fetchone():
                print(f"   ⚠️  表 {table} 不存在，跳过")
                continue
            
            # 获取表结构
            schema = get_table_schema(conn, table)
            indexes = get_table_indexes(conn, table)
            
            # 获取数据
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            
            # 获取列名
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cursor.fetchall()]
            
            # 转换为字典列表
            data = [dict(zip(columns, row)) for row in rows]
            
            export_data['tables'][table] = {
                'schema': schema,
                'indexes': indexes,
                'row_count': len(data),
                'columns': columns,
                'data': data
            }
            
            print(f"   ✅ {table}: {len(data):,} 条记录")
            
        except sqlite3.Error as e:
            print(f"   ❌ 导出 {table} 失败: {e}")
            continue
    
    conn.close()
    
    # 保存到JSON
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    file_size = os.path.getsize(output_file) / 1024 / 1024
    print(f"\n✅ 导出完成！")
    print(f"   文件: {output_file}")
    print(f"   大小: {file_size:.2f} MB")
    
    # 清理临时文件
    shutil.rmtree(TEMP_DIR)
    
    return output_file

def import_sar_data_from_json(json_file='/home/user/webapp/exports/sar_data_export.json'):
    """从JSON文件导入SAR数据"""
    print(f"\n📥 从JSON导入SAR数据...")
    
    if not os.path.exists(json_file):
        print(f"❌ 文件不存在: {json_file}")
        return False
    
    # 读取JSON数据
    with open(json_file, 'r', encoding='utf-8') as f:
        export_data = json.load(f)
    
    print(f"   数据来源: {export_data['export_time']}")
    print(f"   包含表: {', '.join(export_data['tables'].keys())}")
    
    # 连接当前数据库
    conn = sqlite3.connect(CURRENT_DB)
    cursor = conn.cursor()
    
    try:
        # 按顺序导入每个表
        for table, table_data in export_data['tables'].items():
            print(f"\n   📋 处理表: {table}")
            
            # 创建表（如果不存在）
            if table_data['schema']:
                cursor.execute(table_data['schema'])
                print(f"      ✅ 表结构已创建")
            
            # 创建索引
            for index_sql in table_data['indexes']:
                try:
                    cursor.execute(index_sql)
                except sqlite3.Error:
                    pass  # 索引可能已存在
            
            # 导入数据
            if table_data['data']:
                columns = table_data['columns']
                placeholders = ','.join(['?' for _ in columns])
                
                # 批量插入
                insert_sql = f"INSERT OR REPLACE INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
                
                batch_size = 1000
                total_rows = len(table_data['data'])
                
                for i in range(0, total_rows, batch_size):
                    batch = table_data['data'][i:i+batch_size]
                    values = [tuple(row[col] for col in columns) for row in batch]
                    cursor.executemany(insert_sql, values)
                    
                    if (i + batch_size) % 10000 == 0:
                        print(f"      进度: {min(i+batch_size, total_rows):,}/{total_rows:,}")
                
                print(f"      ✅ 导入 {total_rows:,} 条记录")
        
        conn.commit()
        print(f"\n✅ 所有数据导入成功！")
        return True
        
    except sqlite3.Error as e:
        conn.rollback()
        print(f"\n❌ 导入失败: {e}")
        return False
    finally:
        conn.close()

def get_sar_data_summary():
    """获取SAR数据摘要信息"""
    print(f"\n📊 SAR数据摘要:")
    
    conn = sqlite3.connect(CURRENT_DB)
    cursor = conn.cursor()
    
    summary = {}
    
    for table in SAR_TABLES:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            summary[table] = count
            print(f"   {table:30s}: {count:,} 条记录")
        except sqlite3.Error:
            print(f"   {table:30s}: 表不存在")
            summary[table] = 0
    
    conn.close()
    return summary

def direct_copy_tables():
    """直接从备份数据库复制SAR相关表到当前数据库"""
    print(f"\n🚀 直接复制SAR数据表...")
    
    # 提取备份数据库
    backup_db = extract_backup_db()
    
    # 连接两个数据库
    source_conn = sqlite3.connect(backup_db)
    target_conn = sqlite3.connect(CURRENT_DB)
    
    source_cursor = source_conn.cursor()
    target_cursor = target_conn.cursor()
    
    copied_tables = []
    
    for table in SAR_TABLES:
        try:
            # 检查源表是否存在
            source_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            if not source_cursor.fetchone():
                print(f"   ⚠️  源表 {table} 不存在，跳过")
                continue
            
            # 获取行数
            source_cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row_count = source_cursor.fetchone()[0]
            
            if row_count == 0:
                print(f"   ⚠️  表 {table} 无数据，跳过")
                continue
            
            # 获取表结构
            schema = get_table_schema(source_conn, table)
            indexes = get_table_indexes(source_conn, table)
            
            # 在目标数据库创建表
            target_cursor.execute(f"DROP TABLE IF EXISTS {table}")
            target_cursor.execute(schema)
            
            # 创建索引
            for index_sql in indexes:
                try:
                    target_cursor.execute(index_sql)
                except sqlite3.Error:
                    pass
            
            # 使用ATTACH复制数据
            target_cursor.execute(f"ATTACH DATABASE '{backup_db}' AS source_db")
            target_cursor.execute(f"INSERT INTO {table} SELECT * FROM source_db.{table}")
            target_cursor.execute("DETACH DATABASE source_db")
            
            target_conn.commit()
            
            copied_tables.append(table)
            print(f"   ✅ {table}: {row_count:,} 条记录已复制")
            
        except sqlite3.Error as e:
            print(f"   ❌ 复制 {table} 失败: {e}")
            continue
    
    source_conn.close()
    target_conn.close()
    
    # 清理临时文件
    shutil.rmtree(TEMP_DIR)
    
    print(f"\n✅ 复制完成！共处理 {len(copied_tables)} 个表")
    return copied_tables

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("""
SAR斜率数据导出导入工具

用法:
    python3 sar_export_import.py export       # 导出SAR数据到JSON
    python3 sar_export_import.py import       # 从JSON导入SAR数据
    python3 sar_export_import.py copy         # 直接复制表（推荐，最快）
    python3 sar_export_import.py summary      # 查看当前SAR数据摘要
        """)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'export':
        export_sar_data_to_json()
        get_sar_data_summary()
    elif command == 'import':
        json_file = sys.argv[2] if len(sys.argv) > 2 else '/home/user/webapp/exports/sar_data_export.json'
        import_sar_data_from_json(json_file)
        get_sar_data_summary()
    elif command == 'copy':
        direct_copy_tables()
        get_sar_data_summary()
    elif command == 'summary':
        get_sar_data_summary()
    else:
        print(f"❌ 未知命令: {command}")
        sys.exit(1)
