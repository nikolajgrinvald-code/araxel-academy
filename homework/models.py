from django.db import models
from users.models import User
from courses.models import Lesson


class HomeworkSubmission(models.Model):
    SUBMITTED = 'submitted'
    REVIEWING = 'reviewing'
    ACCEPTED = 'accepted'
    NEEDS_REVISION = 'needs_revision'
    STATUS_CHOICES = (
        (SUBMITTED, 'Отправлено'),
        (REVIEWING, 'На проверке'),
        (ACCEPTED, 'Принято'),
        (NEEDS_REVISION, 'Нужно доработать'),
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='homeworks',
        limit_choices_to={'role': User.ROLE_STUDENT},
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='submissions')
    answer_text = models.TextField('Ответ', blank=True)
    attached_file = models.FileField('Файл', upload_to='homework/submissions/', blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=SUBMITTED)
    admin_comment = models.TextField('Комментарий администратора', blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'lesson')
        ordering = ('-submitted_at',)

    def __str__(self):
        student = getattr(self, 'student_id', None)
        lesson = getattr(self, 'lesson_id', None)
        if student and lesson:
            try:
                return f'{self.student} -> {self.lesson}'
            except Exception:
                pass
        return f'HomeworkSubmission #{self.pk or "new"}'
