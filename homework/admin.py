from django.contrib import admin
from .models import HomeworkSubmission


@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id',)
