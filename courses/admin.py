from django.contrib import admin
from .models import Course, Lesson, LessonFile


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at')
    search_fields = ('title',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'order_number', 'title', 'status')
    search_fields = ('title', 'course__title')


@admin.register(LessonFile)
class LessonFileAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'file_type', 'uploaded_at')
    search_fields = ('lesson__title',)
