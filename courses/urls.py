from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.course_list, name='course_list'),
    path('<int:pk>/', v.course_detail, name='course_detail'),
    path('<int:course_pk>/lessons/<int:lesson_pk>/', v.lesson_detail, name='lesson_detail'),
    path('admin/', v.admin_courses, name='admin_courses'),
    path('admin/courses/create/', v.admin_course_create, name='admin_course_create'),
    path('admin/courses/<int:pk>/edit/', v.admin_course_edit, name='admin_course_edit'),
    path('admin/courses/<int:pk>/delete/', v.admin_course_delete, name='admin_course_delete'),
    path('admin/lessons/', v.admin_lessons, name='admin_lessons'),
    path('admin/lessons/create/', v.admin_lesson_create, name='admin_lesson_create'),
    path('admin/lessons/<int:pk>/edit/', v.admin_lesson_edit, name='admin_lesson_edit'),
    path('admin/lessons/<int:pk>/delete/', v.admin_lesson_delete, name='admin_lesson_delete'),
    path('admin/lessons/<int:pk>/addfiles/', v.admin_lesson_addfiles, name='admin_lesson_addfiles'),
]
