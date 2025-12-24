module.exports = {
  apps: [
    // 【0】 同步指标守护进程
    {
      name: 'sync-indicators-daemon',
      script: 'sync_indicators_daemon.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: true,
      watch: false,
      max_memory_restart: '300M',
      error_file: 'logs/sync-indicators-error.log',
      out_file: 'logs/sync-indicators-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【2】 WebSocket 实时数据采集器
    {
      name: 'websocket-collector',
      script: 'okex_websocket_realtime_collector.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      error_file: 'logs/websocket-collector-error.log',
      out_file: 'logs/websocket-collector-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【3】 Google Drive 监控
    {
      name: 'gdrive-monitor',
      script: 'gdrive_monitor.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      error_file: 'logs/gdrive-monitor-error.log',
      out_file: 'logs/gdrive-monitor-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【4】 V1V2 大额成交采集器
    {
      name: 'v1v2-collector',
      script: 'v1v2_collector.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      error_file: 'logs/v1v2-collector-error.log',
      out_file: 'logs/v1v2-collector-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【5】 支撑压力线采集器
    {
      name: 'support-resistance-collector',
      script: 'support_resistance_collector.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      error_file: 'logs/support-resistance-collector-error.log',
      out_file: 'logs/support-resistance-collector-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【6】 支撑压力快照采集器
    {
      name: 'support-resistance-snapshot-collector',
      script: 'support_resistance_snapshot_collector.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      error_file: 'logs/support-resistance-snapshot-collector-error.log',
      out_file: 'logs/support-resistance-snapshot-collector-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【7】 位置系统采集器
    {
      name: 'position-system-collector',
      script: 'position_system_collector.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      error_file: 'logs/position-system-collector-error.log',
      out_file: 'logs/position-system-collector-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【8】 加密指数采集器
    {
      name: 'crypto-index-collector',
      script: 'crypto_index_collector.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      error_file: 'logs/crypto-index-collector-error.log',
      out_file: 'logs/crypto-index-collector-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【9】 采集器监控
    {
      name: 'collector-monitor',
      script: 'collector_monitor.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      error_file: 'logs/collector-monitor-error.log',
      out_file: 'logs/collector-monitor-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【10】 Google Drive 自动触发
    {
      name: 'gdrive-auto-trigger',
      script: 'gdrive_auto_trigger.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      error_file: 'logs/gdrive-auto-trigger-error.log',
      out_file: 'logs/gdrive-auto-trigger-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【11】 恐慌清洗指数采集器
    {
      name: 'panic-wash-collector',
      script: 'panic_wash_collector.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      error_file: 'logs/panic-wash-collector-error.log',
      out_file: 'logs/panic-wash-collector-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【12】 比价系统采集器
    {
      name: 'price-comparison-collector',
      script: 'price_comparison_collector.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      error_file: 'logs/price-comparison-collector-error.log',
      out_file: 'logs/price-comparison-collector-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【13】 Telegram 通知器
    {
      name: 'telegram-notifier',
      script: 'telegram_notifier.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      error_file: 'logs/telegram-notifier-error.log',
      out_file: 'logs/telegram-notifier-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【14】 磁盘监控 (可选)
    {
      name: 'disk-monitor',
      script: 'disk_monitor.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: false,
      watch: false,
      max_memory_restart: '100M',
      error_file: 'logs/disk-monitor-error.log',
      out_file: 'logs/disk-monitor-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【15】 数据库维护 (定时任务)
    {
      name: 'db-maintenance',
      script: 'db_maintenance.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: false,
      cron_restart: '0 3 * * *',  // 每天凌晨3点执行
      watch: false,
      error_file: 'logs/db-maintenance-error.log',
      out_file: 'logs/db-maintenance-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【16】 日志清理 (定时任务) - 文件不存在，暂时禁用
    // {
    //   name: 'log-cleanup',
    //   script: 'auto_cleanup_old_files.py',
    //   interpreter: 'python3',
    //   cwd: '/home/user/webapp',
    //   autorestart: false,
    //   cron_restart: '0 2 * * *',  // 每天凌晨2点执行
    //   watch: false,
    //   error_file: 'logs/log-cleanup-error.log',
    //   out_file: 'logs/log-cleanup-out.log',
    //   log_date_format: 'YYYY-MM-DD HH:mm:ss',
    //   merge_logs: true
    // },

    // 【17】 自动更新文件夹配置
    {
      name: 'auto-folder-update',
      script: 'auto_update_folder_config.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: false,
      cron_restart: '*/10 * * * *',  // 每10分钟执行一次
      watch: false,
      error_file: 'logs/auto-folder-update-error.log',
      out_file: 'logs/auto-folder-update-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【18】 资金监控采集器
    {
      name: 'fund-monitor-collector',
      script: 'fund_monitor_collector.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      error_file: 'logs/fund-monitor-collector-error.log',
      out_file: 'logs/fund-monitor-collector-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【20】 Flask Web 应用 - 主服务
    {
      name: 'flask-app',
      script: 'app_new.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: true,
      watch: false,
      max_memory_restart: '1000M',
      instances: 1,
      exec_mode: 'fork',
      env: {
        FLASK_APP: 'app_new.py',
        FLASK_ENV: 'production',
        PYTHONUNBUFFERED: '1'
      },
      error_file: 'logs/flask-app-error.log',
      out_file: 'logs/flask-app-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【21】 SAR斜率采集器
    {
      name: 'sar-slope-collector',
      script: 'sar_slope_collector.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      error_file: 'logs/sar-slope-collector-error.log',
      out_file: 'logs/sar-slope-collector-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },

    // 【22】 Google Drive TXT文件检测器
    {
      name: 'gdrive-detector',
      script: 'gdrive_final_detector.py',
      interpreter: 'python3',
      cwd: '/home/user/webapp',
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      error_file: 'logs/gdrive-detector-error.log',
      out_file: 'logs/gdrive-detector-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    }
  ]
};
