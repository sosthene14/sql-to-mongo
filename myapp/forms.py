# myapp/forms.py

from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'content': forms.Textarea(attrs={'class': 'textarea'}),
        }
