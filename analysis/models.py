from django.db import models


class AnalysisSummary(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    summary = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"AnalysisSummary {self.id}"
