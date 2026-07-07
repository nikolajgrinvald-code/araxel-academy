from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Course, Lesson, LessonFile
from .forms import CourseForm, LessonForm
from users.models import User
from enrollments.models import Enrollment


def course_list(request):
    q = request.GET.get('q', '').strip()
    courses = Course.objects.all()
    if q:
        courses = courses.filter(Q(title__icontains=q) | Q(description__icontains=q))
    return render(request, 'courses/student_courses.html', {'courses': courses, 'q': q})


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    lessons = course.lessons.select_related('course').all()
    return render(request, 'courses/course_detail.html', {'course': course, 'lessons': lessons})


@login_required
def lesson_detail(request, course_pk, lesson_pk):
    course = get_object_or_404(Course, pk=course_pk)
    lesson = get_object_or_404(Lesson, pk=lesson_pk, course=course)
    return render(request, 'courses/lesson_detail.html', {'course': course, 'lesson': lesson})


@login_required
def admin_courses(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    q = request.GET.get('q', '').strip()
    courses = Course.objects.all()
    if q:
        courses = courses.filter(Q(title__icontains=q) | Q(description__icontains=q))
    return render(request, 'admin/course_list.html', {'courses': courses, 'q': q})


@login_required
def admin_course_create(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    form = CourseForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        course = form.save()
        _sync_students(course, form.cleaned_data.get('students'))
        return redirect('admin_courses')
    return render(request, 'admin/course_form.html', {'form': form})


@login_required
def admin_course_edit(request, pk):
    if not request.user.is_admin:
        return redirect('dashboard')
    obj = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        course = form.save()
        _sync_students(course, form.cleaned_data.get('students'))
        return redirect('admin_courses')
    return render(request, 'admin/course_form.html', {'form': form, 'obj': obj})


@login_required
def admin_course_delete(request, pk):
    if not request.user.is_admin:
        return redirect('dashboard')
    obj = get_object_or_404(Course, pk=pk)
    obj.delete()
    return redirect('admin_courses')


@login_required
def admin_lessons(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    lessons = Lesson.objects.select_related('course').all()
    return render(request, 'admin/lesson_list.html', {'lessons': lessons})


@login_required
def admin_lesson_create(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    form = LessonForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('admin_lessons')
    return render(request, 'admin/lesson_form.html', {'form': form})


@login_required
def admin_lesson_edit(request, pk):
    if not request.user.is_admin:
        return redirect('dashboard')
    obj = get_object_or_404(Lesson, pk=pk)
    form = LessonForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST':
        remove_files = request.POST.getlist('remove_lesson_file')
        LessonFile.objects.filter(pk__in=remove_files, lesson=obj).delete()
    if form.is_valid():
        form.save()
        return redirect('admin_lessons')
    return render(request, 'admin/lesson_form.html', {'form': form, 'obj': obj})


@login_required
def admin_lesson_delete(request, pk):
    if not request.user.is_admin:
        return redirect('dashboard')
    obj = get_object_or_404(Lesson, pk=pk)
    obj.delete()
    return redirect('admin_lessons')


@login_required
def admin_lesson_addfiles(request, pk):
    if not request.user.is_admin or request.method != 'POST':
        return redirect('lesson_detail', course_pk=pk, lesson_pk=pk)
    lesson = get_object_or_404(Lesson, pk=pk)
    for f in request.FILES.getlist('lesson_files'):
        LessonFile.objects.create(lesson=lesson, file=f)
    return redirect('lesson_detail', course_pk=lesson.course_id, lesson_pk=lesson.pk)


def _sync_students(course, students):
    if students is None:
        return
    current = set(Enrollment.objects.filter(course=course).values_list('student_id', flat=True))
    target = set(user.pk for user in students)
    to_remove = current - target
    to_add = target - current
    Enrollment.objects.filter(course=course, student_id__in=to_remove).delete()
    Enrollment.objects.bulk_create([Enrollment(student_id=student_id, course=course) for student_id in to_add])
