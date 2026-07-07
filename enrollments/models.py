from django.db import models
from users.models import User
from courses.models import Course


class Enrollment(models.Model):
    ACTIVE = 'active'
    DISABLED = 'disabled'
    STATUS_CHOICES = ((ACTIVE, 'Активен'), (DISABLED, 'Отключён'))

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='course_enrollments',
        limit_choices_to={'role': User.ROLE_STUDENT},
    )
    access_status = models.CharField('Доступ', max_length=20, choices=STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student} -> {self.course}'
