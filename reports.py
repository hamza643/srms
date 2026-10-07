"""Reports: builds text for result cards and class statistics. Never prints."""

from __future__ import annotations

from datetime import datetime

from academics import Course, GradeCalculator, Result
from people import Student


def _average(values: list[float]) -> float | None:
    """Return the average of the values, or None if the list is empty."""
    if not values:
        return None
    return sum(values) / len(values)


class ReportGenerator:
    """Builds report text. It returns strings and never prints."""

    def student_average(self, student: Student) -> float | None:
        """Return a student's average marks, or None if there are no results."""
        return _average([r.marks for r in student.results])

    def student_card(self, student: Student) -> str:
        """Return the result card of one student."""
        lines = [f"Result card: {student.name} (id {student.student_id})"]
        average = self.student_average(student)
        if average is None:
            lines.append("  No marks entered yet.")
            return "\n".join(lines)
        lines += [
            f"  {r.course.code:<8} {r.course.title:<18} {r.marks:>6}"
            for r in student.results
        ]
        lines.append(
            f"Average: {round(average, 2)}   Grade: {GradeCalculator.grade_for(average)}"
        )
        return "\n".join(lines)

    def course_report(self, course: Course, results: list[Result]) -> str:
        """Return the average, highest and lowest marks of one course."""
        header = f"{course.title} ({course.code})"
        marks = [(r.student.name, r.marks) for r in results if r.course is course]
        if not marks:
            return f"{header}\n  No marks yet."
        average = _average([mark for _, mark in marks])
        best = max(marks, key=lambda item: item[1])
        worst = min(marks, key=lambda item: item[1])
        return (
            f"{header}\n"
            f"  Average: {round(average, 2)}\n"
            f"  Highest: {best[0]} ({best[1]})\n"
            f"  Lowest:  {worst[0]} ({worst[1]})"
        )

    def class_statistics(
        self, students: list[Student], courses: list[Course], results: list[Result]
    ) -> str:
        """Return course statistics, the best and worst student, and grade bands."""
        lines = [f"Total students: {len(students)}", "Course statistics:"]
        if courses:
            lines += [self.course_report(course, results) for course in courses]
        else:
            lines.append("  (no courses yet)")

        graded = [
            (s, self.student_average(s))
            for s in students
            if self.student_average(s) is not None
        ]
        if graded:
            best = max(graded, key=lambda pair: pair[1])
            worst = min(graded, key=lambda pair: pair[1])
            lines.append(f"Highest: {best[0].name} ({round(best[1], 2)})")
            lines.append(f"Lowest:  {worst[0].name} ({round(worst[1], 2)})")
        else:
            lines.append("Highest/Lowest: n/a (no graded students)")

        bands = [GradeCalculator.grade_for(average) for _, average in graded]
        counts = "   ".join(f"{letter}: {bands.count(letter)}" for letter in "ABCF")
        lines.append(f"Grade bands:  {counts}")
        return "\n".join(lines)

    def full_report(
        self, students: list[Student], courses: list[Course], results: list[Result]
    ) -> str:
        """Return every result card plus the class statistics, with a timestamp."""
        lines = [f"Report generated: {datetime.now():%Y-%m-%d %H:%M:%S}", ""]
        for student in sorted(students, key=lambda s: s.name.lower()):
            lines += [self.student_card(student), ""]
        lines.append(self.class_statistics(students, courses, results))
        return "\n".join(lines)