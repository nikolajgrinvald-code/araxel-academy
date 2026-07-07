from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.index, name='index'),
    path('register/', v.register_view, name='register'),
    path('login/', v.login_view, name='login'),
    path('logout/', v.logout_view, name='logout'),
    path('dashboard/', v.dashboard, name='dashboard'),
    path('admin/', v.admin_dashboard, name='admin_dashboard'),
    path('admin/students/', v.admin_students, name='admin_students'),
    path('admin/students/<int:pk>/', v.admin_student_detail, name='admin_student_detail'),
    path('assignments/', v.assignments_view, name='assignments'),
    path('assignments/<int:pk>/', v.assignment_detail_view, name='assignment_detail'),
]
