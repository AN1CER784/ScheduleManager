from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models

from ScheduleManager import settings
from users.models.company import Company


class UserManager(DjangoUserManager):
    def _ensure_company(self, company):
        if company:
            return company
        company, _ = Company.objects.get_or_create(name="Default Company")
        return company

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields["company"] = self._ensure_company(extra_fields.get("company"))
        return super().create_user(username, email=email, password=password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields["company"] = self._ensure_company(extra_fields.get("company"))
        return super().create_superuser(username, email=email, password=password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        EMPLOYEE = "EMPLOYEE", "Employee"
        ADMIN = "ADMIN", "Company admin"

    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    language = models.CharField(max_length=10, default='en', choices=settings.LANGUAGES)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="users")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.EMPLOYEE)
    bonus_balance = models.IntegerField(default=0)

    class Meta:
        db_table = 'user'

    objects = UserManager()
