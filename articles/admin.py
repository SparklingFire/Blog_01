from django.contrib import admin
from .models import (Article, Subscription)
from .forms import ArticleForm
from tag.models import Tag
from django.forms import modelformset_factory, BaseInlineFormSet
from django import forms
from utils_tags_cp.models import Image


class BaseTagFormSet(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
        tags = []
        for form in self.forms:
            tag = form.cleaned_data.get('tag')
            if tag in tags:
                raise forms.ValidationError('Тэг введен повторно')

            tags.append(tag)

            if not tag:
                raise forms.ValidationError('Create a tag')

            if len(tag.tag) < 2:
                raise forms.ValidationError('The tag is too short')


class TagInline(admin.StackedInline):
    model = Tag.article.through
    formset = modelformset_factory(Tag, fields='__all__', formset=BaseTagFormSet)
    extra = 0


class ArticleExtension(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'edited', 'get_hits', 'primary_key'
                    )
    inlines = [TagInline]

    def get_form(self, request, *args, **kwargs):
        """
        set an author by default
        """
        form = super().get_form(request, *args, **kwargs)
        form.base_fields['author'].initial = request.user
        return form


admin.site.register(Article, ArticleExtension)
admin.site.register(Subscription)
