from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from users.models import User
from homework.models import HomeworkSubmission
from enrollments.models import Enrollment
from courses.models import Course, Lesson
from django.db.models import Q


def index(request):
    if request.user.is_authenticated:
        target = 'admin_dashboard' if getattr(request.user, 'role', '') == 'admin' else 'dashboard'
        return redirect(target)
    return render(request, 'index.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        from .forms import RegisterForm
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация завершена.')
            return redirect('dashboard')
    else:
        from .forms import RegisterForm
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    target = 'admin_dashboard' if request.GET.get('admin') == '1' else 'dashboard'
    if request.user.is_authenticated:
        return redirect(target)
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            target = 'admin_dashboard' if user.role == 'admin' else 'dashboard'
            messages.success(request, 'Добро пожаловать.')
            return redirect(target)
        messages.error(request, 'Неверный email или пароль.')
    from .forms import RegisterForm, LoginForm
    form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Вы вышли из аккаунта.')
    return redirect('login')


@login_required
def dashboard(request):
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    student = request.user
    accesses = student.enrollments.select_related('course').all()
    return render(request, 'dashboard.html', {'student': student, 'accesses': accesses})


@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    ctx = {
        'students_count': User.objects.filter(role='student').count(),
        'courses_count': Course.objects.count(),
        'lessons_count': Lesson.objects.count(),
        'pending_count': HomeworkSubmission.objects.filter(status='reviewing').count(),
    }
    return render(request, 'admin/dashboard.html', ctx)


@login_required
def admin_students(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    q = request.GET.get('q', '').strip()
    students = User.objects.filter(role='student')
    if q:
        students = students.filter(Q(name__icontains=q) | Q(email__icontains=q))
    return render(request, 'admin/students.html', {'students': students, 'q': q})


@login_required
def admin_student_detail(request, pk):
    if not request.user.is_admin:
        return redirect('dashboard')
    student = get_object_or_404(User, pk=pk, role='student')
    enrollments = student.enrollments.select_related('course').all()
    submissions = HomeworkSubmission.objects.filter(student=student).select_related('lesson', 'lesson__course').order_by('-submitted_at')
    return render(request, 'admin/student_detail.html', {
        'student': student,
        'enrollments': enrollments,
        'submissions': submissions,
    })


@login_required
def assignments_view(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    items = HomeworkSubmission.objects.select_related('student', 'lesson', 'lesson__course').all().order_by('-submitted_at')
    return render(request, 'admin/assignments.html', {'items': items})


@login_required
def assignment_detail_view(request, pk):
    if not request.user.is_admin:
        return redirect('dashboard')
    item = get_object_or_404(HomeworkSubmission.objects.select_related('student', 'lesson', 'lesson__course'), pk=pk)
    from django.utils import timezone
    if request.method == 'POST':
        item.status = request.POST.get('status', 'reviewing')
        item.admin_comment = request.POST.get('admin_comment', '')
        item.reviewed_at = timezone.now()
        item.save()
        messages.success(request, 'Ответ обновлён.')
        return redirect('assignments')
    return render(request, 'admin/assignment_detail.html', {'item': item})
