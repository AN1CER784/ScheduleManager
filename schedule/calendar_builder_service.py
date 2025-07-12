import calendar
from datetime import datetime

from tasks.models import TaskQuerySet


class TaskCalendarBuilder:
    def __init__(self, tasks: TaskQuerySet):
        self._tasks = tasks
        self._min_date = None
        self._max_date = None
        self._cal = calendar.Calendar(firstweekday=0)
        self._months = []
        self._current_index = 1

    def build(self) -> None:
        if not self._tasks:
            self._handle_no_tasks()
        else:
            self._find_date_range()
            self._build_months()

    def _handle_no_tasks(self) -> None:
        self._months.append(self._cal.monthdatescalendar(datetime.now().year, datetime.now().month))

    def _find_date_range(self) -> None:
        for task in self._tasks:
            start = task.start_datetime.date()
            if task.due_datetime is not None:
                due = task.due_datetime.date()
            else:
                due = None
            if self._min_date is None or start < self._min_date:
                self._min_date = start
            if due and due < self._min_date:
                self._min_date = due
            if self._max_date is None or start > self._max_date:
                self._max_date = start
            if due and due > self._max_date:
                self._max_date = due

    def _build_months(self) -> None:
        year, month = self._min_date.year, self._min_date.month
        current_year, current_month = datetime.now().year, datetime.now().month
        while (year, month) <= (self._max_date.year, self._max_date.month):
            weeks = self._cal.monthdatescalendar(year, month)
            self._months.append(weeks)
            if current_month == month and current_year == year:
                self._current_index = len(self._months)

            if month == 12:
                year += 1
                month = 1
            else:
                month += 1

    @property
    def get_months_list(self) -> list[list[list[datetime.date]]]:
        return self._months

    @property
    def get_current_index(self) -> int:
        return self._current_index
