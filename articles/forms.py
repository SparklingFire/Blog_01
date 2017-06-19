from django import forms
from .models import Article
from django.core.exceptions import ObjectDoesNotExist


class ArticleForm(forms.Form):
    title = forms.CharField(help_text='', label='')
    text = forms.CharField(widget=forms.Textarea, help_text='', label='')

    def __init__(self, *args, **kwargs):
        try:
            self.article = kwargs.pop('article')
        except KeyError:
            self.article = None
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('The title is too short')
        try:
            Article.objects.get(title=title)
            if self.article is not None:
                pass
            else:
                raise forms.ValidationError('Статья с таким заголовком уже существует')
        except ObjectDoesNotExist:
            pass
        return title

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 1:
            raise forms.ValidationError('The text is too short')
        return text


class SearchForm(forms.Form):
    q = forms.CharField(
        label='',
        required=False
    )
