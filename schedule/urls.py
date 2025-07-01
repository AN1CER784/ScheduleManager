from django.urls import path
from .views import ScheduleCalendarView

app_name = 'schedule'

urlpatterns = [
    path('calendar/', ScheduleCalendarView.as_view(), name='calendar'),
]