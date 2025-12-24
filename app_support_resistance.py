#!/usr/bin/env python3
"""
支撑压力线系统独立Flask应用
使用独立的support_resistance.db数据库
"""
from flask import Flask, render_template
from flask_cors import CORS
from support_resistance_routes import sr_bp

app = Flask(__name__)
CORS(app)

# 注册支撑压力线路由蓝图
app.register_blueprint(sr_bp)

# 保留原有的页面路由
@app.route('/support-resistance')
def support_resistance_page():
    return render_template('support_resistance.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

