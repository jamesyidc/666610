"""
支撑压力线API接口封装
使用专用的support_resistance.db数据库
"""
import sqlite3
from flask import jsonify
from db_config import SUPPORT_RESISTANCE_DB

def get_latest_support_resistance():
    """获取最新的支撑压力线数据"""
    try:
        conn = sqlite3.connect(SUPPORT_RESISTANCE_DB)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 获取最新时间
        cursor.execute("SELECT MAX(record_time) as latest_time FROM support_resistance_levels")
        latest_time = cursor.fetchone()['latest_time']
        
        if not latest_time:
            return {'success': False, 'message': 'No data available'}
        
        # 获取该时间的所有数据
        cursor.execute('''
            SELECT 
                symbol, current_price, 
                support_line_1, support_line_2,
                resistance_line_1, resistance_line_2,
                distance_to_support_1, distance_to_support_2,
                distance_to_resistance_1, distance_to_resistance_2,
                support_intensity_score, resistance_intensity_score,
                alert_scenario, record_time
            FROM support_resistance_levels
            WHERE record_time = ?
            ORDER BY symbol
        ''', (latest_time,))
        
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        
        conn.close()
        
        return {
            'success': True,
            'count': len(data),
            'latest_time': latest_time,
            'data': data
        }
        
    except Exception as e:
        return {'success': False, 'message': str(e)}

def get_support_resistance_history(symbol, hours=24):
    """获取指定币种的历史数据"""
    try:
        conn = sqlite3.connect(SUPPORT_RESISTANCE_DB)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                symbol, current_price, 
                support_line_1, support_line_2,
                resistance_line_1, resistance_line_2,
                distance_to_support_1, distance_to_support_2,
                distance_to_resistance_1, distance_to_resistance_2,
                support_intensity_score, resistance_intensity_score,
                alert_scenario, record_time
            FROM support_resistance_levels
            WHERE symbol = ?
                AND datetime(record_time) >= datetime('now', '-' || ? || ' hours', 'localtime')
            ORDER BY record_time DESC
            LIMIT 1000
        ''', (symbol, hours))
        
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        
        conn.close()
        
        return {
            'success': True,
            'symbol': symbol,
            'count': len(data),
            'data': data
        }
        
    except Exception as e:
        return {'success': False, 'message': str(e)}

def get_database_stats():
    """获取数据库统计信息"""
    try:
        conn = sqlite3.connect(SUPPORT_RESISTANCE_DB)
        cursor = conn.cursor()
        
        # 总记录数
        cursor.execute("SELECT COUNT(*) as total FROM support_resistance_levels")
        total = cursor.fetchone()[0]
        
        # 时间范围
        cursor.execute("SELECT MIN(record_time) as min_time, MAX(record_time) as max_time FROM support_resistance_levels")
        time_range = cursor.fetchone()
        
        # 币种统计
        cursor.execute('''
            SELECT symbol, COUNT(*) as count 
            FROM support_resistance_levels 
            GROUP BY symbol 
            ORDER BY count DESC
        ''')
        symbols = cursor.fetchall()
        
        conn.close()
        
        return {
            'success': True,
            'total_records': total,
            'min_time': time_range[0],
            'max_time': time_range[1],
            'symbols': [{'symbol': s[0], 'count': s[1]} for s in symbols]
        }
        
    except Exception as e:
        return {'success': False, 'message': str(e)}

