from django import forms
from .models import Course, Lesson, LessonFile
from users.models import User


class CourseForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'input'}),
    )

    class Meta:
        model = Course
        fields = ['title', 'description', 'cover_image', 'status', 'students']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'input', 'rows': 5}),
        }


class LessonForm(forms.ModelForm):
    extra_files = forms.FileField(
        label='Дополнительные материалы (PDF, презентации и др.)',
        required=False,
        widget=forms.FileInput(attrs={'class': 'input'}),
    )

    class Meta:
        model = Lesson
        fields = ['course', 'order_number', 'title', 'short_description', 'content', 'video_url', 'video_file', 'homework_text', 'status', 'extra_files']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'content': forms.Textarea(attrs={'class': 'input', 'rows': 6}),
            'homework_text': forms.Textarea(attrs={'class': 'input', 'rows': 4}),
        }

    def save(self, commit=True):
        lesson = super().save(commit=commit)
        files = self.files.getlist('extra_files')
        for f in files:
            LessonFile.objects.create(lesson=lesson, file=f)
        return lesson
