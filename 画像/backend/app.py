"""
Flask 主应用 - 学生画像系统
支持生产环境部署的配置
"""

import os
import json
import requests
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 导入模型和数据库
from models import StudentBasic, StudentPortraitDoc, SURVEY_CONFIG, PATH_CONFIG, detect_path
from database import db

# 创建 Flask 应用
def create_app():
    app = Flask(__name__,
        template_folder='../frontend/templates',
        static_folder='../frontend/static'
    )

    # 配置密钥（从环境变量读取）
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # 配置 CORS
    CORS(app)

    # 配置数据库路径（生产环境使用持久化目录）
    db_path = os.environ.get('DATABASE_PATH', '../data/student_portrait.db')
    if not os.path.isabs(db_path):
        # 如果是相对路径，转换为绝对路径
        db_path = os.path.join(os.path.dirname(__file__), db_path)

    # 重新初始化数据库连接
    from database import Database
    global db
    db = Database(db_path)

    return app

app = create_app()

# ========== 页面路由 ==========

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/survey/<int:student_id>')
def survey_page(student_id):
    """问卷页面"""
    return render_template('survey.html', student_id=student_id)

# ========== 健康检查 ==========

@app.route('/health')
def health():
    """健康检查接口（用于部署平台检测）"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

# ========== 学生管理 API ==========

@app.route('/api/students', methods=['GET', 'POST'])
def students():
    """学生列表 / 创建学生"""
    if request.method == 'POST':
        data = request.json
        student = StudentBasic(
            name=data.get('name', ''),
            gender=data.get('gender', ''),
            class_name=data.get('class_name', ''),
            class_time=data.get('class_time', ''),
            path=detect_path(data.get('class_name', ''))
        )
        student_id = db.create_student(student)
        logger.info(f"Created student: {student.name} (ID: {student_id})")
        return jsonify({"success": True, "id": student_id, "message": "学生创建成功"})

    # GET 请求
    class_name = request.args.get('class_name')
    path = request.args.get('path')
    students = db.get_all_students(class_name=class_name, path=path)

    # 获取每个学生的问卷状态
    result = []
    for s in students:
        survey = db.get_survey_by_student(s.id)
        portrait = db.get_latest_portrait_doc(s.id)
        result.append({
            "id": s.id,
            "name": s.name,
            "gender": s.gender,
            "class_name": s.class_name,
            "class_time": s.class_time,
            "path": s.path,
            "path_name": PATH_CONFIG.get(s.path, {}).get('name', s.path),
            "has_survey": survey is not None and survey.is_completed,
            "has_portrait": portrait is not None,
            "created_at": s.created_at
        })

    return jsonify({"success": True, "data": result})

@app.route('/api/students/<int:student_id>', methods=['GET', 'PUT', 'DELETE'])
def student_detail(student_id):
    """学生详情 / 更新 / 删除"""
    if request.method == 'GET':
        student = db.get_student_by_id(student_id)
        if not student:
            return jsonify({"success": False, "message": "学生不存在"}), 404

        survey = db.get_survey_by_student(student_id)
        portrait = db.get_latest_portrait_doc(student_id)

        return jsonify({
            "success": True,
            "data": {
                "id": student.id,
                "name": student.name,
                "gender": student.gender,
                "class_name": student.class_name,
                "class_time": student.class_time,
                "path": student.path,
                "path_name": PATH_CONFIG.get(student.path, {}).get('name', student.path),
                "survey": json.loads(survey.progress) if survey and survey.progress else {},
                "portrait_content": portrait.content if portrait else ""
            }
        })

    elif request.method == 'PUT':
        data = request.json
        student = db.get_student_by_id(student_id)
        if not student:
            return jsonify({"success": False, "message": "学生不存在"}), 404

        student.name = data.get('name', student.name)
        student.gender = data.get('gender', student.gender)
        student.class_name = data.get('class_name', student.class_name)
        student.class_time = data.get('class_time', student.class_time)

        db.update_student(student)
        logger.info(f"Updated student: {student.name} (ID: {student_id})")
        return jsonify({"success": True, "message": "更新成功"})

    elif request.method == 'DELETE':
        db.delete_student(student_id)
        logger.info(f"Deleted student ID: {student_id}")
        return jsonify({"success": True, "message": "删除成功"})

@app.route('/api/students/search', methods=['GET'])
def search_students():
    """搜索学生"""
    keyword = request.args.get('q', '')
    students = db.search_students(keyword)
    result = [{
        "id": s.id,
        "name": s.name,
        "class_name": s.class_name,
        "path": s.path
    } for s in students]
    return jsonify({"success": True, "data": result})

@app.route('/api/students/batch', methods=['POST'])
def batch_import_students():
    """批量导入学生"""
    data = request.json
    lines = data.get('data', '').strip().split('\n')

    students = []
    for line in lines:
        parts = [p.strip() for p in line.split(',')]
        if len(parts) >= 3:
            students.append({
                'name': parts[0],
                'sex': parts[1],
                'class': parts[2],
                'time': ' '.join(parts[3:]) if len(parts) > 3 else ''
            })

    count = db.batch_import_students(students)
    logger.info(f"Batch imported {count} students")
    return jsonify({"success": True, "count": count, "message": f"成功导入 {count} 名学生"})

# ========== 问卷 API ==========

@app.route('/api/survey/config', methods=['GET'])
def get_survey_config():
    """获取问卷配置"""
    path = request.args.get('path', 'kitten')

    # 组合通用配置和路径特定配置
    config = {
        "common": SURVEY_CONFIG.get('common', []),
        "path_specific": SURVEY_CONFIG.get(path, [])
    }

    return jsonify({"success": True, "data": config})

@app.route('/api/survey/<int:student_id>', methods=['GET', 'POST'])
def survey(student_id):
    """获取/保存问卷进度"""
    student = db.get_student_by_id(student_id)
    if not student:
        return jsonify({"success": False, "message": "学生不存在"}), 404

    if request.method == 'GET':
        survey_data = db.get_survey_by_student(student_id)
        if survey_data:
            try:
                progress = json.loads(survey_data.progress) if survey_data.progress else {}
            except:
                progress = {}

            return jsonify({
                "success": True,
                "data": {
                    "student_id": student_id,
                    "path": survey_data.path or student.path,
                    "progress": progress,
                    "remark": survey_data.remark or "",
                    "is_completed": survey_data.is_completed
                }
            })
        else:
            return jsonify({
                "success": True,
                "data": {
                    "student_id": student_id,
                    "path": student.path,
                    "progress": {},
                    "remark": "",
                    "is_completed": False
                }
            })

    elif request.method == 'POST':
        data = request.json
        progress = data.get('progress', {})
        remark = data.get('remark', '')

        db.update_survey_progress(student_id, progress, remark)
        return jsonify({"success": True, "message": "保存成功"})

@app.route('/api/survey/<int:student_id>/complete', methods=['POST'])
def complete_survey(student_id):
    """标记问卷完成"""
    db.mark_survey_complete(student_id)
    return jsonify({"success": True, "message": "问卷已完成"})

# ========== AI 画像生成 API ==========

@app.route('/api/portrait/generate', methods=['POST'])
def generate_portrait():
    """生成学生画像报告"""
    data = request.json
    student_id = data.get('student_id')
    api_key = data.get('api_key', '')

    if not api_key:
        # 尝试从环境变量获取默认 API Key
        api_key = os.environ.get('ZHIPU_API_KEY', '')

    if not api_key:
        return jsonify({"success": False, "message": "需要提供 API Key"}), 400

    student = db.get_student_by_id(student_id)
    if not student:
        return jsonify({"success": False, "message": "学生不存在"}), 404

    survey = db.get_survey_by_student(student_id)
    if not survey or not survey.progress:
        return jsonify({"success": False, "message": "请先完成问卷"}), 400

    try:
        progress_data = json.loads(survey.progress) if survey.progress else {}
    except:
        progress_data = {}

    # 清理数据，过滤空值
    clean_data = {k: v for k, v in progress_data.items() if v and (not isinstance(v, list) or len(v) > 0)}

    # 构建 Prompt
    path_names = {
        'preschool': '幼儿启蒙',
        'kitten': '图形化编程',
        'cpp': 'C++编程',
        'ai': 'AI创新'
    }
    path_name = path_names.get(student.path, student.path)

    prompt = f"""你是顶级教育专家。请将以下测评数据转化为高度结构化的数字化画像卡。

