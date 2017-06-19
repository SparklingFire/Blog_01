from django import forms
from .models import Comment
import datetime
from django.utils.safestring import mark_safe


class CommentForm(forms.ModelForm):
    parent = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'parent'}),
                             required=False)

    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'rows': 5, 'cols': 5})}

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session')
        self.article = kwargs.pop('article')
        super().__init__(*args, **kwargs)

    def clean(self):
        text = self.cleaned_data.get('text')
        if text is None:
            raise forms.ValidationError(' Вы не ввели текст сообщения. ')
        if len(text) < 5:
            raise forms.ValidationError('Сообщение слишком короткое.')
        try:
            if abs(Comment.objects.filter(session=self.session).last().created -
                   datetime.datetime.now(datetime.timezone.utc)) <= datetime.timedelta(seconds=20):
                raise forms.ValidationError('Вы отправляете сообщения слишком быстро')
        except:
            pass
        return self.cleaned_data
