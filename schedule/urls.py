from django.urls import path
from .views import ScheduleView

app_name = 'schedule'

urlpatterns = [
    path('calendar/', ScheduleView.as_view(), name='calendar'),
]
