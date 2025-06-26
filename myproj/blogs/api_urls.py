from django.urls import path
from .api_views import BlogListCreateAPIView , BlogDetailAPIView

urlpatterns = [ 
    path('blogs/',BlogListCreateAPIView.as_view(),name='api-blog-list'),
    path('blogs/<int:pk>/',BlogDetailAPIView.as_view(),name='api-blog-detail'),
]