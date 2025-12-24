"""
数据库配置
"""
import os

# 数据库路径配置
DB_DIR = os.path.join(os.path.dirname(__file__), 'databases')

# 主数据库
CRYPTO_DATA_DB = os.path.join(DB_DIR, 'crypto_data.db')

# 支撑压力线专用数据库
SUPPORT_RESISTANCE_DB = os.path.join(DB_DIR, 'support_resistance.db')

# 其他数据库
FUND_MONITOR_DB = os.path.join(DB_DIR, 'fund_monitor.db')
V1V2_DATA_DB = os.path.join(DB_DIR, 'v1v2_data.db')
PRICE_SPEED_DATA_DB = os.path.join(DB_DIR, 'price_speed_data.db')
SIGNAL_DATA_DB = os.path.join(DB_DIR, 'signal_data.db')

# 为向后兼容保留的别名
CRYPTO_DB_PATH = CRYPTO_DATA_DB
