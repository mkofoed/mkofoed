from django import forms
from markdownx.fields import MarkdownxFormField

from .models import Post


class PostCreateForm(forms.ModelForm):
    content = MarkdownxFormField()

    class Meta:
        model = Post
        exclude = ['date_created', 'date_modified', 'slug', 'author']
        help_texts = {
            'title': 'Title',
            'summary': 'Summary',
            'published': 'Published'}


class PostUpdateForm(forms.ModelForm):
    content = MarkdownxFormField()

    class Meta:
        model = Post
        exclude = ['date_created', 'date_modified', 'slug', 'author']
        help_texts = {
            'title': 'Title',
            'summary': 'Summary',
            'published': 'Published'}
