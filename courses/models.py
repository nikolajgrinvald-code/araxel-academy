from django.db import models


class Course(models.Model):
    ACTIVE = 'active'
    HIDDEN = 'hidden'
    STATUS_CHOICES = ((ACTIVE, 'Активен'), (HIDDEN, 'Скрыт'))

    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    cover_image = models.ImageField('Обложка', upload_to='course-covers/', blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    PUBLISHED = 'published'
    DRAFT = 'draft'
    STATUS_CHOICES = ((PUBLISHED, 'Опубликован'), (DRAFT, 'Черновик'))

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')
    order_number = models.PositiveIntegerField('Номер урока', default=1)
    title = models.CharField('Название', max_length=200)
    short_description = models.CharField('Краткое описание', max_length=255, blank=True)
    content = models.TextField('Содержание', blank=True)
    video_url = models.URLField('Видео URL', blank=True)
    video_file = models.FileField('Видео/аудио файл', upload_to='lessons/videos/', blank=True)
    homework_text = models.TextField('Домашнее задание', blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order_number',)
        unique_together = ('course', 'order_number')

    def __str__(self):
        return f'{self.course} · Урок {self.order_number}'


class LessonFile(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='files', verbose_name='Урок')
    file = models.FileField('Файл', upload_to='lessons/files/')
    file_type = models.CharField('Тип', max_length=50, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
