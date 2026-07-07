from django.contrib import admin
from .models import HomeworkSubmission


@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'status', 'submitted_at', 'reviewed_at')
    list_filter = ('status', 'reviewed_at')
    search_fields = ('student__email', 'lesson__title')
