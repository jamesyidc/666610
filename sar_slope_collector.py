#!/usr/bin/env python3
"""
SAR斜率系统 - 数据采集与计算守护进程
监测27个加密货币的5分钟SAR数据点，标注多空及持续时间，保留近7天数据
"""
import sqlite3
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import traceback
import pytz

# 27个指定币种
MONITORED_SYMBOLS = [
    'BTC-USDT-SWAP', 'ETH-USDT-SWAP', 'XRP-USDT-SWAP', 'BNB-USDT-SWAP',
    'SOL-USDT-SWAP', 'LTC-USDT-SWAP', 'DOGE-USDT-SWAP', 'SUI-USDT-SWAP',
    'TRX-USDT-SWAP', 'TON-USDT-SWAP', 'ETC-USDT-SWAP', 'BCH-USDT-SWAP',
    'HBAR-USDT-SWAP', 'XLM-USDT-SWAP', 'FIL-USDT-SWAP', 'LINK-USDT-SWAP',
    'CRO-USDT-SWAP', 'DOT-USDT-SWAP', 'AAVE-USDT-SWAP', 'UNI-USDT-SWAP',
    'NEAR-USDT-SWAP', 'APT-USDT-SWAP', 'CFX-USDT-SWAP', 'CRV-USDT-SWAP',
    'STX-USDT-SWAP', 'LDO-USDT-SWAP', 'TAO-USDT-SWAP'
]

BEIJING_TZ = pytz.timezone('Asia/Shanghai')
DB_PATH = '/home/user/webapp/databases/crypto_data.db'
TIMEFRAME = '5m'

def init_database():
    """初始化SAR斜率数据库表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建SAR斜率主表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sar_slope_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            timestamp INTEGER NOT NULL,
            datetime_utc TEXT NOT NULL,
            datetime_beijing TEXT NOT NULL,
            sar_value REAL NOT NULL,
            sar_position TEXT NOT NULL,
            sar_quadrant INTEGER,
            position_duration INTEGER DEFAULT 1,
            slope_value REAL,
            slope_direction TEXT,
            price_close REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(symbol, timestamp)
        )
    """)
    
    # 创建索引以提升查询性能
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sar_slope_symbol_timestamp 
        ON sar_slope_data(symbol, timestamp DESC)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sar_slope_position 
        ON sar_slope_data(symbol, sar_position, timestamp DESC)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sar_slope_datetime 
        ON sar_slope_data(datetime_beijing)
    """)
    
    # 创建SAR位置统计表（用于快速查询当前状态）
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sar_position_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL UNIQUE,
            current_position TEXT NOT NULL,
            current_quadrant INTEGER,
            position_start_time INTEGER NOT NULL,
            position_duration INTEGER DEFAULT 1,
            last_sar_value REAL,
            last_price REAL,
            last_update INTEGER NOT NULL,
            last_update_beijing TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')}")

def get_latest_sar_data(symbol: str) -> Dict:
    """从okex_technical_indicators表获取最新SAR数据"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            symbol, timeframe, strftime('%s', record_time) as timestamp, 
            sar, sar_position, sar_quadrant, current_price
        FROM okex_technical_indicators
        WHERE symbol = ? AND timeframe = ? AND sar IS NOT NULL
        ORDER BY record_time DESC
        LIMIT 1
    """, (symbol, TIMEFRAME))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row or row[3] is None:
        return None
    
    return {
        'symbol': row[0],
        'timeframe': row[1],
        'timestamp': int(row[2]),
        'sar': row[3],
        'sar_position': row[4],
        'sar_quadrant': row[5],
        'current_price': row[6]
    }

def get_price_data(symbol: str, timestamp: int) -> tuple:
    """获取对应时间的价格（从okex_technical_indicators）"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT current_price, current_price FROM okex_technical_indicators
        WHERE symbol = ? AND timeframe = ? AND strftime('%s', record_time) = ?
        LIMIT 1
    """, (symbol, TIMEFRAME, str(timestamp)))
    
    row = cursor.fetchone()
    conn.close()
    
    return (row[0], row[0]) if row else (None, None)

def calculate_slope(symbol: str, current_sar: float, timestamp: int) -> Tuple[float, str]:
    """计算SAR斜率"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 获取前一个SAR值（5分钟前）
    previous_timestamp = timestamp - 300000  # 5分钟 = 300秒 = 300000毫秒
    
    cursor.execute("""
        SELECT sar_value FROM sar_slope_data
        WHERE symbol = ? AND timestamp = ?
        LIMIT 1
    """, (symbol, previous_timestamp))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None, 'stable'
    
    previous_sar = row[0]
    
    # 计算斜率 (变化量)
    slope = current_sar - previous_sar
    slope_percent = (slope / previous_sar * 100) if previous_sar != 0 else 0
    
    # 判断斜率方向
    if slope_percent > 0.1:
        direction = 'up'
    elif slope_percent < -0.1:
        direction = 'down'
    else:
        direction = 'stable'
    
    return slope_percent, direction

