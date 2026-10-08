# SRMS: 

A command-line app that manages students, teachers, courses and marks. Data is saved in a JSON file, so it is still there the next time you run it. It is written with classes, to practise object-oriented Python.

## How to run

 need Python and Git. On Windows PowerShell:

```powershell
git clone https://github.com/hamza643/srms.git
cd srms
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python main.py
```

 The `data/` folder and `data/srms.json` are created automatically on the first run.

To run the tests:

```powershell
pip install pytest
python -m pytest -v
```

## What it does

- Add, view, update and delete students
- Add teachers and courses, and assign a teacher to a course
- Enroll a student in a course
- Enter marks for an enrolled student in a course (0 to 100)
- Show a result card for one student
- Show class statistics: average, highest and lowest per course, the best and worst student, and how many students are in each grade band (A, B, C, F)
- Search students by name or id
- Export a full report with a timestamp to `report.txt`

Bad input is rejected and the app asks again. If `data/srms.json` is corrupt, it is renamed to `srms.json.bak` and the app starts empty, so no data is lost.

## Files

- `people.py`: `Person`, `Student` and `Teacher`
- `academics.py`: `Course`, `Result` and `GradeCalculator`
- `repository.py`: `Repository`, the only class that reads or writes the JSON file
- `reports.py`: `ReportGenerator`, which builds report text and never prints
- `validators.py`: input checks used by the menu
- `main.py`: the menu, the only file that calls `print()` or `input()`
- `tests/test_grades.py`: pytest tests for `GradeCalculator` and `Result`


## Classmethod and staticmethod

- `GradeCalculator.grade_for` is a classmethod because it uses the class's own grade table (`cls.BANDS`).
- `GradeCalculator.is_valid_mark` is a staticmethod because it only checks a number, so it needs neither the class nor an object.

## The __del__ experiment

I added a `__del__` method to `Student` that printed a message. When I deleted a student with `del`, the message printed right at that line, before the next line ran. When two names pointed to the same student, `del a` printed nothing, and the message only came when the last name (`b`) was deleted. When I stopped the program abruptly with `os._exit(0)`, the message never printed at all.

I would not trust `__del__` to save student data, because Python decides when it runs, it may run late, and it may not run at all if the program stops suddenly.
 `Repository` is a context manager instead, because `__exit__` always runs when the `with` block ends, even if an error happened inside it, so the data is saved at a known moment. 
I removed `__del__` after the experiment.

## Differences from my design document

- I added `validators.py` to keep the menu's input checks out of `main.py`.
- I added `pytest.ini` so the tests in `tests/` can import `academics` and `people` from the project folder.

## Things to know

- I built this on Python 3.9, so every module starts with `from __future__ import annotations`. I have not tested it on 3.12.

