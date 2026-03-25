# 学生画像系统 - 部署指南

## 快速部署选项

### 选项 1: 部署到 Railway（推荐，免费）

Railway 提供免费的服务器托管，支持自动部署。

#### 步骤:

1. **Fork 本项目到 GitHub**

2. **登录 Railway** (https://railway.app)
   - 使用 GitHub 账号登录

3. **创建新项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你 fork 的仓库

4. **配置环境变量**
   - 进入项目设置
   - 添加变量 `ZHIPU_API_KEY`（你的智谱AI API Key）
   - 添加变量 `SECRET_KEY`（随机字符串）

5. **部署**
   - Railway 会自动检测到 `requirements.txt` 和 `Procfile`
   - 点击 "Deploy" 开始部署
   - 等待几分钟，获得公开访问链接

6. **访问**
   - Railway 会提供一个 `xxx.up.railway.app` 的域名
   - 直接点击即可访问

---

### 选项 2: 部署到 Heroku

#### 步骤:

1. **注册 Heroku 账号** (https://heroku.com)

2. **安装 Heroku CLI**

3. **登录并创建应用**:
```bash
heroku login
heroku create your-app-name
```

4. **配置环境变量**:
```bash
heroku config:set ZHIPU_API_KEY=your-api-key
heroku config:set SECRET_KEY=your-secret-key
```

5. **部署**:
```bash
git push heroku main
```

---

### 选项 3: 部署到 Vercel（使用 Serverless）

Vercel 也支持 Python Flask 应用。

1. **安装 Vercel CLI**:
```bash
npm i -g vercel
```

2. **登录**:
```bash
vercel login
```

3. **部署**:
```bash
vercel --prod
```

---

### 选项 4: 使用 Docker 部署到云服务器

如果你有阿里云/腾讯云/阿里云等服务器。

#### 步骤:

1. **安装 Docker**:
```bash
curl -fsSL https://get.docker.com | sh
```

2. **克隆项目**:
```bash
git clone https://github.com/yourusername/student-portrait.git
cd student-portrait
```

3. **配置环境变量**:
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key
```

4. **构建并运行**:
```bash
docker-compose up -d
```

5. **访问**:
```
http://your-server-ip:5000
```

---

### 选项 5: 部署到 PythonAnywhere（免费，适合小项目）

PythonAnywhere 提供免费的 Python 托管。

1. **注册账号** (https://www.pythonanywhere.com)

2. **上传代码**:
   - 使用 Web 界面上传压缩包，或
   - 使用 Git: `git clone your-repo-url`

3. **创建虚拟环境**:
```bash
mkvirtualenv --python=/usr/bin/python3.9 myenv
pip install -r requirements.txt
```

4. **配置 Web 应用**:
   - 进入 "Web" 标签
   - 点击 "Add a new web app"
   - 选择 "Manual configuration" → "Python 3.9"
   - 配置 WSGI 文件指向 `wsgi.py`

5. **设置环境变量**:
   - 在 WSGI 配置文件中添加:
```python
os.environ['ZHIPU_API_KEY'] = 'your-api-key'
```

6. **重启应用**

---

## 配置说明

### 必需的环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `ZHIPU_API_KEY` | 智谱AI API Key | `your-api-key-here` |
| `SECRET_KEY` | Flask 密钥（随机字符串） | `random-string-123` |

### 可选的环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `PORT` | 服务端口 | `5000` |
| `DATABASE_PATH` | 数据库路径 | `./data/student_portrait.db` |
| `FLASK_ENV` | 运行环境 | `production` |
| `WORKERS` | Gunicorn 工作进程数 | `4` |

---

## 自定义域名

部署到 Railway/Heroku 等平台后，你可以：

1. **绑定自定义域名**:
   - 在平台设置中添加自定义域名
   - 在 DNS 解析中添加 CNAME 记录

2. **配置 HTTPS**:
   - 大多数平台自动提供 HTTPS
   - 或使用 Cloudflare 代理

---

## 数据备份

### 自动备份（推荐）

使用 Railway/Heroku 的数据库插件，或使用以下脚本定期备份：

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
cp data/student_portrait.db backups/backup_$DATE.db
```

添加到 crontab:
```bash
0 2 * * * /path/to/backup.sh  # 每天凌晨2点备份
```

### 手动导出

在系统界面中点击「备份全库」按钮即可下载 JSON 格式的备份文件。

---

## 故障排查

### 服务无法启动

1. 检查端口是否被占用
2. 检查环境变量是否正确设置
3. 查看日志: `docker logs container-name`

### AI 报告生成失败

1. 确认 `ZHIPU_API_KEY` 已正确设置
2. 检查 API Key 是否有额度
3. 查看后端日志

### 数据丢失

1. 检查数据库文件是否存在
2. 检查数据库目录权限
3. 从备份恢复

---

## 性能优化

### 高并发场景

1. 增加 Gunicorn 工作进程:
```bash
export WORKERS=8
```

2. 使用 Redis 缓存（可选）

3. 使用 CDN 加速静态资源

---

## 安全建议

1. **修改默认密钥**: 务必设置 `SECRET_KEY`
2. **API Key 保护**: 不要将 API Key 提交到 Git
3. **HTTPS**: 生产环境务必使用 HTTPS
4. **数据备份**: 定期备份数据
5. **访问控制**: 如需限制访问，可添加简单的 Basic Auth

---

## 获取帮助

如有问题，请：
1. 查看项目 Issues
2. 提交新的 Issue
3. 联系项目维护者
