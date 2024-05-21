from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'cols': 80, 'rows': 9,
                                          'style': 'resize:none',
                                          'class': 'form-control',
                                          'placeholder':
                                              'Только авторизованные пользователи могут оставлять комментарии.'})
        }