def get_position_duration(symbol: str, current_position: str, timestamp: int) -> int:
    """计算当前多空位置持续时间（周期数）"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 查询当前位置的统计信息
    cursor.execute("""
        SELECT position_duration, current_position 
        FROM sar_position_stats
        WHERE symbol = ?
    """, (symbol,))
    
    row = cursor.fetchone()
    
    if not row:
        # 新币种，初始化持续时间为1
        return 1
    
    last_duration, last_position = row
    
    if last_position == current_position:
        # 位置未变，持续时间+1
        return last_duration + 1
    else:
        # 位置改变，重新开始计数
        return 1

def update_position_stats(symbol: str, sar_data: Dict, price_close: float, duration: int):
    """更新SAR位置统计表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = sar_data['timestamp']
    dt_utc = datetime.utcfromtimestamp(timestamp / 1000)
    dt_beijing = dt_utc.replace(tzinfo=pytz.UTC).astimezone(BEIJING_TZ)
    datetime_beijing = dt_beijing.strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute("""
        INSERT INTO sar_position_stats 
        (symbol, current_position, current_quadrant, position_start_time, 
         position_duration, last_sar_value, last_price, last_update, last_update_beijing)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(symbol) DO UPDATE SET
            current_position = excluded.current_position,
            current_quadrant = excluded.current_quadrant,
            position_start_time = CASE 
                WHEN current_position != excluded.current_position 
                THEN excluded.position_start_time 
                ELSE position_start_time 
            END,
            position_duration = excluded.position_duration,
            last_sar_value = excluded.last_sar_value,
            last_price = excluded.last_price,
            last_update = excluded.last_update,
            last_update_beijing = excluded.last_update_beijing,
            updated_at = CURRENT_TIMESTAMP
    """, (
        symbol,
        sar_data['sar_position'],
        sar_data['sar_quadrant'],
        timestamp,
        duration,
        sar_data['sar'],
        price_close,
        timestamp,
        datetime_beijing
    ))
    
    conn.commit()
    conn.close()

