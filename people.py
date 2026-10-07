"""People in the SRMS: Person, Student and Teacher."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from academics import Course, Result


class Person:
    """A person with contact details. Parent class of Student and Teacher."""

    school_name: str = "City School"

    def __init__(self, name: str, email: str, phone: str) -> None:
        """Store the person's contact details."""
        self.name = name
        self.email = email
        self.phone = phone

    def __repr__(self) -> str:
        """Return a readable text for print()."""
        return f"{type(self).__name__}(name={self.name!r}, email={self.email!r})"

    def __eq__(self, other: object) -> bool:
        """Two people are equal when their name and email are the same."""
        if not isinstance(other, Person):
            return NotImplemented
        return self.name == other.name and self.email == other.email

    def __hash__(self) -> int:
        """Keep people usable in sets and dicts, matching __eq__."""
        return hash((self.name, self.email))

    @property
    def is_contactable(self) -> bool:
        """Return True when the person has an email."""
        return bool(self.email.strip())


class Student(Person):
    """A student who has an id and a list of results."""

    def __init__(
        self,
        student_id: int,
        name: str,
        email: str,
        phone: str,
        department: str = "",
        semester: int = 1,
    ) -> None:
        """Create a student. The parent __init__ sets name, email and phone."""
        super().__init__(name, email, phone)
        self.student_id = student_id
        self.department = department
        self.semester = semester
        self.results: list[Result] = []


class Teacher(Person):
    """A teacher who has an employee id and the courses they teach."""

    def __init__(self, employee_id: int, name: str, email: str, phone: str) -> None:
        """Create a teacher. The parent __init__ sets name, email and phone."""
        super().__init__(name, email, phone)
        self.employee_id = employee_id
        self.courses: list[Course] = []