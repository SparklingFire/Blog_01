from django import forms
from django.forms import (modelformset_factory, BaseModelFormSet)
from .models import Tag
import re


class TagForm(forms.Form):
    tag_list = forms.CharField()

    def clean(self):
        tag_list = self.cleaned_data.get('tag_list').split(';')
        print(tag_list)
        return self.cleaned_data
