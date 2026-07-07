from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from courses.models import Course
from .models import Enrollment


@login_required
def grant_access(request, course_pk):
    if not request.user.is_admin:
        return redirect('dashboard')
    course = get_object_or_404(Course, pk=course_pk)
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        if not student_id:
            messages.error(request, 'Укажи ученика.')
            return redirect('admin_courses')
        if Enrollment.objects.filter(student_id=student_id, course=course).exists():
            messages.error(request, 'Доступ уже выдан.')
            return redirect('admin_courses')
        Enrollment.objects.create(student_id=student_id, course=course)
        messages.success(request, 'Доступ выдан.')
        return redirect('admin_courses')
    return render(request, 'enrollments/grant.html', {'course': course})


@login_required
def revoke_access(request, pk):
    if not request.user.is_admin:
        return redirect('dashboard')
    obj = get_object_or_404(Enrollment, pk=pk)
    obj.delete()
    return redirect('admin_courses')


@login_required
def my_enrollments(request):
    if request.user.role == 'admin':
        return redirect('dashboard')
    enrollments = request.user.course_enrollments.select_related('course').all()
    return render(request, 'enrollments/my.html', {'enrollments': enrollments})
