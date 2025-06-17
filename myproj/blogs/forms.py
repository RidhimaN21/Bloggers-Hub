from django import forms 
from .models import Comment , Blog
from django.utils.translation import gettext_lazy as _

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text' : _('text'),
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','body','slug','banner']
        labels = {
            'title' : _('title'),
            'body' : _('body'),
            'slug' : _('slug'),
            'banner' : _('banner'),
        }