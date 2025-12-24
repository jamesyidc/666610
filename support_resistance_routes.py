"""
支撑压力线系统路由 - 使用独立的support_resistance.db数据库
"""
from flask import Blueprint, jsonify, request, render_template, make_response
import sqlite3
import json
from datetime import datetime
from db_config import SUPPORT_RESISTANCE_DB

sr_bp = Blueprint('support_resistance', __name__)

@sr_bp.route('/api/support-resistance/latest')
def api_support_resistance_latest():
    """获取最新的支撑压力线数据 - 每个币种的最新记录"""
    try:
        conn = sqlite3.connect(SUPPORT_RESISTANCE_DB)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 获取每个币种的最新记录（使用子查询）
        cursor.execute('''
            SELECT 
                symbol, current_price, 
                support_line_1, support_line_2,
                resistance_line_1, resistance_line_2,
                distance_to_support_1, distance_to_support_2,
                distance_to_resistance_1, distance_to_resistance_2,
                support_intensity_score, resistance_intensity_score,
                alert_scenario, record_time,
                position_s2_r1, position_s1_r2, position_s1_r2_upper, position_s1_r1,
                position_7d, position_48h,
                alert_7d_low, alert_7d_high, alert_48h_low, alert_48h_high,
                alert_scenario_1, alert_scenario_2, alert_scenario_3, alert_scenario_4,
                alert_triggered, baseline_price_24h, change_percent_24h,
                high_7d, low_7d, high_48h, low_48h
            FROM support_resistance_levels srl
            WHERE srl.record_time = (
                SELECT MAX(record_time) 
                FROM support_resistance_levels 
                WHERE symbol = srl.symbol
            )
            ORDER BY symbol
        ''')
        
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        
        if not data:
            conn.close()
            return jsonify({
                'success': False,
                'message': 'No data available'
            })
        
        # 获取最新更新时间
        latest_time = max(row['record_time'] for row in data)
        
        # 按场景分组
        scenario_1 = []  # 接近支撑线
        scenario_2 = []  # 接近压力线
        scenario_3 = []  # 突破压力线
        scenario_4 = []  # 跌破支撑线
        
        for item in data:
            scenario = item.get('alert_scenario') or ''
            if '接近支撑' in scenario or '靠近支撑' in scenario:
                scenario_1.append(item['symbol'])
            elif '接近压力' in scenario or '靠近压力' in scenario:
                scenario_2.append(item['symbol'])
            elif '突破压力' in scenario:
                scenario_3.append(item['symbol'])
            elif '跌破支撑' in scenario:
                scenario_4.append(item['symbol'])
        
        conn.close()
        
        return jsonify({
            'success': True,
            'latest_time': latest_time,
            'total_coins': len(data),
            'scenario_1_count': len(scenario_1),
            'scenario_2_count': len(scenario_2),
            'scenario_3_count': len(scenario_3),
            'scenario_4_count': len(scenario_4),
            'scenario_1_coins': scenario_1,
            'scenario_2_coins': scenario_2,
            'scenario_3_coins': scenario_3,
            'scenario_4_coins': scenario_4,
            'data': data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

@sr_bp.route('/api/support-resistance/history/<symbol>')
def api_support_resistance_history(symbol):
    """获取指定币种的历史数据"""
    try:
        hours = request.args.get('hours', 24, type=int)
        
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
                alert_scenario, record_time,
                position_s2_r1, position_s1_r2, position_s1_r2_upper, position_s1_r1,
                position_7d, position_48h,
                alert_7d_low, alert_7d_high, alert_48h_low, alert_48h_high,
                alert_scenario_1, alert_scenario_2, alert_scenario_3, alert_scenario_4,
                alert_triggered, baseline_price_24h, change_percent_24h,
                high_7d, low_7d, high_48h, low_48h
            FROM support_resistance_levels
            WHERE symbol = ?
                AND datetime(record_time) >= datetime('now', '-' || ? || ' hours', 'localtime')
            ORDER BY record_time DESC
            LIMIT 1000
        ''', (symbol, hours))
        
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'count': len(data),
            'data': data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

@sr_bp.route('/api/support-resistance/snapshots')
def api_support_resistance_snapshots():
    """获取快照历史数据"""
    try:
        get_all = request.args.get('all', 'false').lower() == 'true'
        
        conn = sqlite3.connect(SUPPORT_RESISTANCE_DB)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if get_all:
            cursor.execute('''
                SELECT *
                FROM support_resistance_snapshots
                ORDER BY snapshot_time ASC
            ''')
        else:
            limit = request.args.get('limit', 100, type=int)
            cursor.execute('''
                SELECT *
                FROM support_resistance_snapshots
                ORDER BY snapshot_time DESC
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'count': len(data),
            'data': data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

@sr_bp.route('/api/support-resistance/stats')
def api_support_resistance_stats():
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
        
        return jsonify({
            'success': True,
            'total_records': total,
            'min_time': time_range[0],
            'max_time': time_range[1],
            'symbols': [{'symbol': s[0], 'count': s[1]} for s in symbols]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

