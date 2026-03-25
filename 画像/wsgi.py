"""
WSGI 入口文件
用于 Gunicorn 等 WSGI 服务器启动
"""
import os
import sys

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'backend'))

from backend.app import app

if __name__ == "__main__":
    app.run()
