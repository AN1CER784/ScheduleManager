import numpy as np
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from tasks.models import Task


class TaskAutomatonReport:
    def __init__(self, user, period, start_date, end_date):
        self._user = user
        self._tasks = Task.objects.filter(project__user=self._user).select_related('project')
        self._start_date = start_date
        self._end_date = end_date
        self._period = period
        self._state_labels = {0: 'EMPTY', 1: 'IN_PROGRESS', 2: 'DONE', 3: 'LATE'}

    def _build_matrix(self):
        matrix = []
        for day_offset in range(self._period):
            day = self._start_date + timedelta(days=day_offset)
            row = []
            for t in self._tasks:
                if t.is_completed:
                    comp_dt = t.progress.updated_datetime
                    comp_date = timezone.localtime(comp_dt).date() if comp_dt else None
                    if comp_date == day:
                        row.append(2)
                    else:
                        continue
                else:
                    if t.due_datetime:
                        due_date = timezone.localtime(t.due_datetime).date()
                        if day > due_date:
                            row.append(3)
                        else:
                            row.append(1)
                    else:
                        row.append(1)
            matrix.append(row or [0])
        max_len = max(len(r) for r in matrix)
        return np.array([r + [0] * (max_len - len(r)) for r in matrix])

    @staticmethod
    def _filter_empty(matrix):
        """Вернёт одномерный массив всех ячеек ≠ EMPTY."""
        return matrix[matrix != 0]

    def _daily_metrics(self):
        report = []
        for i in range(self._period):
            day = self._start_date + timedelta(days=i)
            matrix_row = self._build_matrix()[i]
            cells = matrix_row[matrix_row != 0]
            total = len(cells)
            done = np.sum(cells == 2) if total else 0
            late = np.sum(cells == 3) if total else 0
            in_prog = np.sum(cells == 1) if total else 0
            report.append({
                'date': str(day),
                'total': int(total),
                'done': int(done),
                'late': int(late),
                'in_progress': int(in_prog),
                'done_pct': float(done / total * 100) if total else None,
                'late_pct': float(late / total * 100) if total else None,
                'in_progress_pct': float(in_prog / total * 100) if total else None,
            })
        return report

    def _trend_analysis(self):
        daily = self._daily_metrics()
        done_list = [d['done_pct'] or 0 for d in daily]
        mov_avg = []
        for i in range(len(done_list)):
            window = done_list[max(0, i - 2):i + 1]
            mov_avg.append(sum(window) / len(window))
        streak_done = streak_late = 0
        for entry in reversed(daily):
            if entry['done_pct'] is not None and entry['done_pct'] >= 50:
                streak_done += 1
                streak_late = 0
            elif entry['late_pct'] is not None and entry['late_pct'] > 50:
                streak_late += 1
                streak_done = 0
            else:
                break
        return {
            'daily_done_pct': done_list,
            'moving_avg_3d': mov_avg,
            'streak': {'done_days': streak_done, 'late_days': streak_late}
        }

    def _project_breakdown(self):
        data = {}
        for t in self._tasks:
            name = t.project.name
            rec = data.setdefault(name, {'total':0, 'done':0, 'late':0, 'in_progress':0})
            if t.is_completed:
                rec['done'] += 1
            else:
                if t.due_datetime:
                    if self._end_date > timezone.localtime(t.due_datetime).date():
                        rec['late'] += 1
                    else:
                        rec['in_progress'] += 1
                else:
                    rec['in_progress'] += 1
            rec['total'] += 1
        for rec in data.values():
            total = rec['total']
            rec['done_pct'] = rec['done']/total*100 if total else None
            rec['late_pct'] = rec['late']/total*100 if total else None
            rec['in_progress_pct'] = rec['in_progress']/total*100 if total else None
        return data

    @property
    def _get_matrix(self):
        matrix = self._build_matrix()
        return self._filter_empty(matrix)

    @property
    def _get_overall_report(self):
        mat = self._get_matrix
        done = np.sum(mat == 2) / mat.size * 100 if mat.size else 0
        late = np.sum(mat == 3) / mat.size * 100 if mat.size else 0
        in_prog = np.sum(mat == 1) / mat.size * 100 if mat.size else 0
        return {
            'overall': {'done_ratio': done, 'late_ratio': late, 'in_progress_ratio': in_prog},
            'forecast': self._forecast(done, late)
        }

    def generate_report(self):
        if self._period == 7:
            return self.generate_week_report()
        return self.generate_day_report()

    def generate_week_report(self):
        overall = self._get_overall_report
        return {**overall, 'daily': self._daily_metrics(), 'trend': self._trend_analysis(), 'by_project': self._project_breakdown()}

    def generate_day_report(self):
        overall = self._get_overall_report
        return {**overall, 'by_project': self._project_breakdown()}

    @staticmethod
    def _forecast(done, late):
        if done > 0.75:
            return _("Your productivity is excellent, keep it up")
        elif done > 0.5:
            return _("Your productivity is good, keep it up")
        elif late > 0.5:
            return _("Your productivity is low, you should pay attention")
        return _("Your productivity is not bad, but you can do better")