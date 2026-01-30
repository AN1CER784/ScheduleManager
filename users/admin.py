from django.contrib import admin
from .models import User, Company, BonusTransaction

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'company', 'role', 'bonus_balance', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('company', 'role', 'is_active', 'is_staff', 'is_superuser')
    ordering = ('-date_joined',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(BonusTransaction)
class BonusTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'points', 'reason', 'created_at')
    list_filter = ('points', 'created_at')
