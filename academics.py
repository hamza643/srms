"""Academic classes of the SRMS: GradeCalculator, Course and Result."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from people import Student, Teacher


class GradeCalculator:
    """Turns marks into letter grades."""

    BANDS: tuple[tuple[float, str], ...] = ((85, "A"), (70, "B"), (55, "C"))
    LOWEST_GRADE: str = "F"

    @classmethod
    def grade_for(cls, average: float) -> str:
        """Return A, B, C or F for an average, using the class's band table."""
        for minimum, letter in cls.BANDS:
            if average >= minimum:
                return letter
        return cls.LOWEST_GRADE

    @staticmethod
    def is_valid_mark(mark: float) -> bool:
        """Return True if the mark is between 0 and 100."""
        return 0 <= mark <= 100


class Course:
    """A course with a code, a title, credit hours and an optional teacher."""

    def __init__(
        self,
        code: str,
        title: str,
        credit_hours: int,
        teacher: Teacher | None = None,
    ) -> None:
        """Create a course. The teacher can be assigned now or later."""
        self.code = code
        self.title = title
        self.credit_hours = credit_hours
        self.student_ids: list[int] = []
        self.teacher: Teacher | None = None
        if teacher is not None:
            self.assign_teacher(teacher)

    def assign_teacher(self, teacher: Teacher) -> None:
        """Set the teacher of this course and add it to the teacher's courses."""
        self.teacher = teacher
        if self not in teacher.courses:
            teacher.courses.append(self)

    def enroll(self, student: Student) -> bool:
        """Enroll a student. Return False if the student is already enrolled."""
        if student.student_id in self.student_ids:
            return False
        self.student_ids.append(student.student_id)
        return True

    def __repr__(self) -> str:
        """Return a readable text for print()."""
        return f"Course(code={self.code!r}, title={self.title!r})"


class Result:
    """The marks of one student in one course. It links the two together."""

    def __init__(self, student: Student, course: Course, marks: float) -> None:
        """Create a result. Marks outside 0 to 100 raise ValueError."""
        if not GradeCalculator.is_valid_mark(marks):
            raise ValueError("Grade must be between 0 and 100.")
        self.student = student
        self.course = course
        self.marks = marks

    def __repr__(self) -> str:
        """Return a readable text for print()."""
        return (
            f"Result(student={self.student.name!r}, "
            f"course={self.course.code!r}, marks={self.marks})"
        )