姓名：{student.name}
课程路径：{path_name}
性别：{student.gender}
班级：{student.class_name}

测评数据：{json.dumps(clean_data, ensure_ascii=False)}

要求：
1. **完整映射**：涵盖所有勾选项，采用 [维度名 | 观测事实 | 专业定义] 格式
2. **自解释性**：确保非专业人士能直接读懂各项指标含义
3. **禁止臆造**：数据空缺则不提
4. **风格**：客观、严谨、数据密集
5. **结构**：使用 Markdown 格式，包含以下章节：
   - 基础档案
   - 核心特质分析
   - 学习建议
   - 发展预测

请生成专业的学生画像报告。"""

    try:
        # 调用智谱AI API
        response = requests.post(
            'https://open.bigmodel.cn/api/paas/v4/chat/completions',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            },
            json={
                'model': 'glm-4-flash',
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.7
            },
            timeout=60
        )

        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content']

            # 保存到数据库
            doc = StudentPortraitDoc(
                student_id=student_id,
                content=content,
                model_used='glm-4-flash'
            )
            doc_id = db.save_portrait_doc(doc)

            # 标记问卷完成
            db.mark_survey_complete(student_id)

            logger.info(f"Generated portrait for {student.name} (ID: {student_id})")
            return jsonify({
                "success": True,
                "data": {
                    "content": content,
                    "doc_id": doc_id
                }
            })
        else:
            logger.error(f"AI API error: {result}")
            return jsonify({"success": False, "message": "AI 返回格式错误", "error": result}), 500

    except Exception as e:
        logger.error(f"Portrait generation failed: {str(e)}")
        return jsonify({"success": False, "message": f"AI 请求失败: {str(e)}"}), 500

@app.route('/api/portrait/<int:student_id>', methods=['GET'])
def get_portrait(student_id):
    """获取学生最新画像报告"""
    doc = db.get_latest_portrait_doc(student_id)
    if not doc:
        return jsonify({"success": False, "message": "暂无画像报告"}), 404

    return jsonify({
        "success": True,
        "data": {
            "content": doc.content,
            "model_used": doc.model_used,
            "created_at": doc.created_at
        }
    })

@app.route('/api/portrait/all', methods=['GET'])
def get_all_portraits():
    """获取所有有画像的学生"""
    students = db.get_all_students()
    result = []
    for s in students:
        doc = db.get_latest_portrait_doc(s.id)
        if doc:
            result.append({
                "student_id": s.id,
                "name": s.name,
                "class_name": s.class_name,
                "path": s.path,
                "path_name": PATH_CONFIG.get(s.path, {}).get('name', s.path),
                "content_preview": doc.content[:200] + "..." if len(doc.content) > 200 else doc.content,
                "created_at": doc.created_at
            })
    return jsonify({"success": True, "data": result})

# ========== 统计数据 API ==========

@app.route('/api/stats/overview', methods=['GET'])
def get_overview_stats():
    """获取概览统计数据"""
    total_students = len(db.get_all_students())
    path_dist = db.get_path_distribution()

    # 计算已完成问卷的学生数
    surveys_completed = 0
    portraits_count = 0
    for s in db.get_all_students():
        survey = db.get_survey_by_student(s.id)
        if survey and survey.is_completed:
            surveys_completed += 1
        portrait = db.get_latest_portrait_doc(s.id)
        if portrait:
            portraits_count += 1

    return jsonify({
        "success": True,
        "data": {
            "total_students": total_students,
            "surveys_completed": surveys_completed,
            "portraits_count": portraits_count,
            "path_distribution": path_dist
        }
    })

# ========== 数据导入导出 API ==========

@app.route('/api/export', methods=['GET'])
def export_data():
    """导出所有数据"""
    data = db.export_all_data()
    return jsonify({"success": True, "data": data})

@app.route('/api/import', methods=['POST'])
def import_data():
    """导入数据"""
    data = request.json.get('data', {})
    count = db.import_data(data)
    return jsonify({"success": True, "count": count, "message": f"成功导入 {count} 条记录"})

@app.route('/api/export/portraits', methods=['GET'])
def export_all_portraits():
    """导出所有画像报告为 Markdown"""
    students = db.get_all_students()
    md_content = []

    for s in students:
        doc = db.get_latest_portrait_doc(s.id)
        if doc:
            md_content.append(f"# {s.name}\\n\\n{doc.content}\\n\\n---\\n")

    return jsonify({
        "success": True,
        "data": "\\n".join(md_content)
    })

# ========== 错误处理 ==========

@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "message": "接口不存在"}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {str(e)}")
    return jsonify({"success": False, "message": "服务器内部错误"}), 500

# ========== 启动应用 ==========

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'

    print("=" * 60)
    print("🎓 学生画像系统服务启动中...")
    print(f"🌐 访问地址: http://localhost:{port}")
    print("=" * 60)

    app.run(debug=debug, host='0.0.0.0', port=port)
