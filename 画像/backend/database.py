"""
数据库操作模块
封装 SQLite 数据库的增删改查操作
"""

import sqlite3
import os
import json
from typing import List, Optional, Dict, Any, Tuple
from contextlib import contextmanager
from models import (
    StudentBasic, StudentAcademic, StudentBehavior, StudentSurvey,
    StudentPortraitDoc, StudentTag, TABLE_SCHEMAS, detect_path
)


class Database:
    """数据库操作类"""

    def __init__(self, db_path: str = "../data/student_portrait.db"):
        """初始化数据库连接

        Args:
            db_path: 数据库文件路径，默认为项目根目录下的 data 文件夹
        """
        # 确保数据目录存在
        data_dir = os.path.dirname(db_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)

        self.db_path = db_path
        self._init_database()

    @contextmanager
    def _get_connection(self):
        """获取数据库连接的上下文管理器"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 使查询结果可以通过列名访问
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _init_database(self):
        """初始化数据库表结构"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for table_name, schema in TABLE_SCHEMAS.items():
                cursor.execute(schema)
                print(f"表 {table_name} 初始化完成")

    # ========== 学生基础信息操作 ==========

    def create_student(self, student: StudentBasic) -> int:
        """创建学生记录

        Returns:
            新创建的学生ID
        """
        # 自动检测课程路径
        if not student.path and student.class_name:
            student.path = detect_path(student.class_name)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (name, student_no, age, gender, class_name, grade, path,
                                    class_time, enrollment_date, contact, address, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (student.name, student.student_no, student.age, student.gender,
                  student.class_name, student.grade, student.path, student.class_time,
                  student.enrollment_date, student.contact, student.address,
                  student.created_at, student.updated_at))
            return cursor.lastrowid

    def batch_import_students(self, student_data_list: List[Dict]) -> int:
        """批量导入学生"""
        count = 0
        for data in student_data_list:
            try:
                student = StudentBasic(
                    name=data.get('name', ''),
                    gender=data.get('sex', ''),
                    class_name=data.get('class', ''),
                    class_time=data.get('time', ''),
                    path=detect_path(data.get('class', ''))
                )
                self.create_student(student)
                count += 1
            except Exception as e:
                print(f"导入学生 {data.get('name')} 失败: {e}")
        return count

    def get_student_by_id(self, student_id: int) -> Optional[StudentBasic]:
        """根据ID获取学生信息"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_student(row)
            return None

    def get_student_by_name(self, name: str) -> Optional[StudentBasic]:
        """根据姓名获取学生信息"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return self._row_to_student(row)
            return None

    def get_student_by_no(self, student_no: str) -> Optional[StudentBasic]:
        """根据学号获取学生信息"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE student_no = ?", (student_no,))
            row = cursor.fetchone()
            if row:
                return self._row_to_student(row)
            return None

    def get_all_students(self, class_name: str = None, grade: str = None, path: str = None) -> List[StudentBasic]:
        """获取所有学生列表，支持按班级、年级、路径筛选"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM students WHERE 1=1"
            params = []
            if class_name:
                query += " AND class_name = ?"
                params.append(class_name)
            if grade:
                query += " AND grade = ?"
                params.append(grade)
            if path:
                query += " AND path = ?"
                params.append(path)
            query += " ORDER BY created_at DESC"

            cursor.execute(query, params)
            return [self._row_to_student(row) for row in cursor.fetchall()]

    def update_student(self, student: StudentBasic) -> bool:
        """更新学生信息"""
        # 如果班级变了，重新检测路径
        old_student = self.get_student_by_id(student.id)
        if old_student and old_student.class_name != student.class_name:
            student.path = detect_path(student.class_name)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            from datetime import datetime
            student.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                UPDATE students SET name=?, age=?, gender=?, class_name=?, grade=?,
                                  path=?, class_time=?, enrollment_date=?, contact=?,
                                  address=?, updated_at=?
                WHERE id=?
            """, (student.name, student.age, student.gender, student.class_name,
                  student.grade, student.path, student.class_time, student.enrollment_date,
                  student.contact, student.address, student.updated_at, student.id))
            return cursor.rowcount > 0

    def delete_student(self, student_id: int) -> bool:
        """删除学生及其所有关联数据"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # 删除关联数据
            cursor.execute("DELETE FROM student_academic WHERE student_id = ?", (student_id,))
            cursor.execute("DELETE FROM student_behavior WHERE student_id = ?", (student_id,))
            cursor.execute("DELETE FROM student_survey WHERE student_id = ?", (student_id,))
            cursor.execute("DELETE FROM student_portrait_docs WHERE student_id = ?", (student_id,))
            cursor.execute("DELETE FROM student_tags WHERE student_id = ?", (student_id,))
            # 删除学生记录
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            return cursor.rowcount > 0

    def search_students(self, keyword: str) -> List[StudentBasic]:
        """根据关键词搜索学生（姓名、学号）"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            pattern = f"%{keyword}%"
            cursor.execute("""
                SELECT * FROM students
                WHERE name LIKE ? OR student_no LIKE ? OR class_name LIKE ?
                ORDER BY created_at DESC
            """, (pattern, pattern, pattern))
            return [self._row_to_student(row) for row in cursor.fetchall()]

    # ========== 学业信息操作 ==========

    def create_academic_record(self, record: StudentAcademic) -> int:
        """创建学业记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO student_academic (student_id, semester, chinese, math, english,
                    physics, chemistry, biology, history, geography, politics,
                    class_participation, homework_completion, learning_attitude, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (record.student_id, record.semester, record.chinese, record.math,
                  record.english, record.physics, record.chemistry, record.biology,
                  record.history, record.geography, record.politics,
                  record.class_participation, record.homework_completion,
                  record.learning_attitude, record.created_at))
            return cursor.lastrowid

    def get_academic_records(self, student_id: int, semester: str = None) -> List[StudentAcademic]:
        """获取学生的学业记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM student_academic WHERE student_id = ?"
            params = [student_id]
            if semester:
                query += " AND semester = ?"
                params.append(semester)
            query += " ORDER BY semester DESC"

            cursor.execute(query, params)
            return [self._row_to_academic(row) for row in cursor.fetchall()]

    def update_academic_record(self, record: StudentAcademic) -> bool:
        """更新学业记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE student_academic SET
                    chinese=?, math=?, english=?, physics=?, chemistry=?,
                    biology=?, history=?, geography=?, politics=?,
                    class_participation=?, homework_completion=?, learning_attitude=?
                WHERE id=?
            """, (record.chinese, record.math, record.english, record.physics,
                  record.chemistry, record.biology, record.history, record.geography,
                  record.politics, record.class_participation, record.homework_completion,
                  record.learning_attitude, record.id))
            return cursor.rowcount > 0

    # ========== 行为特征操作 ==========

    def create_behavior_record(self, record: StudentBehavior) -> int:
        """创建行为记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO student_behavior (student_id, semester, attendance_rate, late_count,
                    absence_count, clubs, activities, hobbies, talents, discipline_score,
                    teamwork_score, leadership_score, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (record.student_id, record.semester, record.attendance_rate,
                  record.late_count, record.absence_count, record.clubs, record.activities,
                  record.hobbies, record.talents, record.discipline_score,
                  record.teamwork_score, record.leadership_score, record.created_at))
            return cursor.lastrowid

    def get_behavior_records(self, student_id: int, semester: str = None) -> List[StudentBehavior]:
        """获取学生的行为记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM student_behavior WHERE student_id = ?"
            params = [student_id]
            if semester:
                query += " AND semester = ?"
                params.append(semester)
            query += " ORDER BY semester DESC"

            cursor.execute(query, params)
            return [self._row_to_behavior(row) for row in cursor.fetchall()]

    def update_behavior_record(self, record: StudentBehavior) -> bool:
        """更新行为记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE student_behavior SET
                    attendance_rate=?, late_count=?, absence_count=?, clubs=?,
                    activities=?, hobbies=?, talents=?, discipline_score=?,
                    teamwork_score=?, leadership_score=?
                WHERE id=?
            """, (record.attendance_rate, record.late_count, record.absence_count,
                  record.clubs, record.activities, record.hobbies, record.talents,
                  record.discipline_score, record.teamwork_score, record.leadership_score,
                  record.id))
            return cursor.rowcount > 0

    # ========== 问卷数据操作 ==========

    def get_or_create_survey(self, student_id: int, semester: str = None) -> StudentSurvey:
        """获取或创建问卷记录"""
        student = self.get_student_by_id(student_id)
        if not student:
            raise ValueError(f"未找到学生ID: {student_id}")

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM student_survey WHERE student_id = ? AND (semester = ? OR semester IS NULL)
                ORDER BY created_at DESC LIMIT 1
            """, (student_id, semester))
            row = cursor.fetchone()
            if row:
                return self._row_to_survey(row)

            # 创建新问卷记录
            survey = StudentSurvey(
                student_id=student_id,
                semester=semester or "",
                path=student.path
            )
            cursor.execute("""
                INSERT INTO student_survey (student_id, semester, path, progress, remark, is_completed, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (survey.student_id, survey.semester, survey.path, survey.progress,
                  survey.remark, 0, survey.created_at, survey.updated_at))
            survey.id = cursor.lastrowid
            return survey

    def update_survey_progress(self, student_id: int, progress: Dict, remark: str = "", semester: str = None) -> bool:
        """更新问卷进度"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            from datetime import datetime
            updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            progress_json = json.dumps(progress, ensure_ascii=False)

            # 检查是否有记录
            cursor.execute("SELECT id FROM student_survey WHERE student_id = ? AND (semester = ? OR semester IS NULL)",
                          (student_id, semester))
            row = cursor.fetchone()

            if row:
                cursor.execute("""
                    UPDATE student_survey SET progress=?, remark=?, updated_at=?
                    WHERE student_id=? AND (semester=? OR semester IS NULL)
                """, (progress_json, remark, updated_at, student_id, semester))
            else:
                student = self.get_student_by_id(student_id)
                cursor.execute("""
                    INSERT INTO student_survey (student_id, semester, path, progress, remark, is_completed, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (student_id, semester or "", student.path if student else "", progress_json, remark, 0, updated_at, updated_at))
            return cursor.rowcount > 0

    def mark_survey_complete(self, student_id: int, semester: str = None) -> bool:
        """标记问卷已完成"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE student_survey SET is_completed=1, updated_at=?
                WHERE student_id=? AND (semester=? OR semester IS NULL)
            """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), student_id, semester))
            return cursor.rowcount > 0

    def get_survey_by_student(self, student_id: int, semester: str = None) -> Optional[StudentSurvey]:
        """获取学生的问卷记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM student_survey WHERE student_id = ? AND (semester = ? OR semester IS NULL)
                ORDER BY created_at DESC LIMIT 1
            """, (student_id, semester))
            row = cursor.fetchone()
            if row:
                return self._row_to_survey(row)
            return None

    # ========== 画像报告操作 ==========

    def save_portrait_doc(self, doc: StudentPortraitDoc) -> int:
        """保存画像报告"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO student_portrait_docs (student_id, content, model_used, created_at)
                VALUES (?, ?, ?, ?)
            """, (doc.student_id, doc.content, doc.model_used, doc.created_at))
            return cursor.lastrowid

    def get_latest_portrait_doc(self, student_id: int) -> Optional[StudentPortraitDoc]:
        """获取学生最新的画像报告"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM student_portrait_docs WHERE student_id = ?
                ORDER BY created_at DESC LIMIT 1
            """, (student_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_portrait_doc(row)
            return None

    def get_all_portrait_docs(self, student_id: int) -> List[StudentPortraitDoc]:
        """获取学生的所有画像报告"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM student_portrait_docs WHERE student_id = ?
                ORDER BY created_at DESC
            """, (student_id,))
            return [self._row_to_portrait_doc(row) for row in cursor.fetchall()]

    # ========== 标签操作 ==========

    def create_tag(self, tag: StudentTag) -> int:
        """创建标签"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO student_tags (student_id, tag_name, tag_category, tag_value, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (tag.student_id, tag.tag_name, tag.tag_category, tag.tag_value, tag.created_at))
            return cursor.lastrowid

    def get_student_tags(self, student_id: int) -> List[StudentTag]:
        """获取学生的所有标签"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM student_tags WHERE student_id = ? ORDER BY tag_category
            """, (student_id,))
            return [self._row_to_tag(row) for row in cursor.fetchall()]

    def delete_student_tags(self, student_id: int) -> bool:
        """删除学生的所有标签（用于重新计算）"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM student_tags WHERE student_id = ?", (student_id,))
            return cursor.rowcount > 0

    # ========== 统计查询 ==========

    def get_class_statistics(self, class_name: str, semester: str) -> Dict[str, Any]:
        """获取班级统计数据"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 获取班级学生ID列表
            cursor.execute("SELECT id FROM students WHERE class_name = ?", (class_name,))
            student_ids = [row[0] for row in cursor.fetchall()]

            if not student_ids:
                return {"student_count": 0}

            stats = {"student_count": len(student_ids)}

            # 标签统计
            placeholders = ','.join('?' * len(student_ids))
            cursor.execute(f"""
                SELECT tag_name, COUNT(*) as count
                FROM student_tags
                WHERE student_id IN ({placeholders})
                GROUP BY tag_name
                ORDER BY count DESC
            """, student_ids)
            stats["tag_distribution"] = {row[0]: row[1] for row in cursor.fetchall()}

            # 问卷完成统计
            cursor.execute(f"""
                SELECT COUNT(*) FROM student_survey
                WHERE student_id IN ({placeholders}) AND is_completed = 1
            """, student_ids)
            stats["completed_surveys"] = cursor.fetchone()[0]

            return stats

    def get_grade_class_list(self) -> List[Dict[str, str]]:
        """获取所有年级班级列表"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT grade, class_name FROM students
                ORDER BY grade, class_name
            """)
            return [{"grade": row[0], "class_name": row[1]} for row in cursor.fetchall()]

    def get_path_distribution(self) -> Dict[str, int]:
        """获取课程路径分布统计"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT path, COUNT(*) FROM students GROUP BY path")
            return {row[0]: row[1] for row in cursor.fetchall()}

    # ========== 数据导入导出 ==========

    def export_all_data(self) -> Dict:
        """导出所有数据"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            data = {}

            for table in ['students', 'student_survey', 'student_portrait_docs']:
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                data[table] = [dict(row) for row in rows]

            return data

    def import_data(self, data: Dict) -> int:
        """导入数据"""
        count = 0
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 导入学生
            for student in data.get('students', []):
                try:
                    cursor.execute("""
                        INSERT OR REPLACE INTO students (id, name, student_no, age, gender, class_name, grade, path, class_time, enrollment_date, contact, address, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (student.get('id'), student.get('name'), student.get('student_no'),
                          student.get('age'), student.get('gender'), student.get('class_name'),
                          student.get('grade'), student.get('path'), student.get('class_time'),
                          student.get('enrollment_date'), student.get('contact'),
                          student.get('address'), student.get('created_at'), student.get('updated_at')))
                    count += 1
                except Exception as e:
                    print(f"导入学生失败: {e}")

        return count

    # ========== 辅助方法 ==========

    def _row_to_student(self, row: sqlite3.Row) -> StudentBasic:
        """将数据库行转换为StudentBasic对象"""
        return StudentBasic(
            id=row["id"],
            name=row["name"],
            student_no=row["student_no"] or "",
            age=row["age"] or 0,
            gender=row["gender"] or "",
            class_name=row["class_name"] or "",
            grade=row["grade"] or "",
            path=row["path"] or "kitten",
            class_time=row["class_time"] or "",
            enrollment_date=row["enrollment_date"] or "",
            contact=row["contact"] or "",
            address=row["address"] or "",
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    def _row_to_academic(self, row: sqlite3.Row) -> StudentAcademic:
        """将数据库行转换为StudentAcademic对象"""
        return StudentAcademic(
            id=row["id"],
            student_id=row["student_id"],
            semester=row["semester"],
            chinese=row["chinese"],
            math=row["math"],
            english=row["english"],
            physics=row["physics"],
            chemistry=row["chemistry"],
            biology=row["biology"],
            history=row["history"],
            geography=row["geography"],
            politics=row["politics"],
            class_participation=row["class_participation"],
            homework_completion=row["homework_completion"],
            learning_attitude=row["learning_attitude"],
            created_at=row["created_at"]
        )

    def _row_to_behavior(self, row: sqlite3.Row) -> StudentBehavior:
        """将数据库行转换为StudentBehavior对象"""
        return StudentBehavior(
            id=row["id"],
            student_id=row["student_id"],
            semester=row["semester"],
            attendance_rate=row["attendance_rate"],
            late_count=row["late_count"],
            absence_count=row["absence_count"],
            clubs=row["clubs"] or "",
            activities=row["activities"] or "",
            hobbies=row["hobbies"] or "",
            talents=row["talents"] or "",
            discipline_score=row["discipline_score"],
            teamwork_score=row["teamwork_score"],
            leadership_score=row["leadership_score"],
            created_at=row["created_at"]
        )

    def _row_to_survey(self, row: sqlite3.Row) -> StudentSurvey:
        """将数据库行转换为StudentSurvey对象"""
        progress = row["progress"] or "{}"
        try:
            progress = json.loads(progress)
        except:
            progress = {}

        return StudentSurvey(
            id=row["id"],
            student_id=row["student_id"],
            semester=row["semester"] or "",
            path=row["path"] or "",
            progress=json.dumps(progress, ensure_ascii=False) if isinstance(progress, dict) else progress,
            remark=row["remark"] or "",
            is_completed=bool(row["is_completed"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    def _row_to_portrait_doc(self, row: sqlite3.Row) -> StudentPortraitDoc:
        """将数据库行转换为StudentPortraitDoc对象"""
        return StudentPortraitDoc(
            id=row["id"],
            student_id=row["student_id"],
            content=row["content"] or "",
            model_used=row["model_used"] or "",
            created_at=row["created_at"]
        )

    def _row_to_tag(self, row: sqlite3.Row) -> StudentTag:
        """将数据库行转换为StudentTag对象"""
        return StudentTag(
            id=row["id"],
            student_id=row["student_id"],
            tag_name=row["tag_name"],
            tag_category=row["tag_category"] or "",
            tag_value=row["tag_value"],
            created_at=row["created_at"]
        )


# 全局数据库实例
db = Database()
