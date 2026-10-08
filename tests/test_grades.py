"""Tests for GradeCalculator and Result."""

from __future__ import annotations

import pytest

from academics import Course, GradeCalculator, Result
from people import Student


@pytest.fixture
def student() -> Student:
    """Return a sample student."""
    return Student(1, "Ali", "ali@example.com", "0300")


@pytest.fixture
def course() -> Course:
    """Return a sample course."""
    return Course("M1", "Math", 3)


def test_grade_a_boundary() -> None:
    """85 is the lowest A, and 84.99 is still a B."""
    assert GradeCalculator.grade_for(85) == "A"
    assert GradeCalculator.grade_for(84.99) == "B"


def test_grade_b_boundary() -> None:
    """70 is the lowest B, and 69.99 is still a C."""
    assert GradeCalculator.grade_for(70) == "B"
    assert GradeCalculator.grade_for(69.99) == "C"


def test_grade_c_boundary() -> None:
    """55 is the lowest C, and 54.99 is an F."""
    assert GradeCalculator.grade_for(55) == "C"
    assert GradeCalculator.grade_for(54.99) == "F"


def test_grade_for_sample_students() -> None:
    """The sample averages from the practical give the expected grades."""
    assert GradeCalculator.grade_for(81.0) == "B"
    assert GradeCalculator.grade_for(90.5) == "A"
    assert GradeCalculator.grade_for(47.0) == "F"


def test_valid_marks_include_the_edges() -> None:
    """0 and 100 are valid marks."""
    assert GradeCalculator.is_valid_mark(0) is True
    assert GradeCalculator.is_valid_mark(100) is True


def test_invalid_marks_outside_the_range() -> None:
    """-1 and 101 are not valid marks."""
    assert GradeCalculator.is_valid_mark(-1) is False
    assert GradeCalculator.is_valid_mark(101) is False


def test_result_rejects_marks_above_100(student: Student, course: Course) -> None:
    """A Result with 101 marks raises ValueError."""
    with pytest.raises(ValueError, match="between 0 and 100"):
        Result(student, course, 101)


def test_result_rejects_negative_marks(student: Student, course: Course) -> None:
    """A Result with -1 marks raises ValueError."""
    with pytest.raises(ValueError, match="between 0 and 100"):
        Result(student, course, -1)


def test_result_keeps_valid_marks(student: Student, course: Course) -> None:
    """A Result keeps marks of 0, 88 and 100 as they are."""
    for marks in (0, 88, 100):
        assert Result(student, course, marks).marks == marks