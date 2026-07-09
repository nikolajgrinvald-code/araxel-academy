from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.http import FileResponse, Http404
from urllib.parse import unquote
import logging

logger = logging.getLogger('media_proxy')


def media_proxy(request, path):
    if not path:
        raise Http404()
    mime = 'application/octet-stream'
    lower = path.lower()
    if lower.endswith(('.mp4',)):
        mime = 'video/mp4'
    elif lower.endswith(('.pdf',)):
        mime = 'application/pdf'
    elif lower.endswith(('.pptx',)):
        mime = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    elif lower.endswith(('.jpg', '.jpeg')):
        mime = 'image/jpeg'
    elif lower.endswith(('.png',)):
        mime = 'image/png'

    object_path = unquote(path)
    try:
        import boto3
        client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=getattr(settings, 'AWS_S3_ENDPOINT_URL', None),
            region_name=getattr(settings, 'AWS_S3_REGION_NAME', 'us-east-1'),
        )
        obj = client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=object_path)
        return FileResponse(obj['Body'], content_type=obj.get('ContentType', mime))
    except Exception as e:
        raise Http404()


def link_lesson_6(request):
    from courses.models import Lesson, LessonFile
    import os
    secret = request.GET.get('secret', '')
    if secret != os.environ.get('DJANGO_SECRET_KEY', ''):
        return __import__('django.http').http.JsonResponse({'error': 'forbidden'}, status=403)
    lesson = Lesson.objects.filter(pk=6).first()
    if not lesson:
        return __import__('django.http').http.JsonResponse({'error': 'lesson not found'}, status=404)
    lesson.video_file.name = 'lessons/videos/Часть 2 Языкастик.mp4'
    lesson.save(update_fields=['video_file'])
    # Убрать старые файлы и добавить правильные
    LessonFile.objects.filter(lesson=lesson).exclude(file='lessons/files/Лекция 1.pptx').delete()
    LessonFile.objects.get_or_create(lesson=lesson, file='lessons/files/Лекция 1.pptx', defaults={'file_type': 'pptx'})
    return __import__('django.http').http.JsonResponse({'video': lesson.video_file.name, 'file': lesson.files.first().file.name if lesson.files.exists() else None})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path('enrollments/', include('enrollments.urls')),
    path('homework/', include('homework.urls')),
    path('media/<path:path>', media_proxy, name='media_proxy'),
    path('', user_views.index, name='index'),
    path('_debug/storage/', lambda request: __import__('django.http').http.JsonResponse({
        'DEFAULT_FILE_STORAGE': settings.DEFAULT_FILE_STORAGE,
        'MEDIA_URL': settings.MEDIA_URL,
        'AWS_ACCESS_KEY_ID': bool(getattr(settings, 'AWS_ACCESS_KEY_ID', None)),
        'AWS_STORAGE_BUCKET_NAME': settings.AWS_STORAGE_BUCKET_NAME,
        'AWS_S3_ENDPOINT_URL': settings.AWS_S3_ENDPOINT_URL,
        'AWS_S3_REGION_NAME': settings.AWS_S3_REGION_NAME,
    })),
    path('_admin/link_lesson_6/', link_lesson_6, name='link_lesson_6'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
