from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import FileResponse, Http404
import boto3
from users import views as user_views


@require_GET
def media_proxy(request, path):
    if not path:
        raise Http404()
    ext = path.lower().split('.')[-1]
    mime = 'application/octet-stream'
    if ext == 'mp4':
        mime = 'video/mp4'
    elif ext == 'pdf':
        mime = 'application/pdf'
    elif ext == 'pptx':
        mime = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    elif ext in ('jpg', 'jpeg'):
        mime = 'image/jpeg'
    elif ext == 'png':
        mime = 'image/png'

    client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=getattr(settings, 'AWS_S3_ENDPOINT_URL', None),
        region_name=getattr(settings, 'AWS_S3_REGION_NAME', 'us-east-1'),
    )
    try:
        obj = client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=path)
        return FileResponse(obj['Body'], content_type=obj.get('ContentType', mime))
    except Exception:
        raise Http404()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path('enrollments/', include('enrollments.urls')),
    path('homework/', include('homework.urls')),
    path('media/<path:path>', media_proxy, name='media_proxy'),
    path('', user_views.index, name='index'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
