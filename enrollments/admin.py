from django.contrib import admin
from .models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'access_status', 'created_at')
    list_filter = ('access_status',)
    search_fields = ('student__email', 'course__title')
