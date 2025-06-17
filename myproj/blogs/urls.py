from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.blogs_list,name="list"),
    path('<slug:slug>',views.blog_page,name="blog_page"),
    path('comment/edit/<int:pk>',views.edit_comment,name="edit_comment"),
    path('comment/delete/<int:pk>',views.delete_comment,name="delete_comment"),
    path('upvote/<int:blog_id>',views.upvote_blog,name="upvote_blog"),
    path('new/',views.blog_new,name="blog_new"),
]
