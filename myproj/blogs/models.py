from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _ 
from django.conf import settings

class Blog(models.Model):
    title = models.CharField(_("Title"), max_length=60)
    body = models.TextField(_("Body"))
    slug = models.SlugField(_("Slug"), unique=True, blank=True)
    date = models.DateTimeField(_("Date"), auto_now_add=True)
    banner = models.ImageField(_("Banner"), default="fallback.png", blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,blank=True, verbose_name=_("Author"))
    upvoted_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='upvoted_blogs', verbose_name=_("Upvoted by"))

    def total_upvotes(self):
        return self.upvoted_by.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE, verbose_name=_("Blog"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, verbose_name=_("User"))
    name = models.CharField(_("Name"), max_length=30)
    text = models.TextField(_("Text"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.blog}'
