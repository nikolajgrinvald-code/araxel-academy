from django.urls import path
from . import views as v

urlpatterns = [
    path('lessons/<int:lesson_pk>/submit/', v.submit_homework, name='submit_homework'),
    path('my/', v.my_submissions, name='my_submissions'),
]