def insert_sar_slope_data(symbol: str, sar_data: Dict, price_open: float, price_close: float, duration: int, slope: float, slope_direction: str):
    """插入SAR斜率数据"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = sar_data['timestamp']
    dt_utc = datetime.utcfromtimestamp(timestamp / 1000)
    dt_beijing = dt_utc.replace(tzinfo=pytz.UTC).astimezone(BEIJING_TZ)
    
    datetime_utc = dt_utc.strftime('%Y-%m-%d %H:%M:%S')
    datetime_beijing = dt_beijing.strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute("""
        INSERT OR REPLACE INTO sar_slope_data
        (symbol, timestamp, datetime_utc, datetime_beijing, sar_value, sar_position, 
         sar_quadrant, position_duration, slope_value, slope_direction, price_open, price_close)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        symbol,
        timestamp,
        datetime_utc,
        datetime_beijing,
        sar_data['sar'],
        sar_data['sar_position'],
        sar_data['sar_quadrant'],
        duration,
        slope,
        slope_direction,
        price_open,
        price_close
    ))
    
    # 同步到 sar_slope_v2 表（用于API展示）
    cursor.execute("""
        INSERT OR REPLACE INTO sar_slope_v2
        (symbol, timestamp, datetime_utc, datetime_beijing, sar_value, sar_direction, price_open, price_close)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        symbol,
        timestamp,
        datetime_utc,
        datetime_beijing,
        sar_data['sar'],
        sar_data['sar_position'],  # sar_position 映射到 sar_direction
        price_open,
        price_close
    ))
    
    conn.commit()
    conn.close()

def cleanup_old_data():
    """清理2天前的旧数据（保留48小时 = 576根K线）"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 计算2天前的时间戳（48小时）
    two_days_ago = int((datetime.now() - timedelta(days=2)).timestamp() * 1000)
    
    cursor.execute("""
        DELETE FROM sar_slope_data
        WHERE timestamp < ?
    """, (two_days_ago,))
    
    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()
    
    if deleted_count > 0:
        print(f"🧹 Cleaned up {deleted_count} old records (>48 hours)")
    
    return deleted_count

def process_symbol(symbol: str) -> bool:
    """处理单个币种的SAR数据"""
    try:
        # 获取最新SAR数据
        sar_data = get_latest_sar_data(symbol)
        if not sar_data:
            print(f"⚠️  {symbol}: No SAR data available")
            return False
        
        # 获取价格数据（开盘价和收盘价）
        price_open, price_close = get_price_data(symbol, sar_data['timestamp'])
        if not price_close:
            print(f"⚠️  {symbol}: No price data available")
            return False
        
        # 计算持续时间
        duration = get_position_duration(symbol, sar_data['sar_position'], sar_data['timestamp'])
        
        # 计算斜率
        slope, slope_direction = calculate_slope(symbol, sar_data['sar'], sar_data['timestamp'])
        
        # 插入数据
        insert_sar_slope_data(symbol, sar_data, price_open, price_close, duration, slope, slope_direction)
        
        # 更新统计表
        update_position_stats(symbol, sar_data, price_close, duration)
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing {symbol}: {e}")
        traceback.print_exc()
        return False

def collect_all_symbols():
    """采集所有币种的SAR斜率数据"""
    print(f"\n{'='*60}")
    print(f"🔄 Starting SAR Slope Collection - {datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    success_count = 0
    fail_count = 0
    
    for symbol in MONITORED_SYMBOLS:
        if process_symbol(symbol):
            success_count += 1
            short_name = symbol.replace('-USDT-SWAP', '')
            print(f"✅ {short_name}: Data collected")
        else:
            fail_count += 1
    
    print(f"\n📊 Collection Summary:")
    print(f"   ✅ Success: {success_count}/{len(MONITORED_SYMBOLS)}")
    print(f"   ❌ Failed: {fail_count}/{len(MONITORED_SYMBOLS)}")
    print(f"{'='*60}\n")

def main():
    """主循环"""
    print("🚀 SAR Slope Collector Daemon Starting...")
    print(f"📍 Database: {DB_PATH}")
    print(f"📊 Monitoring: {len(MONITORED_SYMBOLS)} symbols")
    print(f"⏱️  Timeframe: {TIMEFRAME}")
    print(f"💾 Data retention: 48 hours (576 K-lines per coin)")
    
    # 初始化数据库
    init_database()
    
    # 执行一次初始采集
    collect_all_symbols()
    
    # 每5分钟采集一次数据
    collection_interval = 300  # 5分钟 = 300秒
    cleanup_counter = 0
    
    while True:
        try:
            time.sleep(collection_interval)
            
            # 采集数据
            collect_all_symbols()
            
            # 每12次采集（1小时）执行一次清理
            cleanup_counter += 1
            if cleanup_counter >= 12:
                cleanup_old_data()
                cleanup_counter = 0
            
        except KeyboardInterrupt:
            print("\n⏹️  SAR Slope Collector stopped by user")
            break
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            traceback.print_exc()
            time.sleep(60)  # 出错后等待1分钟再继续

if __name__ == '__main__':
    main()
