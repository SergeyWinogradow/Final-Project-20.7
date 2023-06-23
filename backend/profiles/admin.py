from django.contrib import admin

from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Профиль пользователя
    list_display = ("user", "nike", "first_name", "last_name", "phone", "email_two")
    prepopulated_fields = {"slug": ("user",)}
    # фильтр
    list_filter = ("user", "nike")
    # поиск
    # search_fields = ("user", "nike", "first_name", "last_name", "phone", "email_two")