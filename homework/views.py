from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from courses.models import Lesson
from .models import HomeworkSubmission
from .forms import HomeworkForm


@login_required
def submit_homework(request, lesson_pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    sub = HomeworkSubmission.objects.filter(student=request.user, lesson=lesson).first()
    if sub and sub.status in ('reviewing', 'accepted'):
        messages.info(request, 'Задание уже отправлено или проверено.')
        return redirect('lesson_detail', course_pk=lesson.course_id, lesson_pk=lesson.pk)
    if request.method == 'POST':
        form = HomeworkForm(request.POST, request.FILES, instance=sub)
        if form.is_valid():
            item = form.save(commit=False)
            item.student = request.user
            item.lesson = lesson
            item.status = 'submitted'
            item.save()
            messages.success(request, 'Ответ сохранён.')
            return redirect('lesson_detail', course_pk=lesson.course_id, lesson_pk=lesson.pk)
    else:
        form = HomeworkForm(instance=sub)
    return render(request, 'homework/submit.html', {'lesson': lesson, 'form': form, 'submission': sub})


@login_required
def my_submissions(request):
    items = HomeworkSubmission.objects.filter(student=request.user).select_related('lesson', 'lesson__course').all()
    return render(request, 'homework/my.html', {'items': items})
