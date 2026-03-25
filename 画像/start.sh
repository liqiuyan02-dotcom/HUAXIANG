#!/bin/bash
# 启动脚本 - 用于生产环境

echo "🚀 启动学生画像系统..."

# 检查虚拟环境
if [ -d "venv" ]; then
    echo "✓ 激活虚拟环境"
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "✓ 激活虚拟环境"
    source .venv/bin/activate
fi

# 检查环境变量
if [ -f ".env" ]; then
    echo "✓ 加载环境变量"
    export $(grep -v '^#' .env | xargs)
fi

# 检查数据库目录
if [ ! -d "data" ]; then
    echo "✓ 创建数据目录"
    mkdir -p data
fi

# 获取端口（默认5000）
PORT=${PORT:-5000}
WORKERS=${WORKERS:-4}

echo "🌐 服务配置:"
echo "  - 端口: $PORT"
echo "  - 工作进程: $WORKERS"
echo "  - 日志级别: info"
echo ""

# 启动 Gunicorn
cd backend
gunicorn -w $WORKERS \
    -b 0.0.0.0:$PORT \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --timeout 60 \
    --graceful-timeout 30 \
    --keep-alive 2 \
    app:app
