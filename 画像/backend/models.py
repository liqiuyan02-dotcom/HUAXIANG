"""
数据模型定义模块
定义学生信息相关的数据结构和数据库表模型
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class StudentBasic:
    """学生基础信息"""
    id: Optional[int] = None
    name: str = ""  # 姓名
    student_no: str = ""  # 学号
    age: int = 0  # 年龄
    gender: str = ""  # 性别
    class_name: str = ""  # 班级
    grade: str = ""  # 年级
    path: str = ""  # 课程路径 (preschool/kitten/cpp/ai)
    class_time: str = ""  # 上课时间
    enrollment_date: str = ""  # 入学日期
    contact: str = ""  # 联系方式
    address: str = ""  # 家庭住址
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@dataclass
class StudentAcademic:
    """学生学业信息"""
    id: Optional[int] = None
    student_id: int = 0  # 关联学生ID
    semester: str = ""  # 学期（如：2023-2024-1）
    # 各科成绩
    chinese: Optional[float] = None  # 语文
    math: Optional[float] = None  # 数学
    english: Optional[float] = None  # 英语
    physics: Optional[float] = None  # 物理
    chemistry: Optional[float] = None  # 化学
    biology: Optional[float] = None  # 生物
    history: Optional[float] = None  # 历史
    geography: Optional[float] = None  # 地理
    politics: Optional[float] = None  # 政治
    # 课堂表现评分 (1-5分)
    class_participation: int = 3  # 课堂参与度
    homework_completion: int = 3  # 作业完成情况
    learning_attitude: int = 3  # 学习态度
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@dataclass
class StudentBehavior:
    """学生行为特征信息"""
    id: Optional[int] = None
    student_id: int = 0  # 关联学生ID
    semester: str = ""  # 学期
    # 出勤情况
    attendance_rate: float = 100.0  # 出勤率 (%)
    late_count: int = 0  # 迟到次数
    absence_count: int = 0  # 缺勤次数
    # 课外活动
    clubs: str = ""  # 参加的社团（逗号分隔）
    activities: str = ""  # 参与的活动
    # 兴趣特长
    hobbies: str = ""  # 兴趣爱好
    talents: str = ""  # 特长
    # 行为评价
    discipline_score: int = 5  # 纪律评分 (1-5)
    teamwork_score: int = 5  # 团队协作评分 (1-5)
    leadership_score: int = 5  # 领导力评分 (1-5)
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@dataclass
class StudentSurvey:
    """学生问卷数据"""
    id: Optional[int] = None
    student_id: int = 0
    semester: str = ""
    path: str = ""  # 课程路径
    progress: str = ""  # JSON格式的问卷答案
    remark: str = ""  # 教师备注
    is_completed: bool = False  # 是否完成
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@dataclass
class StudentPortraitDoc:
    """学生画像报告"""
    id: Optional[int] = None
    student_id: int = 0
    content: str = ""  # Markdown格式的报告内容
    model_used: str = ""  # 使用的AI模型
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@dataclass
class StudentTag:
    """学生标签"""
    id: Optional[int] = None
    student_id: int = 0  # 关联学生ID
    tag_name: str = ""  # 标签名称
    tag_category: str = ""  # 标签类别（学业/行为/兴趣/性格）
    tag_value: float = 0.0  # 标签数值（用于权重）
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@dataclass
class StudentPortrait:
    """学生画像数据"""
    student: StudentBasic = field(default_factory=StudentBasic)
    academic: Optional[StudentAcademic] = None
    behavior: Optional[StudentBehavior] = None
    survey: Optional[StudentSurvey] = None
    portrait_doc: Optional[StudentPortraitDoc] = None
    tags: List[StudentTag] = field(default_factory=list)
    analysis_summary: Dict[str, Any] = field(default_factory=dict)  # 分析摘要


# 数据库表结构定义（用于初始化数据库）
TABLE_SCHEMAS = {
    "students": """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_no TEXT UNIQUE,
            age INTEGER,
            gender TEXT,
            class_name TEXT,
            grade TEXT,
            path TEXT DEFAULT 'kitten',
            class_time TEXT,
            enrollment_date TEXT,
            contact TEXT,
            address TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """,
    "student_academic": """
        CREATE TABLE IF NOT EXISTS student_academic (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            semester TEXT NOT NULL,
            chinese REAL,
            math REAL,
            english REAL,
            physics REAL,
            chemistry REAL,
            biology REAL,
            history REAL,
            geography REAL,
            politics REAL,
            class_participation INTEGER DEFAULT 3,
            homework_completion INTEGER DEFAULT 3,
            learning_attitude INTEGER DEFAULT 3,
            created_at TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """,
    "student_behavior": """
        CREATE TABLE IF NOT EXISTS student_behavior (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            semester TEXT NOT NULL,
            attendance_rate REAL DEFAULT 100.0,
            late_count INTEGER DEFAULT 0,
            absence_count INTEGER DEFAULT 0,
            clubs TEXT,
            activities TEXT,
            hobbies TEXT,
            talents TEXT,
            discipline_score INTEGER DEFAULT 5,
            teamwork_score INTEGER DEFAULT 5,
            leadership_score INTEGER DEFAULT 5,
            created_at TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """,
    "student_survey": """
        CREATE TABLE IF NOT EXISTS student_survey (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            semester TEXT,
            path TEXT,
            progress TEXT,
            remark TEXT,
            is_completed INTEGER DEFAULT 0,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """,
    "student_portrait_docs": """
        CREATE TABLE IF NOT EXISTS student_portrait_docs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            content TEXT,
            model_used TEXT,
            created_at TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """,
    "student_tags": """
        CREATE TABLE IF NOT EXISTS student_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            tag_name TEXT NOT NULL,
            tag_category TEXT,
            tag_value REAL DEFAULT 0.0,
            created_at TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """
}


# 问卷配置 - 2026春季班全阶段体系
SURVEY_CONFIG = {
    # ========== 通用基础模块 ==========
    "common": [
        {"group": "学生基础信息", "items": [
            {"id": "info_name", "label": "学生姓名", "type": "text", "placeholder": "请输入学生姓名"},
            {"id": "info_nickname", "label": "常用昵称/小名", "type": "text", "placeholder": "如：小明、乐乐"},
            {"id": "info_gender", "label": "性别", "type": "radio", "opts": ["男","女"]},
            {"id": "info_birth", "label": "出生年月", "type": "text", "placeholder": "如：2018-06"},
            {"id": "info_grade", "label": "当前年级", "type": "radio", "opts": ["小小班","小班","中班","大班","一年级","二年级","三年级","四年级","五年级","六年级","初中"]},
            {"id": "info_school", "label": "所在学校", "type": "text", "placeholder": "幼儿园/学校名称"},
            {"id": "info_class", "label": "班级名称", "type": "text", "placeholder": "如：L1-意识世界-周六上午"},
            {"id": "info_time", "label": "上课时间", "type": "text", "placeholder": "如：周六上午9:00"},
            {"id": "info_contact", "label": "家长联系方式", "type": "text", "placeholder": "手机号/微信"}
        ]},
        {"group": "家庭背景与家长期待（详细）", "items": [
            {"id": "b1", "label": "家中排行", "type": "radio", "opts": ["独生子女","老大(有弟妹)","老二(有兄姐)","老三及以后"]},
            {"id": "b1_1", "label": "是否有兄弟姐妹", "type": "radio", "opts": ["独生","有兄弟姐妹"]},
            {"id": "b2", "label": "主要照护者", "type": "checkbox", "opts": ["父亲","母亲","祖父母/外祖父母","保姆/阿姨","其他"]},
            {"id": "b2_1", "label": "主要教养人", "type": "radio", "opts": ["父母","祖辈","保姆/阿姨","混合"]},
            {"id": "b3", "label": "父母教育背景", "type": "checkbox", "opts": ["高中及以下","大专","本科","硕士","博士","理工科背景","文科背景","教育相关"]},
            {"id": "b4", "label": "家庭教育投入", "type": "radio", "opts": ["非常重视","比较重视","一般","较少关注"]},
            {"id": "b4_1", "label": "教育资源投入", "type": "radio", "opts": ["愿意投入","适度","观望","不额外投入"]},
            {"id": "b5", "label": "课外兴趣班数量", "type": "radio", "opts": ["0个","1-2个","3-4个","5个以上"]},
            {"id": "b5_1", "label": "疲劳程度", "type": "radio", "opts": ["精力充沛","偶尔累","经常疲惫"]},
            {"id": "b6", "label": "每日屏幕时间", "type": "radio", "opts": ["无接触","<30min","30-60min","1-2h","2h以上"]},
            {"id": "b7", "label": "过敏/特殊注意", "type": "text", "placeholder": "如：花生过敏、ADHD等，无则填无"},
            {"id": "b8", "label": "报名初衷", "type": "checkbox", "opts": ["培养兴趣","锻炼专注","社交需求","能力培养","竞赛准备","升学准备","其他"]},
            {"id": "b8_1", "label": "报名目的", "type": "radio", "opts": ["兴趣深化","能力培养","竞赛准备","升学准备"]},
            {"id": "b9", "label": "家长最关注", "type": "radio", "opts": ["开心就好","能力进步","习惯养成","社交发展","竞赛成绩"]},
            {"id": "b9_1", "label": "核心期待", "type": "checkbox", "opts": ["兴趣维持","能力成长","习惯养成","比赛成绩","学习效果"]},
            {"id": "b10", "label": "教育理念", "type": "radio", "opts": ["快乐成长","适度引导","严格要求","自然发展"]},
            {"id": "b10_1", "label": "家长焦虑程度", "type": "radio", "opts": ["佛系","适度关注","较焦虑"]},
            {"id": "b11", "label": "作业辅导", "type": "radio", "opts": ["自主完成","家长陪同","家长主导"]},
            {"id": "b11_1", "label": "学习陪伴", "type": "radio", "opts": ["自主","适度关注","密切参与","主导"]},
            {"id": "b12", "label": "未来规划", "type": "radio", "opts": ["科技特长","综合素质","顺其自然","明确竞赛路径"]},
            {"id": "b12_1", "label": "对AI的态度", "type": "radio", "opts": ["积极拥抱","谨慎乐观","观望","不太了解"]},
            {"id": "b13", "label": "主要联系人", "type": "radio", "opts": ["爸爸","妈妈","父母共同"]},
            {"id": "b13_1", "label": "沟通方式偏好", "type": "checkbox", "opts": ["微信","电话","面谈","定期会议","不频繁打扰"]},
            {"id": "b14", "label": "沟通频率", "type": "radio", "opts": ["每课后","每周","有问题时","阶段总结"]},
            {"id": "b14_1", "label": "沟通时间偏好", "type": "radio", "opts": ["随时","晚上","周末"]},
            {"id": "b15", "label": "关注信息类型", "type": "checkbox", "opts": ["能力成长","比赛信息","升学建议","作品展示","照片/视频","教师描述"]}
        ]},
        {"group": "性格特质（详细）", "items": [
            {"id": "c1", "label": "气质类型", "type": "checkbox", "opts": ["活泼好动(精力充沛)","文静内向(深思熟虑)","谨慎观察(追求完美)","平和稳重(适应良好)","细腻敏感(在意评价)","执着主见(有主见)","慢热淡定(需预热)","精力过人(活跃型)","容易分心(需关注)"]},
            {"id": "c1_1", "label": "分离焦虑程度(幼儿)", "type": "radio", "opts": ["无-入课顺畅","轻度-短暂情绪","中度-需2-4周适应","明显-需特别关注"]},
            {"id": "c2", "label": "面对新环境", "type": "radio", "opts": ["很快适应","需要观察","退缩抗拒","视情况而定"]},
            {"id": "c3", "label": "面对挫折失败", "type": "radio", "opts": ["很快恢复","需要安抚","容易放弃","情绪爆发","不服输重来"]},
            {"id": "c3_1", "label": "挫折恢复速度", "type": "radio", "opts": ["快速恢复","需时间","易气馁","需持续关注"]},
            {"id": "c4", "label": "竞争意识", "type": "radio", "opts": ["强烈渴望第一","享受过程不在意结果","害怕竞争","视情况而定"]},
            {"id": "c4_1", "label": "胜负反应", "type": "radio", "opts": ["胜不骄败不馁","赢了开心输了沮丧","情绪波动大","无所谓"]},
            {"id": "c5", "label": "社交特点", "type": "checkbox", "opts": ["喜欢交朋友","有固定好友圈","偏好独处","社交被动","社交主动","容易冲突","受欢迎","边缘型"]},
            {"id": "c5_1", "label": "同伴互动模式", "type": "radio", "opts": ["主动交友","被动跟随","平行玩耍","独自游戏"]},
            {"id": "c5_2", "label": "与老师互动", "type": "radio", "opts": ["主动亲近","适度交流","观察型","回避型"]},
            {"id": "c6", "label": "情绪表达方式", "type": "checkbox", "opts": ["直接表达","压抑隐藏","寻求安慰","独自消化","转移注意力","情绪外露","语言表达","行为表达"]},
            {"id": "c6_1", "label": "情绪触发点", "type": "text", "placeholder": "如：作品倒塌、规则限制、被忽视等"},
            {"id": "c6_2", "label": "情绪稳定性", "type": "radio", "opts": ["非常稳定","较为稳定","偶有波动","需关注"]},
            {"id": "c7", "label": "有效安抚策略", "type": "checkbox", "opts": ["肢体拥抱","语言鼓励","注意力转移","具体夸奖","陪伴静坐","给予选择权","短暂独处","物质奖励","其他"]},
            {"id": "c7_1", "label": "安抚有效方式", "type": "text", "placeholder": "具体什么方式最有效"},
            {"id": "c8", "label": "压力信号", "type": "text", "placeholder": "如：咬手指、发呆、哭闹、退缩等"},
            {"id": "c9", "label": "自信心水平", "type": "radio", "opts": ["非常自信","比较自信","有时不自信","缺乏自信"]},
            {"id": "c10", "label": "坚持性", "type": "radio", "opts": ["能坚持完成","需鼓励","易放弃","视难度而定"]}
        ]},
        {"group": "学习特点（详细）", "items": [
            {"id": "l1", "label": "学习风格", "type": "checkbox", "opts": ["视觉型(喜欢看图)","听觉型(喜欢听讲)","动觉型(喜欢动手)","阅读型(喜欢文字)","混合型"]},
            {"id": "l1_1", "label": "信息处理方式", "type": "radio", "opts": ["先理解后操作","边做边学","直接试错","观察模仿"]},
            {"id": "l2", "label": "专注力时长", "type": "radio", "opts": ["10分钟以下","10-20分钟","20-30分钟","30-45分钟","45分钟以上"]},
            {"id": "l2_1", "label": "抗干扰能力", "type": "radio", "opts": ["强","一般(提醒可恢复)","弱(易分心)"]},
            {"id": "l2_2", "label": "需提醒频率", "type": "radio", "opts": ["很少","偶尔","经常","持续陪伴"]},
            {"id": "l3", "label": "任务启动速度", "type": "radio", "opts": ["立即开始","需要预热","经常拖延","需要督促"]},
            {"id": "l3_1", "label": "学习节奏", "type": "radio", "opts": ["快速理解","需要消化时间","需重复练习"]},
            {"id": "l4", "label": "任务完成质量", "type": "radio", "opts": ["追求尽善尽美","完成即可","经常半途而废","马虎潦草"]},
            {"id": "l4_1", "label": "作品完成度", "type": "radio", "opts": ["总是完成","基本完成","经常未完成","需辅助完成"]},
            {"id": "l5", "label": "独立思考能力", "type": "radio", "opts": ["能独立解决问题","需少量提示","依赖指导","等待答案"]},
            {"id": "l5_1", "label": "思维类型", "type": "checkbox", "opts": ["分析型(喜欢拆解)","创造型(喜欢创新)","实践型(动手强)","理论型(逻辑强)"]},
            {"id": "l6", "label": "提问主动性", "type": "radio", "opts": ["经常提问","偶尔提问","很少提问","被动回答"]},
            {"id": "l6_1", "label": "提问方式", "type": "radio", "opts": ["主动提问","私下问","不问但困惑","很少困惑"]},
            {"id": "l7", "label": "错误修正态度", "type": "radio", "opts": ["主动找错改正","愿意接受纠正","抗拒批评","不在意错误"]},
            {"id": "l7_1", "label": "调试耐心", "type": "radio", "opts": ["有耐心","一般","易急躁","直接求助"]},
            {"id": "l8", "label": "时间管理能力", "type": "radio", "opts": ["能自主规划","需提醒","经常超时","无时间概念"]},
            {"id": "l8_1", "label": "等待能力", "type": "radio", "opts": ["能等待","需分散注意","等待困难"]},
            {"id": "l9", "label": "笔记/记录习惯", "type": "radio", "opts": ["主动记录","按要求记录","不愿记录","不会记录"]},
            {"id": "l9_1", "label": "知识整理方式", "type": "radio", "opts": ["主动笔记/导图","简单记录","不记录","需指导"]},
            {"id": "l10", "label": "课堂参与度", "type": "radio", "opts": ["非常积极","比较积极","一般","被动","走神"]},
            {"id": "l10_1", "label": "课堂表现", "type": "checkbox", "opts": ["积极举手","被点名能答","被动参与","需鼓励","自由活动时专注","讲解时专注"]},
            {"id": "l11", "label": "作业完成情况", "type": "radio", "opts": ["主动完成","按时完成","经常拖延","需要督促","未完成"]},
            {"id": "l11_1", "label": "课后作业量感受", "type": "radio", "opts": ["轻松","适中","较多"]},
            {"id": "l12", "label": "知识迁移能力", "type": "radio", "opts": ["能举一反三","能模仿应用","需要具体例子","无法迁移"]},
            {"id": "l12_1", "label": "困难处理方式", "type": "radio", "opts": ["查资料解决","问老师","搁置","放弃"]},
            {"id": "l13", "label": "乐高/积木史", "type": "radio", "opts": ["资深玩家(2年+)","经常玩(1年+)","初次接触","完全陌生"]},
            {"id": "l13_1", "label": "在家玩乐高/积木", "type": "radio", "opts": ["经常","偶尔","从不"]},
            {"id": "l14", "label": "精细动作发展", "type": "radio", "opts": ["发展超前","发展适龄","需多练习","明显落后"]},
            {"id": "l15", "label": "科技产品接触", "type": "checkbox", "opts": ["平板电脑","手机","电脑","编程玩具","机器人套件","无接触"]},
            {"id": "l16", "label": "编程基础", "type": "radio", "opts": ["有系统学习","接触过","听说过","完全零基础"]},
            {"id": "l17", "label": "学习主动性", "type": "radio", "opts": ["自主学习","需家长督促","完全被动"]},
            {"id": "l17_1", "label": "预习习惯", "type": "radio", "opts": ["自觉预习","家长督促","仅课堂学习"]},
            {"id": "l17_2", "label": "复习习惯", "type": "radio", "opts": ["自觉复习","家长督促","仅课堂学习"]},
            {"id": "l18", "label": "学习兴趣偏好", "type": "radio", "opts": ["理论学习","项目实践","两者结合"]},
            {"id": "l19", "label": "目标意识", "type": "radio", "opts": ["清晰(知道自己要什么)","模糊(跟随安排)","无(被动参与)"]},
            {"id": "l20", "label": "反思习惯", "type": "radio", "opts": ["主动复盘","提示后反思","不反思"]},
            {"id": "l21", "label": "元认知能力", "type": "radio", "opts": ["能评估自己水平","大概知道","不清楚"]}
        ]},
        {"group": "合作与社交", "items": [
            {"id": "s1", "label": "团队合作表现", "type": "checkbox", "opts": ["主动分享材料","愿意轮流等待","能倾听他人","会协商分工","喜欢独自完成","容易起冲突","规则意识强","领导他人"]},
            {"id": "s2", "label": "角色偏好", "type": "radio", "opts": ["领导者","跟随者","协调者","观察者","独立工作者"]},
            {"id": "s3", "label": "冲突处理方式", "type": "radio", "opts": ["主动调解","寻求成人帮助","回避退让","对抗争执","视情况而定"]},
            {"id": "s4", "label": "分享意愿", "type": "radio", "opts": ["乐于分享","愿意分享","勉强分享","不愿分享"]},
            {"id": "s5", "label": "表达能力", "type": "radio", "opts": ["清晰完整","基本清楚","词不达意","不愿表达"]},
            {"id": "s6", "label": "倾听习惯", "type": "radio", "opts": ["认真倾听","偶尔分心","经常走神","打断他人"]}
        ]},
        {"group": "学科基础与认知发展", "items": [
            {"id": "ac1", "label": "数学基础", "type": "radio", "opts": ["超前","优秀","良好","一般","需加强"]},
            {"id": "ac2", "label": "识字量", "type": "radio", "opts": ["足够自主阅读","可配合拼音","需协助","较弱"]},
            {"id": "ac3", "label": "书写能力", "type": "radio", "opts": ["工整快速","工整较慢","需练习","较弱"]},
            {"id": "ac4", "label": "拼音掌握", "type": "radio", "opts": ["熟练","一般","不熟练","不熟悉"]},
            {"id": "ac5", "label": "英语能力", "type": "radio", "opts": ["能读英文文档","基础词汇","较弱"]},
            {"id": "ac6", "label": "科学素养", "type": "radio", "opts": ["强","一般","较弱"]},
            {"id": "ac7", "label": "逻辑思维能力", "type": "radio", "opts": ["强(抽象思维成熟)","一般(具体为主)","待发展"]},
            {"id": "ac8", "label": "空间想象能力", "type": "radio", "opts": ["丰富","一般","较务实","待开发"]},
            {"id": "ac9", "label": "知识迁移能力", "type": "radio", "opts": ["善于迁移","需提示","较局限"]},
            {"id": "ac10", "label": "现实联系能力", "type": "radio", "opts": ["能联系实际","课堂为主","较抽象"]}
        ]},
        {"group": "竞赛与成就（小学中高年级）", "items": [
            {"id": "cp1", "label": "参赛经历", "type": "radio", "opts": ["无","校内","区级","市级","省级","国家级"]},
            {"id": "cp2", "label": "竞赛心态", "type": "radio", "opts": ["享受过程","目标导向","压力过大","无所谓"]},
            {"id": "cp3", "label": "抗压能力", "type": "radio", "opts": ["强(紧张但能发挥)","一般","易紧张"]},
            {"id": "cp4", "label": "团队协作", "type": "radio", "opts": ["善于配合","可配合","倾向独立"]},
            {"id": "cp5", "label": "临场应变", "type": "radio", "opts": ["灵活","一般","需充分准备"]},
            {"id": "cp6", "label": "团队角色", "type": "radio", "opts": ["leader","执行者","创意者","配合者"]},
            {"id": "cp7", "label": "成就动机", "type": "radio", "opts": ["内在驱动","外在认可","两者兼有","无明显动机"]},
            {"id": "cp8", "label": "目标设定", "type": "radio", "opts": ["自己设定","家长设定","老师设定","无明确目标"]},
            {"id": "cp9", "label": "挫折恢复", "type": "radio", "opts": ["快速恢复","需时间","易气馁"]}
        ]},
        {"group": "职业规划意识（小学高段萌芽）", "items": [
            {"id": "ca1", "label": "未来职业想法", "type": "text", "placeholder": "如有"},
            {"id": "ca2", "label": "科技行业认知", "type": "radio", "opts": ["有了解","初步接触","无概念"]},
            {"id": "ca3", "label": "学习动力来源", "type": "checkbox", "opts": ["兴趣","未来目标","成就感","外部要求"]},
            {"id": "ca4", "label": "发展方向", "type": "radio", "opts": ["信奥/算法竞赛","AIGC应用","两者都有兴趣","尚未确定"]}
        ]},
        {"group": "健康与安全", "items": [
            {"id": "h1", "label": "过敏史", "type": "text", "placeholder": "如有请填写"},
            {"id": "h2", "label": "饮食注意", "type": "text", "placeholder": "如有请填写"},
            {"id": "h3", "label": "身体协调", "type": "radio", "opts": ["良好","一般","需关注"]},
            {"id": "h4", "label": "如厕情况", "type": "radio", "opts": ["完全自理","偶尔需帮助","需提醒"]},
            {"id": "h5", "label": "特殊健康状况", "type": "text", "placeholder": "如：ADHD、感统失调等"}
        ]},
        {"group": "其他观察", "items": [
            {"id": "o1", "label": "特殊才能", "type": "checkbox", "opts": ["数学逻辑","语言表达","空间感知","音乐节奏","身体协调","艺术创造","记忆力强","观察细致"]},
            {"id": "o2", "label": "需要特别关注", "type": "checkbox", "opts": ["注意力缺陷","多动倾向","自闭倾向","感统失调","情绪障碍","学习困难","gifted(超常)"]},
            {"id": "o3", "label": "近期重要事件", "type": "text", "placeholder": "如：刚上幼儿园、家庭变故等"},
            {"id": "o4", "label": "教师综合评语", "type": "textarea", "placeholder": "对学生的整体观察和建议"}
        ]}
    ],

    # ========== L1 意识世界（小小班）==========
    "l1_awareness": [
        {"group": "L1 管道建构与空间意识", "items": [
            {"id": "l1_1", "label": "管道连接精准度", "type": "radio", "opts": ["独立精准连接","需辅助对齐","经常接反或错位","完全需要帮助"]},
            {"id": "l1_2", "label": "路线规划能力", "type": "checkbox", "opts": ["能预设完整路线","会调整转弯角度","理解高低落差","会预留出口","只会直线延伸","随意搭建无规划"]},
            {"id": "l1_3", "label": "结构稳定性意识", "type": "radio", "opts": ["主动加固连接处","会检查摇晃度","搭完就测试","反复倒塌 unaware"]},
            {"id": "l1_4", "label": "任务理解与执行", "type": "checkbox", "opts": ["能复述任务要求","按步骤完成","会自我检查","需多次提醒","容易中途换玩法"]},
            {"id": "l1_5", "label": "表达分享能力", "type": "radio", "opts": ["完整讲述搭建过程","能说清作品功能","只能说作品名称","不愿表达分享"]}
        ]}
    ],

    # ========== L2 发现世界（小班）==========
    "l2_discovery": [
        {"group": "L2 工程拆装与精细动作", "items": [
            {"id": "l2_1", "label": "螺丝刀使用能力", "type": "radio", "opts": ["独立精准固定","懂得顺松逆紧","需手部辅助稳定","无法对准孔位"]},
            {"id": "l2_2", "label": "结构稳定性意识", "type": "checkbox", "opts": ["主动加固底部","理解垂直支撑","螺丝拧得恰到好处","只会盲目堆砌","力道过猛易散架"]},
            {"id": "l2_3", "label": "分类与排序逻辑", "type": "checkbox", "opts": ["按颜色分类快","按长短排序准","准确估计数量","理解大小关系","会用表格记录"]},
            {"id": "l2_4", "label": "任务复杂度适应", "type": "radio", "opts": ["独立完成多步任务","需分解步骤提示","仅能完成单一步骤","经常遗漏环节"]},
            {"id": "l2_5", "label": "调试与坚持度", "type": "radio", "opts": ["反复调试直到成功","试几次后放弃","直接求助老师","无所谓完成度"]}
        ]}
    ],

    # ========== L3 发明世界（中班）==========
    "l3_invention": [
        {"group": "L3 实物编程与机械启蒙", "items": [
            {"id": "l3_1", "label": "编程指令理解", "type": "checkbox", "opts": ["理解前进/后退方向","掌握转向角度","会使用循环","理解条件判断","能独立读程序"]},
            {"id": "l3_2", "label": "多级加速理解", "type": "radio", "opts": ["理解二级加速原理","能解释快慢原因","会应用大小齿轮","只会模仿搭建"]},
            {"id": "l3_3", "label": "传动机构调试", "type": "checkbox", "opts": ["齿轮咬合精准","皮带张力适中","连杆运动顺畅","会调整对齐度","遇问题主动调试"]},
            {"id": "l3_4", "label": "因果复述能力", "type": "radio", "opts": ["说清'因为...所以'","能说步骤和原因","只能说作品名","逻辑跳跃无关联"]},
            {"id": "l3_5", "label": "创新与改造", "type": "checkbox", "opts": ["主动添加创意","会改良结构","尝试不同方案","严格按图搭建","拒绝改变"]},
            {"id": "l3_6", "label": "调试与优化循环", "type": "radio", "opts": ["多次测试改进","找原因改方案","试一次就结束","不测试直接展示"]}
        ]}
    ],

    # ========== L4 动力机械（中班）==========
    "l4_power": [
        {"group": "L4 动力传动与机械工程", "items": [
            {"id": "l4_1", "label": "齿轮传动系统", "type": "checkbox", "opts": ["理解减速/加速","计算齿比关系","多级传动设计","会解决打滑问题","精准对齐齿轮"]},
            {"id": "l4_2", "label": "连杆机构应用", "type": "checkbox", "opts": ["四边形结构","曲柄摇杆","实现往复运动","实现摆动转向","创意机构组合"]},
            {"id": "l4_3", "label": "机械稳定性调试", "type": "radio", "opts": ["跑得稳不卡顿","会调整结构位置","优化齿轮比例","只搭不调试"]},
            {"id": "l4_4", "label": "工程问题解决", "type": "checkbox", "opts": ["定位问题原因","提出改进方案","验证解决方案","记录调试过程","工程思维闭环"]},
            {"id": "l4_5", "label": "速度与力量权衡", "type": "radio", "opts": ["理解速度/力量关系","按需求选择齿比","会计算预测","随意搭配"]},
            {"id": "l4_6", "label": "作品完成度", "type": "radio", "opts": ["完整运转流畅","基本功能实现","需辅助才能运行","结构问题明显"]}
        ]}
    ],

    # ========== L5 创造世界（大班）==========
    "l5_creation": [
        {"group": "L5 WeDo智能编程与传感器", "items": [
            {"id": "l5_1", "label": "程序结构理解", "type": "checkbox", "opts": ["理解顺序结构","使用循环重复","条件分支判断","变量存储数据","函数模块化"]},
            {"id": "l5_2", "label": "传感器应用", "type": "checkbox", "opts": ["距离传感器","倾斜传感器","声音传感器","多传感器组合","智能决策逻辑"]},
            {"id": "l5_3", "label": "电机控制", "type": "checkbox", "opts": ["精准控制转速","正反转切换","运行时长控制","功率调节"]},
            {"id": "l5_4", "label": "调试与优化", "type": "radio", "opts": ["反复测试找最优","会改结构/改程序","数据记录对比","一次性完成不调试"]},
            {"id": "l5_5", "label": "智能流程设计", "type": "checkbox", "opts": ["感知-判断-动作闭环","多条件组合判断","错误处理机制","用户交互设计"]},
            {"id": "l5_6", "label": "作品展示表达", "type": "radio", "opts": ["完整演示+讲解","说明功能逻辑","只说能做什么","不愿展示"]}
        ]}
    ],

    # ========== SPIKE（一年级）==========
    "spike": [
        {"group": "SPIKE Prime 工程与数据思维", "items": [
            {"id": "sp_1", "label": "程序架构设计", "type": "checkbox", "opts": ["模块化程序结构","自定义积木/函数","列表/数组应用","参数化调优","系统排错能力"]},
            {"id": "sp_2", "label": "多条件决策", "type": "checkbox", "opts": ["距离+角度综合","时间+速度判断","传感器数据融合","复杂状态机","多分支逻辑"]},
            {"id": "sp_3", "label": "精度控制", "type": "radio", "opts": ["角度距离精准","阈值调整得当","结果稳定一致","波动较大"]},
            {"id": "sp_4", "label": "调试方法论", "type": "checkbox", "opts": ["区分结构/程序/传感器问题","数据观察分析","参数微调验证","记录调试日志","形成解决方案"]},
            {"id": "sp_5", "label": "主题项目能力", "type": "radio", "opts": ["科技生活项目","疯狂嘉年华游戏","能量转换理解","协作沟通表达"]},
            {"id": "sp_6", "label": "项目稳定性", "type": "radio", "opts": ["可重复稳定完成","偶尔需要调整","经常失败需帮助","单次偶然成功"]}
        ]}
    ],

    # ========== Kitten K2（二年级）==========
    "kitten_k2": [
        {"group": "K2 图形化基础与数据思维", "items": [
            {"id": "k2_1", "label": "变量应用", "type": "checkbox", "opts": ["创建与赋值","显示与隐藏","数值增减变化","多变量管理","变量逻辑应用"]},
            {"id": "k2_2", "label": "程序结构", "type": "checkbox", "opts": ["顺序执行清晰","循环结构使用","条件判断分支","循环分支嵌套","逻辑组合应用"]},
            {"id": "k2_3", "label": "画笔与坐标", "type": "checkbox", "opts": ["坐标定位准确","绘制几何图形","轨迹控制","图形变换","创意绘图"]},
            {"id": "k2_4", "label": "交互设计", "type": "checkbox", "opts": ["输入输出交互","选择题设计","文字印章","语音翻译/侦测","用户反馈设计"]},
            {"id": "k2_5", "label": "AI/AR初探", "type": "radio", "opts": ["积极尝试新功能","理解AI概念","AR互动体验","创意科技应用"]},
            {"id": "k2_6", "label": "Bug调试能力", "type": "radio", "opts": ["自主发现修复","定位问题原因","需提示才找到","直接求助老师"]},
            {"id": "k2_7", "label": "作品完整度", "type": "radio", "opts": ["有规则有挑战","功能完整可玩","基本完成要求","功能缺失明显"]}
        ]}
    ],

    # ========== Kitten K4（三年级）==========
    "kitten_k4": [
        {"group": "K4 图形化进阶与竞赛能力", "items": [
            {"id": "k4_1", "label": "复杂逻辑", "type": "checkbox", "opts": ["条件循环嵌套","逻辑运算组合","多条件判断","布尔逻辑","算法逻辑"]},
            {"id": "k4_2", "label": "克隆技术", "type": "checkbox", "opts": ["克隆体生成","克隆体控制","弹幕机制","对象池管理","性能优化"]},
            {"id": "k4_3", "label": "数据系统", "type": "checkbox", "opts": ["变量2应用","云变量联网","数据存储","统计与排行榜","多用户交互"]},
            {"id": "k4_4", "label": "函数与模块化", "type": "checkbox", "opts": ["自定义积木","函数参数传递","代码复用","模块化设计","封装思想"]},
            {"id": "k4_5", "label": "列表应用", "type": "checkbox", "opts": ["列表创建","增删改查操作","遍历循环","题库/背包系统","关卡数据管理"]},
            {"id": "k4_6", "label": "字符串处理", "type": "checkbox", "opts": ["字符串连接","子串提取","字符遍历","文本处理","加密解密"]},
            {"id": "k4_7", "label": "物理引擎", "type": "checkbox", "opts": ["重力模拟","碰撞检测","反弹摩擦","运动轨迹","真实物理效果"]},
            {"id": "k4_8", "label": "竞赛项目能力", "type": "radio", "opts": ["独立完成复杂项目","添加机制关卡策略","作品完成度高","具比赛竞争力"]}
        ]}
    ],

    # ========== AICODE01（C++入门）==========
    "cpp_a1": [
        {"group": "A1 代码英雄 C++基础", "items": [
            {"id": "a1_1", "label": "代码阅读习惯", "type": "checkbox", "opts": ["理解代码结构","识别语法元素","理解注释","分析代码逻辑","预测运行结果"]},
            {"id": "a1_2", "label": "基础语法掌握", "type": "checkbox", "opts": ["变量定义使用","输入输出语句","基本运算","条件判断","循环结构"]},
            {"id": "a1_3", "label": "任务驱动学习", "type": "radio", "opts": ["先理解任务再学","边做边学","被动跟随","死记硬背语法"]},
            {"id": "a1_4", "label": "即时反馈调试", "type": "checkbox", "opts": ["主动找Bug","观察角色行为","测试验证","优化方案","享受调试"]},
            {"id": "a1_5", "label": "计算思维建立", "type": "radio", "opts": ["逻辑清晰","步骤明确","会改会解决问题","混乱无序"]},
            {"id": "a1_6", "label": "课程完成度", "type": "radio", "opts": ["全部通关","大部分完成","基本完成","进度落后"]}
        ]}
    ],

    # ========== AICODE02（C++进阶）==========
    "cpp_a2": [
        {"group": "A2 代码岛英雄 C++进阶", "items": [
            {"id": "a2_1", "label": "复杂条件判断", "type": "checkbox", "opts": ["If-Else嵌套","多条件组合","与或逻辑","选择型问题","逻辑推理"]},
            {"id": "a2_2", "label": "循环与数组", "type": "checkbox", "opts": ["循环遍历","数组定义","数据存储","索引访问","批量处理"]},
            {"id": "a2_3", "label": "调试纠错能力", "type": "radio", "opts": ["定位问题","调整策略","独立解决","依赖答案","回避调试"]},
            {"id": "a2_4", "label": "地图任务闯关", "type": "checkbox", "opts": ["路径规划","坐标计算","条件判断","循环优化","组合策略"]},
            {"id": "a2_5", "label": "代码规范性", "type": "checkbox", "opts": ["缩进整齐","命名规范","注释清晰","结构清晰","可读性强"]},
            {"id": "a2_6", "label": "方向选择", "type": "radio", "opts": ["倾向信奥竞赛","倾向AIGC应用","两者都有兴趣","尚未确定"]}
        ]}
    ],

    # ========== AICODE03（AI创新）==========
    "ai_a3": [
        {"group": "A3 AI编程创新与AIGC", "items": [
            {"id": "a3_1", "label": "Prompt工程能力", "type": "checkbox", "opts": ["需求描述清晰","结构化Prompt","多轮迭代优化","上下文示例","Few-shot技巧"]},
            {"id": "a3_2", "label": "AI结果验证", "type": "checkbox", "opts": ["识别AI幻觉","运行验证逻辑","判断代码质量","发现潜在问题","修正AI错误"]},
            {"id": "a3_3", "label": "人机协作调试", "type": "radio", "opts": ["描述Bug精准","让AI协助修复","自己判断对错","盲信AI结果"]},
            {"id": "a3_4", "label": "MVP产品思维", "type": "radio", "opts": ["先通逻辑再美化","快速原型迭代","纠结细节进程慢","无迭代意识"]},
            {"id": "a3_5", "label": "项目完整性", "type": "checkbox", "opts": ["可玩小游戏","实用小工具","用户体验优化","持续改进","发布展示"]},
            {"id": "a3_6", "label": "信息伦理意识", "type": "checkbox", "opts": ["素材版权意识","AI结果真实性","账号数据安全","技术伦理思考"]},
            {"id": "a3_7", "label": "创造力与表达", "type": "radio", "opts": ["创意丰富","表达清晰","作品独特","缺乏想法"]}
        ]}
    ],

    # ========== 保留旧路径兼容 ==========
    "preschool": [
        {"group": "幼儿阶段综合评估", "items": [
            {"id": "p_old_1", "label": "精细动作发展", "type": "radio", "opts": ["发展超前","发展适龄","需多练习","明显落后"]},
            {"id": "p_old_2", "label": "任务完成度", "type": "radio", "opts": ["独立完成","需少量提示","需全程辅助","无法完成"]},
            {"id": "p_old_3", "label": "分享表达", "type": "radio", "opts": ["主动完整表达","能回答问题","只会说名称","不愿表达"]}
        ]}
    ],
    "kitten": [
        {"group": "图形化编程综合评估", "items": [
            {"id": "k_old_1", "label": "程序复杂度", "type": "checkbox", "opts": ["多角色互动","循环嵌套","条件判断","变量应用","克隆技术"]},
            {"id": "k_old_2", "label": "调试能力", "type": "radio", "opts": ["独立调试","需提示","直接求助","跳过调试"]},
            {"id": "k_old_3", "label": "创意表现", "type": "radio", "opts": ["原创丰富","有改良","模仿为主","完全范例"]}
        ]}
    ],
    "cpp": [
        {"group": "C++编程综合评估", "items": [
            {"id": "c_old_1", "label": "代码规范", "type": "checkbox", "opts": ["缩进规范","命名合理","注释清晰","结构清晰"]},
            {"id": "c_old_2", "label": "算法思维", "type": "radio", "opts": ["逻辑严谨","思路清晰","基本理解","混乱无序"]},
            {"id": "c_old_3", "label": "调试能力", "type": "radio", "opts": ["独立找Bug","定位准确","需提示","直接要答案"]}
        ]}
    ],
    "ai": [
        {"group": "AI创新综合评估", "items": [
            {"id": "a_old_1", "label": "Prompt质量", "type": "radio", "opts": ["结构化精准","描述清晰","简单提问","模糊不清"]},
            {"id": "a_old_2", "label": "AI协作", "type": "radio", "opts": [ "人机协作","验证结果","复制粘贴","盲目信任"]},
            {"id": "a_old_3", "label": "产品思维", "type": "radio", "opts": ["MVP迭代","追求完成","纠结细节","无迭代意识"]}
        ]}
    ]
}


# 课程路径配置 - 2026春季班全阶段体系
PATH_CONFIG = {
    # 幼儿阶段
    "l1_awareness": {"name": "L1 意识世界", "badge_class": "badge-preschool", "color": "#ef4444", "grade": "小小班", "tool": "管道游戏套装"},
    "l2_discovery": {"name": "L2 发现世界", "badge_class": "badge-preschool", "color": "#f97316", "grade": "小班", "tool": "百变工程螺丝刀"},
    "l3_invention": {"name": "L3 发明世界", "badge_class": "badge-preschool", "color": "#f59e0b", "grade": "中班", "tool": "实物编程+简单机械"},
    "l4_power": {"name": "L4 动力机械", "badge_class": "badge-preschool", "color": "#eab308", "grade": "中班", "tool": "9686动力机械"},
    "l5_creation": {"name": "L5 创造世界", "badge_class": "badge-preschool", "color": "#84cc16", "grade": "大班", "tool": "WeDo 2.0"},
    "spike": {"name": "SPIKE", "badge_class": "badge-kitten", "color": "#10b981", "grade": "一年级", "tool": "SPIKE Prime"},
    # 图形化阶段
    "kitten_k2": {"name": "Kitten K2 萌新", "badge_class": "badge-kitten", "color": "#06b6d4", "grade": "二年级", "tool": "Kitten图形化"},
    "kitten_k4": {"name": "Kitten K4 乐学", "badge_class": "badge-kitten", "color": "#3b82f6", "grade": "三年级", "tool": "Kitten图形化进阶"},
    # 代码阶段
    "cpp_a1": {"name": "AICODE01 代码英雄", "badge_class": "badge-cpp", "color": "#6366f1", "grade": "入门", "tool": "C++基础"},
    "cpp_a2": {"name": "AICODE02 代码岛英雄", "badge_class": "badge-cpp", "color": "#8b5cf6", "grade": "进阶", "tool": "C++进阶"},
    "ai_a3": {"name": "AICODE03 AI创新", "badge_class": "badge-ai", "color": "#a855f7", "grade": "高阶", "tool": "AIGC开发"},
    # 保留旧路径兼容
    "preschool": {"name": "幼儿启蒙", "badge_class": "badge-preschool", "color": "#ef4444"},
    "kitten": {"name": "图形化编程", "badge_class": "badge-kitten", "color": "#10b981"},
    "cpp": {"name": "C++编程", "badge_class": "badge-cpp", "color": "#2563eb"},
    "ai": {"name": "AI创新", "badge_class": "badge-ai", "color": "#9333ea"}
}


# 智能路径识别规则 - 2026春季班
def detect_path(class_name: str) -> str:
    """根据班级名称智能识别课程路径"""
    if not class_name:
        return "preschool"

    cls = class_name.upper().replace(" ", "").replace("-", "").replace("_", "")

    # 优先级 1: AICODE 03 / AI创新 / AIGC
    if any(k in cls for k in ["AICODE03", "AI创新", "AIGC", "AICODE3"]):
        return "ai_a3"

    # 优先级 2: AICODE 02 / 代码岛 / 进阶
    if any(k in cls for k in ["AICODE02", "代码岛", "AICODE2", "代码岛英雄"]):
        return "cpp_a2"

    # 优先级 3: AICODE 01 / 代码英雄 / C++
    if any(k in cls for k in ["AICODE01", "代码英雄", "AICODE1", "AICODE", "C++", "CPP"]):
        return "cpp_a1"

    # 优先级 4: SPIKE
    if "SPIKE" in cls:
        return "spike"

    # 优先级 5: Kitten K4 / 三年级 / 乐学 / 进阶
    if any(k in cls for k in ["KITTENK4", "K4", "三年级", "乐学", "KITTEN4"]):
        return "kitten_k4"

    # 优先级 6: Kitten K2 / 二年级 / 萌新 / 入门
    if any(k in cls for k in ["KITTENK2", "K2", "二年级", "萌新", "KITTEN2", "图形化"]):
        return "kitten_k2"

    # 优先级 7: L5 创造世界 / 大班 / WeDo
    if any(k in cls for k in ["L5", "创造世界", "WEDO", "大班"]):
        return "l5_creation"

    # 优先级 8: L4 动力机械 / 9686
    if any(k in cls for k in ["L4", "动力机械", "9686"]):
        return "l4_power"

    # 优先级 9: L3 发明世界 / 中班
    if any(k in cls for k in ["L3", "发明世界", "中班"]):
        return "l3_invention"

    # 优先级 10: L2 发现世界 / 小班 / 螺丝刀
    if any(k in cls for k in ["L2", "发现世界", "小班", "螺丝刀"]):
        return "l2_discovery"

    # 优先级 11: L1 意识世界 / 小小班 / 管道
    if any(k in cls for k in ["L1", "意识世界", "小小班", "管道", "管道游戏"]):
        return "l1_awareness"

    # 默认: 启蒙方向
    return "preschool"


# 预定义标签体系
TAG_SYSTEM = {
    "学业水平": [
        {"name": "学霸", "condition": "avg_score >= 90"},
        {"name": "优秀生", "condition": "avg_score >= 80"},
        {"name": "中等生", "condition": "avg_score >= 60"},
        {"name": "需努力", "condition": "avg_score < 60"},
        {"name": "偏科型", "condition": "max_score - min_score > 20"},
        {"name": "全能型", "condition": "all_score >= 80"},
    ],
    "学习习惯": [
        {"name": "积极主动", "condition": "class_participation >= 4"},
        {"name": "作业优秀", "condition": "homework_completion >= 4"},
        {"name": "态度认真", "condition": "learning_attitude >= 4"},
        {"name": "需督促", "condition": "homework_completion <= 2"},
    ],
    "出勤表现": [
        {"name": "全勤", "condition": "attendance_rate == 100"},
        {"name": "出勤良好", "condition": "attendance_rate >= 95"},
        {"name": "出勤一般", "condition": "attendance_rate >= 90"},
        {"name": "需关注", "condition": "attendance_rate < 90"},
    ],
    "综合素质": [
        {"name": "社团活跃", "condition": "len(clubs) > 0"},
        {"name": "特长明显", "condition": "len(talents) > 0"},
        {"name": "团队核心", "condition": "teamwork_score >= 4"},
        {"name": "领导潜质", "condition": "leadership_score >= 4"},
        {"name": "纪律模范", "condition": "discipline_score >= 4"},
    ]
}
