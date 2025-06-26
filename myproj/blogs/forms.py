from django import forms 
from .models import Comment , Blog
from django.utils.translation import gettext_lazy as _
from django.forms import RadioSelect

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text' : _('text'),
        }

class BlogForm(forms.ModelForm):
    category_name = forms.CharField(label=_('Category'), required=False)

    class Meta:
        model = Blog
        fields = ['title','body','banner',]
        labels = {
            'title' : _('title'),
            'body' : _('body'),
            'banner' : _('banner'),
        }