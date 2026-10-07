"""Repository: the only place that reads or writes the JSON file."""

from __future__ import annotations

import json
from pathlib import Path
from types import TracebackType

from academics import Course, Result
from people import Student, Teacher


class Repository:
    """Holds all SRMS data. Loads it on entering a with block, saves it on leaving."""

    def __init__(self, path: Path) -> None:
        """Remember the file path and start with empty data."""
        self.path = path
        self.students: list[Student] = []
        self.teachers: list[Teacher] = []
        self.courses: list[Course] = []
        self.results: list[Result] = []
        self.warning: str | None = None

    def __enter__(self) -> Repository:
        """Load the data from the file and return the repository."""
        self.load()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Save the data, even if an exception happened. Return None so errors still propagate."""
        self.save()

    def load(self) -> None:
        """Read the JSON file. A missing file starts empty; a corrupt file is kept as .bak."""
        if not self.path.exists():
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self._build(json.load(f))
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            backup = self.path.with_name(self.path.name + ".bak")
            try:
                self.path.replace(backup)
                note = f" The old file was kept as {backup.name}."
            except OSError:
                note = " The old file could not be backed up."
            self.warning = "Data file is empty or corrupt." + note + " Starting with no data."
        except OSError as error:
            self.warning = f"Could not read data file: {error}"

    def _build(self, raw: dict) -> None:
        """Turn the loaded JSON into objects and link them together."""
        teachers = [
            Teacher(t["employee_id"], t["name"], t["email"], t["phone"])
            for t in raw["teachers"]
        ]
        students = [
            Student(s["student_id"], s["name"], s["email"], s["phone"],
                    s["department"], s["semester"])
            for s in raw["students"]
        ]
        teacher_by_id = {t.employee_id: t for t in teachers}
        student_by_id = {s.student_id: s for s in students}

        courses = []
        for c in raw["courses"]:
            course = Course(c["code"], c["title"], c["credit_hours"])
            if c["teacher_id"] is not None:
                course.assign_teacher(teacher_by_id[c["teacher_id"]])
            course.student_ids = list(c["student_ids"])
            courses.append(course)
        course_by_code = {c.code: c for c in courses}

        results = []
        for r in raw["results"]:
            student = student_by_id[r["student_id"]]
            result = Result(student, course_by_code[r["course_code"]], r["marks"])
            student.results.append(result)
            results.append(result)

        self.teachers, self.students = teachers, students
        self.courses, self.results = courses, results

    def save(self) -> None:
        """Write all data to the JSON file."""
        data = {
            "teachers": [
                {"employee_id": t.employee_id, "name": t.name,
                 "email": t.email, "phone": t.phone}
                for t in self.teachers
            ],
            "students": [
                {"student_id": s.student_id, "name": s.name, "email": s.email,
                 "phone": s.phone, "department": s.department, "semester": s.semester}
                for s in self.students
            ],
            "courses": [
                {"code": c.code, "title": c.title, "credit_hours": c.credit_hours,
                 "teacher_id": c.teacher.employee_id if c.teacher else None,
                 "student_ids": c.student_ids}
                for c in self.courses
            ],
            "results": [
                {"student_id": r.student.student_id, "course_code": r.course.code,
                 "marks": r.marks}
                for r in self.results
            ],
        }
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as error:
            self.warning = f"Could not save data file: {error}"

    def add_student(self, student: Student) -> None:
        """Add a student. Raise ValueError if the id is already used."""
        if self.find_student(student.student_id) is not None:
            raise ValueError(f"Student id {student.student_id} already exists.")
        self.students.append(student)

    def add_teacher(self, teacher: Teacher) -> None:
        """Add a teacher. Raise ValueError if the id is already used."""
        if self.find_teacher(teacher.employee_id) is not None:
            raise ValueError(f"Employee id {teacher.employee_id} already exists.")
        self.teachers.append(teacher)

    def add_course(self, course: Course) -> None:
        """Add a course. Raise ValueError if the code is already used."""
        if self.find_course(course.code) is not None:
            raise ValueError(f"Course code {course.code} already exists.")
        self.courses.append(course)

    def add_result(self, student: Student, course: Course, marks: float) -> Result:
        """Save marks for a student in a course, replacing any earlier result."""
        result = Result(student, course, marks)
        self.results = [
            r for r in self.results if not (r.student is student and r.course is course)
        ]
        student.results = [r for r in student.results if r.course is not course]
        self.results.append(result)
        student.results.append(result)
        return result

    def find_student(self, student_id: int) -> Student | None:
        """Return the student with this id, or None."""
        return next((s for s in self.students if s.student_id == student_id), None)

    def find_teacher(self, employee_id: int) -> Teacher | None:
        """Return the teacher with this id, or None."""
        return next((t for t in self.teachers if t.employee_id == employee_id), None)

    def find_course(self, code: str) -> Course | None:
        """Return the course with this code, or None."""
        return next((c for c in self.courses if c.code == code), None)

    def delete_student(self, student_id: int) -> bool:
        """Delete a student and their results. Return False if not found."""
        student = self.find_student(student_id)
        if student is None:
            return False
        self.students = [s for s in self.students if s is not student]
        self.results = [r for r in self.results if r.student is not student]
        for course in self.courses:
            if student_id in course.student_ids:
                course.student_ids.remove(student_id)
        return True

    def next_student_id(self) -> int:
        """Return the next free student id."""
        return max((s.student_id for s in self.students), default=0) + 1

    def next_employee_id(self) -> int:
        """Return the next free employee id."""
        return max((t.employee_id for t in self.teachers), default=0) + 1