from django import forms
from .models import Message


class SendMessageForm(forms.Form):
    title = forms.CharField(label='заголовок', error_messages={'required': ''})
    text = forms.CharField(label='текст', widget=forms.Textarea, error_messages={'required': ''})

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title is None:
            raise forms.ValidationError('введите заголовок')
        return title

    def clean_text(self):
        text = self.cleaned_data.get('text')
        return text
