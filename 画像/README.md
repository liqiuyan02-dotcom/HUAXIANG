# Student Portrait System

[![Deploy to Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id)

🎓 **2026春季班全阶段科创编程课程体系画像系统**

基于 Flask + SQLite + 智谱 AI 的全路径学生数字化画像系统。支持从幼儿启蒙(L1)到AI创新(AICODE03)共**11个阶段**、**100+维度**的学生信息管理和智能画像生成。

## 📚 支持课程路径

### 幼儿阶段（3-6岁）
| 阶段 | 课程名称 | 适用年级 | 核心教具 |
|------|---------|---------|---------|
| 🟥 L1 | 意识世界 | 小小班 | 管道游戏套装 |
| 🟧 L2 | 发现世界 | 小班 | 百变工程螺丝刀套装 |
| 🟨 L3 | 发明世界 | 中班 | 实物编程+简单机械 |
| 🟩 L4 | 动力机械 | 中班 | 9686动力机械套装 |
| 🟢 L5 | 创造世界 | 大班 | WeDo 2.0 科学机器人 |

### 图形化阶段（6-9岁）
| 阶段 | 课程名称 | 适用年级 | 核心工具 |
|------|---------|---------|---------|
| 🔷 SPIKE | SPIKE | 一年级 | LEGO SPIKE Prime |
| 🩵 K2 | Kitten萌新大课堂 | 二年级 | Kitten图形化编程 |
| 🔵 K4 | Kitten乐学大课堂 | 三年级 | Kitten图形化进阶 |

### 代码阶段（9岁+）
| 阶段 | 课程名称 | 适用水平 | 核心内容 |
|------|---------|---------|---------|
| 🟣 A1 | AICODE01代码英雄 | 入门 | C++基础 |
| 🟪 A2 | AICODE02代码岛英雄 | 进阶 | C++进阶 |
| 💜 A3 | AICODE03AI编程创新 | 高阶 | AIGC开发 |

> 详细课程体系说明请查看 [docs/curriculum.md](docs/curriculum.md)

## 功能特点

- 📊 **学生信息管理** - 批量导入、智能识别课程路径
- 📝 **多路径问卷** - 65+ 维度观测（幼儿/图形化/C++/AI）
- 🤖 **AI 智能画像** - 基于 GLM-4 自动生成专业报告
- 📚 **档案库管理** - 历史追溯、Markdown 导出

## 快速开始

### 方式 1: 一键部署到 Railway（推荐）

点击上方按钮，按照指引完成部署。

### 方式 2: 本地运行

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/student-portrait.git
cd student-portrait

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 API Key
cp .env.example .env
# 编辑 .env，填入 ZHIPU_API_KEY

# 4. 启动服务
cd backend
python app.py

# 5. 访问 http://localhost:5000
```

## 项目结构

```
student-portrait/
├── backend/              # Flask 后端
│   ├── app.py           # 主应用
│   ├── models.py        # 数据模型
│   ├── database.py      # 数据库操作
│   └── analysis.py      # 数据分析
├── frontend/             # 前端页面
│   ├── templates/
│   └── static/
├── docs/                 # 文档
│   └── deploy.md        # 详细部署指南
├── requirements.txt      # Python 依赖
├── Dockerfile            # Docker 配置
├── railway.json          # Railway 配置
├── Procfile              # Heroku 配置
└── README.md
```

## 详细部署文档

查看 [docs/deploy.md](docs/deploy.md) 了解更多部署选项：
- Railway（免费）
- Heroku
- Vercel
- Docker
- PythonAnywhere
- 云服务器

## 使用说明

### 1. 导入学生名单

格式：`姓名,性别,班级,上课时间`

示例：
```
李华,男,AICODE-03,周六上午
王芳,女,启蒙-01,周日下午
```

系统会自动识别课程路径：
- `AICODE-03` → AI 创新
- `AICODE` → C++ 编程
- `Kitten` → 图形化编程
- `启蒙` → 幼儿启蒙

### 2. 填写问卷

点击进入问卷页面，系统会根据学生路径加载对应的问卷模块。

### 3. 生成画像

点击「生成画像」，系统调用智谱 AI 分析数据并生成 Markdown 报告。

### 4. 管理档案

生成的报告自动存入档案库，支持导出和查看历史。

## 环境变量

| 变量 | 必需 | 说明 |
|------|------|------|
| `ZHIPU_API_KEY` | ✅ | 智谱 AI API Key |
| `SECRET_KEY` | ✅ | Flask 密钥 |
| `PORT` | ❌ | 服务端口（默认5000） |

获取智谱 AI API Key: https://open.bigmodel.cn/

## 技术栈

- **后端**: Python 3.8+, Flask, SQLite
- **前端**: HTML5, CSS3, JavaScript
- **AI**: 智谱 GLM-4-Flash
- **部署**: Docker, Gunicorn

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
