"""The menu. This is the only file that calls print() or input()."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, TypeVar

from academics import Course
from people import Student, Teacher
from reports import ReportGenerator
from repository import Repository
from validators import (
    validate_email,
    validate_id,
    validate_marks,
    validate_required,
    validate_whole,
)

DATA_FILE = Path(__file__).parent / "data" / "srms.json"
REPORT_FILE = Path(__file__).parent / "report.txt"

T = TypeVar("T")

MENU = (
    "Add student",
    "View students",
    "Update student",
    "Delete student",
    "Add teacher",
    "Add course",
    "Assign teacher to course",
    "Enroll student in course",
    "Enter marks",
    "Show result card",
    "Class statistics",
    "Search students",
    "Export report",
    "Exit",
)


def ask(prompt: str, validator: Callable[[str], T]) -> T:
    """Keep asking until the validator accepts the input."""
    while True:
        try:
            return validator(input(prompt))
        except ValueError as error:
            print(f"  x {error} Try again.")


def show_menu() -> None:
    """Print the numbered menu."""
    print("\n=== Student Result Management System ===")
    for number, label in enumerate(MENU, start=1):
        print(f"{number}. {label}")


def pick_student(repo: Repository) -> Student | None:
    """Ask for a student id and return the student, or None if not found."""
    student = repo.find_student(ask("Student id: ", validate_id))
    if student is None:
        print("No student with that id.")
    return student


def pick_teacher(repo: Repository) -> Teacher | None:
    """Ask for an employee id and return the teacher, or None if not found."""
    teacher = repo.find_teacher(ask("Employee id: ", validate_id))
    if teacher is None:
        print("No teacher with that id.")
    return teacher


def pick_course(repo: Repository) -> Course | None:
    """Ask for a course code and return the course, or None if not found."""
    course = repo.find_course(input("Course code: ").strip().upper())
    if course is None:
        print("No course with that code.")
    return course


def print_students(students: list[Student]) -> None:
    """Print students in an aligned table, sorted by name."""
    print(f"{'ID':>3}  {'Name':<18}  {'Email':<24}  {'Department':<12}  {'Sem':>3}")
    for s in sorted(students, key=lambda s: s.name.lower()):
        print(
            f"{s.student_id:>3}  {s.name:<18}  {s.email:<24}  "
            f"{s.department:<12}  {s.semester:>3}"
        )


def add_student(repo: Repository) -> None:
    """Ask for a new student's details and add the student."""
    name = ask("Name: ", lambda t: validate_required(t, "Name"))
    email = ask("Email: ", validate_email)
    phone = input("Phone: ").strip()
    department = input("Department: ").strip()
    semester = ask("Semester (1-12): ", lambda t: validate_whole(t, 1, 12, "Semester"))
    student = Student(repo.next_student_id(), name, email, phone, department, semester)
    repo.add_student(student)
    print(f"Student added with id {student.student_id}.")


def view_students(repo: Repository) -> None:
    """Print all students, or a message if there are none."""
    if not repo.students:
        print("No students yet.")
        return
    print_students(repo.students)


def update_student(repo: Repository) -> None:
    """Change one detail of a student."""
    student = pick_student(repo)
    if student is None:
        return
    print("1. Email  2. Phone  3. Department  4. Semester")
    choice = input("What do you want to change? ").strip()
    if choice == "1":
        student.email = ask("New email: ", validate_email)
    elif choice == "2":
        student.phone = input("New phone: ").strip()
    elif choice == "3":
        student.department = input("New department: ").strip()
    elif choice == "4":
        student.semester = ask(
            "New semester (1-12): ", lambda t: validate_whole(t, 1, 12, "Semester")
        )
    else:
        print("Please choose 1 to 4.")
        return
    print("Student updated.")


def delete_student(repo: Repository) -> None:
    """Delete a student after confirmation."""
    student = pick_student(repo)
    if student is None:
        return
    answer = input(f"Delete {student.name}? (y/n): ").strip().lower()
    if answer != "y":
        print("Cancelled.")
        return
    repo.delete_student(student.student_id)
    print("Student deleted.")


