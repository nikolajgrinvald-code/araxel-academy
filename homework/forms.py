from django import forms
from .models import HomeworkSubmission


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = HomeworkSubmission
        fields = ['answer_text', 'attached_file']
        widgets = {
            'answer_text': forms.Textarea(attrs={'class': 'input', 'rows': 6, 'placeholder': 'Твой ответ...'}),
        }
