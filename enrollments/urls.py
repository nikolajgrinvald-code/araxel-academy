from django.urls import path
from . import views as v

urlpatterns = [
    path('my/', v.my_enrollments, name='my_enrollments'),
    path('grant/<int:course_pk>/', v.grant_access, name='grant_access'),
    path('revoke/<int:pk>/', v.revoke_access, name='revoke_access'),
]