def add_teacher(repo: Repository) -> None:
    """Ask for a new teacher's details and add the teacher."""
    name = ask("Name: ", lambda t: validate_required(t, "Name"))
    email = ask("Email: ", validate_email)
    phone = input("Phone: ").strip()
    teacher = Teacher(repo.next_employee_id(), name, email, phone)
    repo.add_teacher(teacher)
    print(f"Teacher added with employee id {teacher.employee_id}.")


def add_course(repo: Repository) -> None:
    """Ask for a new course's details and add the course."""
    code = ask("Course code: ", lambda t: validate_required(t, "Code").upper())
    title = ask("Title: ", lambda t: validate_required(t, "Title"))
    hours = ask("Credit hours (1-6): ", lambda t: validate_whole(t, 1, 6, "Credit hours"))
    try:
        repo.add_course(Course(code, title, hours))
    except ValueError as error:
        print(error)
        return
    print("Course added.")


def assign_teacher(repo: Repository) -> None:
    """Assign a teacher to a course."""
    course = pick_course(repo)
    if course is None:
        return
    teacher = pick_teacher(repo)
    if teacher is None:
        return
    course.assign_teacher(teacher)
    print(f"{teacher.name} now teaches {course.title}.")


def enroll_student(repo: Repository) -> None:
    """Enroll a student in a course."""
    student = pick_student(repo)
    if student is None:
        return
    course = pick_course(repo)
    if course is None:
        return
    if course.enroll(student):
        print(f"{student.name} enrolled in {course.title}.")
    else:
        print("Student is already enrolled in this course.")


def enter_marks(repo: Repository) -> None:
    """Enter marks for an enrolled student in a course."""
    student = pick_student(repo)
    if student is None:
        return
    course = pick_course(repo)
    if course is None:
        return
    if student.student_id not in course.student_ids:
        print("Student is not enrolled in this course. Enroll first.")
        return
    marks = ask("Marks (0-100): ", validate_marks)
    repo.add_result(student, course, marks)
    print("Marks saved.")


def show_result_card(repo: Repository, reports: ReportGenerator) -> None:
    """Print the result card of one student."""
    student = pick_student(repo)
    if student is not None:
        print(reports.student_card(student))


def show_statistics(repo: Repository, reports: ReportGenerator) -> None:
    """Print the class statistics."""
    print("\n=== Class statistics ===")
    print(reports.class_statistics(repo.students, repo.courses, repo.results))


def search_students(repo: Repository) -> None:
    """Search students by part of the name, or by exact id."""
    query = input("Search by name or id: ").strip().lower()
    if not query:
        print("Nothing to search for.")
        return
    matches = [
        s for s in repo.students
        if query in s.name.lower() or query == str(s.student_id)
    ]
    if matches:
        print_students(matches)
    else:
        print("No students found.")


def export_report(repo: Repository, reports: ReportGenerator) -> None:
    """Write the full report to report.txt."""
    text = reports.full_report(repo.students, repo.courses, repo.results)
    try:
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    except OSError as error:
        print(f"Could not write report: {error}")
        return
    print("Report saved to report.txt.")


def main() -> None:
    """Open the repository, run the menu, and save everything on exit."""
    reports = ReportGenerator()
    with Repository(DATA_FILE) as repo:
        if repo.warning:
            print(f"Warning: {repo.warning}")
        actions: dict[str, Callable[[], None]] = {
            "1": lambda: add_student(repo),
            "2": lambda: view_students(repo),
            "3": lambda: update_student(repo),
            "4": lambda: delete_student(repo),
            "5": lambda: add_teacher(repo),
            "6": lambda: add_course(repo),
            "7": lambda: assign_teacher(repo),
            "8": lambda: enroll_student(repo),
            "9": lambda: enter_marks(repo),
            "10": lambda: show_result_card(repo, reports),
            "11": lambda: show_statistics(repo, reports),
            "12": lambda: search_students(repo),
            "13": lambda: export_report(repo, reports),
        }
        while True:
            show_menu()
            choice = input("\nSelect an option: ").strip()
            if choice == "14":
                print("Goodbye.")
                break
            action = actions.get(choice)
            if action is None:
                print("Please choose a number from 1 to 14.")
            else:
                action()


if __name__ == "__main__":
    main()