"""
数据分析模块
负责学生数据的分析计算、标签生成和画像构建
"""

import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import asdict
from models import (
    StudentBasic, StudentAcademic, StudentBehavior,
    StudentTag, StudentPortrait, TAG_SYSTEM
)
from database import db


class StudentAnalyzer:
    """学生数据分析器"""

    # 学科列表
    SUBJECTS = ["chinese", "math", "english", "physics", "chemistry",
                "biology", "history", "geography", "politics"]
    SUBJECT_NAMES = {
        "chinese": "语文", "math": "数学", "english": "英语",
        "physics": "物理", "chemistry": "化学", "biology": "生物",
        "history": "历史", "geography": "地理", "politics": "政治"
    }

    def __init__(self):
        self.tag_system = TAG_SYSTEM

    def analyze_student(self, student_id: int, semester: str = None) -> StudentPortrait:
        """分析单个学生，生成完整画像

        Args:
            student_id: 学生ID
            semester: 学期，不指定则使用最新数据

        Returns:
            StudentPortrait: 学生画像对象
        """
        # 获取基础信息
        student = db.get_student_by_id(student_id)
        if not student:
            raise ValueError(f"未找到ID为{student_id}的学生")

        portrait = StudentPortrait(student=student)

        # 获取学业数据
        academic_records = db.get_academic_records(student_id, semester)
        if academic_records:
            portrait.academic = academic_records[0]  # 取最新记录

        # 获取行为数据
        behavior_records = db.get_behavior_records(student_id, semester)
        if behavior_records:
            portrait.behavior = behavior_records[0]

        # 生成标签
        tags = self._generate_tags(portrait)
        portrait.tags = tags

        # 保存标签到数据库
        self._save_tags(student_id, tags)

        # 生成分析摘要
        portrait.analysis_summary = self._generate_summary(portrait)

        return portrait

    def batch_analyze_class(self, class_name: str, semester: str) -> List[StudentPortrait]:
        """批量分析班级所有学生

        Args:
            class_name: 班级名称
            semester: 学期

        Returns:
            List[StudentPortrait]: 班级学生画像列表
        """
        students = db.get_all_students(class_name=class_name)
        portraits = []
        for student in students:
            try:
                portrait = self.analyze_student(student.id, semester)
                portraits.append(portrait)
            except Exception as e:
                print(f"分析学生 {student.name} 时出错: {e}")
        return portraits

    def _generate_tags(self, portrait: StudentPortrait) -> List[StudentTag]:
        """根据学生数据生成标签"""
        tags = []
        academic = portrait.academic
        behavior = portrait.behavior

        if academic:
            # 计算学业标签
            tags.extend(self._calculate_academic_tags(academic))

        if behavior:
            # 计算出勤标签
            tags.extend(self._calculate_attendance_tags(behavior))
            # 计算综合素质标签
            tags.extend(self._calculate_quality_tags(behavior))

        return tags

    def _calculate_academic_tags(self, academic: StudentAcademic) -> List[StudentTag]:
        """计算学业相关标签"""
        tags = []

        # 获取所有科目成绩
        scores = []
        for subject in self.SUBJECTS:
            score = getattr(academic, subject)
            if score is not None:
                scores.append(score)

        if not scores:
            return tags

        avg_score = np.mean(scores)
        max_score = max(scores)
        min_score = min(scores)

        # 学业水平标签
        if avg_score >= 90:
            tags.append(StudentTag(
                student_id=academic.student_id,
                tag_name="学霸",
                tag_category="学业水平",
                tag_value=avg_score
            ))
        elif avg_score >= 80:
            tags.append(StudentTag(
                student_id=academic.student_id,
                tag_name="优秀生",
                tag_category="学业水平",
                tag_value=avg_score
            ))
        elif avg_score >= 60:
            tags.append(StudentTag(
                student_id=academic.student_id,
                tag_name="中等生",
                tag_category="学业水平",
                tag_value=avg_score
            ))
        else:
            tags.append(StudentTag(
                student_id=academic.student_id,
                tag_name="需努力",
                tag_category="学业水平",
                tag_value=avg_score
            ))

        # 偏科型标签
        if max_score - min_score > 20:
            tags.append(StudentTag(
                student_id=academic.student_id,
                tag_name="偏科型",
                tag_category="学业水平",
                tag_value=max_score - min_score
            ))

        # 全能型标签
        if all(s >= 80 for s in scores):
            tags.append(StudentTag(
                student_id=academic.student_id,
                tag_name="全能型",
                tag_category="学业水平",
                tag_value=avg_score
            ))

        # 学习习惯标签
        if academic.class_participation >= 4:
            tags.append(StudentTag(
                student_id=academic.student_id,
                tag_name="积极主动",
                tag_category="学习习惯",
                tag_value=academic.class_participation
            ))

        if academic.homework_completion >= 4:
            tags.append(StudentTag(
                student_id=academic.student_id,
                tag_name="作业优秀",
                tag_category="学习习惯",
                tag_value=academic.homework_completion
            ))
        elif academic.homework_completion <= 2:
            tags.append(StudentTag(
                student_id=academic.student_id,
                tag_name="需督促",
                tag_category="学习习惯",
                tag_value=academic.homework_completion
            ))

        if academic.learning_attitude >= 4:
            tags.append(StudentTag(
                student_id=academic.student_id,
                tag_name="态度认真",
                tag_category="学习习惯",
                tag_value=academic.learning_attitude
            ))

        # 优势学科标签
        for subject in self.SUBJECTS:
            score = getattr(academic, subject)
            if score and score >= 90:
                subject_cn = self.SUBJECT_NAMES.get(subject, subject)
                tags.append(StudentTag(
                    student_id=academic.student_id,
                    tag_name=f"{subject_cn}优秀",
                    tag_category="优势学科",
                    tag_value=score
                ))

        return tags

    def _calculate_attendance_tags(self, behavior: StudentBehavior) -> List[StudentTag]:
        """计算出勤相关标签"""
        tags = []

        if behavior.attendance_rate == 100:
            tags.append(StudentTag(
                student_id=behavior.student_id,
                tag_name="全勤",
                tag_category="出勤表现",
                tag_value=behavior.attendance_rate
            ))
        elif behavior.attendance_rate >= 95:
            tags.append(StudentTag(
                student_id=behavior.student_id,
                tag_name="出勤良好",
                tag_category="出勤表现",
                tag_value=behavior.attendance_rate
            ))
        elif behavior.attendance_rate < 90:
            tags.append(StudentTag(
                student_id=behavior.student_id,
                tag_name="需关注",
                tag_category="出勤表现",
                tag_value=behavior.attendance_rate
            ))

        return tags

    def _calculate_quality_tags(self, behavior: StudentBehavior) -> List[StudentTag]:
        """计算综合素质标签"""
        tags = []

        # 社团活跃
        if behavior.clubs and len(behavior.clubs.strip()) > 0:
            tags.append(StudentTag(
                student_id=behavior.student_id,
                tag_name="社团活跃",
                tag_category="综合素质",
                tag_value=len(behavior.clubs.split(","))
            ))

        # 特长明显
        if behavior.talents and len(behavior.talents.strip()) > 0:
            tags.append(StudentTag(
                student_id=behavior.student_id,
                tag_name="特长明显",
                tag_category="综合素质",
                tag_value=1
            ))

        # 团队核心
        if behavior.teamwork_score >= 4:
            tags.append(StudentTag(
                student_id=behavior.student_id,
                tag_name="团队核心",
                tag_category="综合素质",
                tag_value=behavior.teamwork_score
            ))

        # 领导潜质
        if behavior.leadership_score >= 4:
            tags.append(StudentTag(
                student_id=behavior.student_id,
                tag_name="领导潜质",
                tag_category="综合素质",
                tag_value=behavior.leadership_score
            ))

        # 纪律模范
        if behavior.discipline_score >= 4:
            tags.append(StudentTag(
                student_id=behavior.student_id,
                tag_name="纪律模范",
                tag_category="综合素质",
                tag_value=behavior.discipline_score
            ))

        return tags

    def _save_tags(self, student_id: int, tags: List[StudentTag]):
        """保存标签到数据库"""
        # 先删除旧标签
        db.delete_student_tags(student_id)
        # 保存新标签
        for tag in tags:
            tag.student_id = student_id
            db.create_tag(tag)

    def _generate_summary(self, portrait: StudentPortrait) -> Dict[str, Any]:
        """生成分析摘要"""
        summary = {
            "overview": "",
            "strengths": [],
            "weaknesses": [],
            "suggestions": []
        }

        # 基于标签生成摘要
        tag_categories = {}
        for tag in portrait.tags:
            if tag.tag_category not in tag_categories:
                tag_categories[tag.tag_category] = []
            tag_categories[tag.tag_category].append(tag.tag_name)

        # 概述
        if portrait.academic:
            scores = [getattr(portrait.academic, s) for s in self.SUBJECTS
                     if getattr(portrait.academic, s) is not None]
            if scores:
                avg = np.mean(scores)
                summary["overview"] = f"该生平均成绩为{avg:.1f}分，"

                # 优势学科
                strength_subjects = []
                for subject in self.SUBJECTS:
                    score = getattr(portrait.academic, subject)
                    if score and score >= 85:
                        strength_subjects.append(self.SUBJECT_NAMES[subject])

                if strength_subjects:
                    summary["strengths"].append(f"擅长科目：{', '.join(strength_subjects)}")

                # 薄弱学科
                weak_subjects = []
                for subject in self.SUBJECTS:
                    score = getattr(portrait.academic, subject)
                    if score and score < 60:
                        weak_subjects.append(self.SUBJECT_NAMES[subject])

                if weak_subjects:
                    summary["weaknesses"].append(f"薄弱科目：{', '.join(weak_subjects)}")

        # 学习态度评价
        if portrait.academic:
            if portrait.academic.learning_attitude >= 4:
                summary["strengths"].append("学习态度认真端正")
            elif portrait.academic.learning_attitude <= 2:
                summary["weaknesses"].append("学习态度需要改进")

        # 出勤评价
        if portrait.behavior:
            if portrait.behavior.attendance_rate < 95:
                summary["weaknesses"].append(f"出勤率较低 ({portrait.behavior.attendance_rate:.1f}%)")

        # 综合素质
        if portrait.behavior and portrait.behavior.clubs:
            summary["strengths"].append(f"积极参与社团活动：{portrait.behavior.clubs}")

        # 建议
        if "需努力" in tag_categories.get("学业水平", []):
            summary["suggestions"].append("建议加强基础知识学习，制定个性化辅导计划")

        if "偏科型" in tag_categories.get("学业水平", []):
            summary["suggestions"].append("存在偏科现象，建议均衡发展或发挥优势学科带头作用")

        if portrait.academic and portrait.academic.homework_completion <= 2:
            summary["suggestions"].append("作业完成情况不理想，建议加强课后监督")

        return summary

    def get_class_comparison(self, class_name: str, semester: str) -> Dict[str, Any]:
        """获取班级对比分析数据

        Returns:
            包含班级统计数据和可视化数据的字典
        """
        portraits = self.batch_analyze_class(class_name, semester)

        if not portraits:
            return {"error": "班级无数据"}

        # 收集各科成绩数据
        subject_scores = {s: [] for s in self.SUBJECTS}
        attendance_rates = []
        tag_distribution = {}

        for p in portraits:
            if p.academic:
                for subject in self.SUBJECTS:
                    score = getattr(p.academic, subject)
                    if score is not None:
                        subject_scores[subject].append(score)

            if p.behavior:
                attendance_rates.append(p.behavior.attendance_rate)

            for tag in p.tags:
                tag_distribution[tag.tag_name] = tag_distribution.get(tag.tag_name, 0) + 1

        # 计算统计数据
        result = {
            "student_count": len(portraits),
            "subject_averages": {
                self.SUBJECT_NAMES[s]: np.mean(scores) if scores else 0
                for s, scores in subject_scores.items() if scores
            },
            "attendance": {
                "average": np.mean(attendance_rates) if attendance_rates else 0,
                "full_attendance": sum(1 for r in attendance_rates if r == 100),
                "concerning": sum(1 for r in attendance_rates if r < 90)
            },
            "tag_distribution": dict(sorted(tag_distribution.items(),
                                           key=lambda x: x[1], reverse=True)[:10]),
            "score_distribution": self._calculate_score_distribution(subject_scores)
        }

        return result

    def _calculate_score_distribution(self, subject_scores: Dict[str, List[float]]) -> Dict[str, int]:
        """计算成绩分布"""
        all_scores = []
        for scores in subject_scores.values():
            all_scores.extend(scores)

        if not all_scores:
            return {}

        distribution = {
            "优秀(90-100)": sum(1 for s in all_scores if s >= 90),
            "良好(80-89)": sum(1 for s in all_scores if 80 <= s < 90),
            "中等(70-79)": sum(1 for s in all_scores if 70 <= s < 80),
            "及格(60-69)": sum(1 for s in all_scores if 60 <= s < 70),
            "不及格(<60)": sum(1 for s in all_scores if s < 60)
        }
        return distribution


# 全局分析器实例
analyzer = StudentAnalyzer()
