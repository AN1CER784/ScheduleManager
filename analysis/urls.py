from django.urls import path
from .views import GenerateSummaryView, DeleteSummaryView

app_name = 'analysis'

urlpatterns = [
    path('generate-summary/', GenerateSummaryView.as_view(), name='generate-summary'),
    path('delete-summary', DeleteSummaryView.as_view(), name='delete-summary')

]
