from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('accounts/signup/', views.register_view,name="register"),
    path('accounts/login/', views.customLoginView,name="login"),
    path('accounts/logout/', views.logout_view,name="logout"),
    path('profile/',views.profile,name="profile"),
    path('accounts/password/change/', views.CustomPasswordChangeView.as_view(), name='change_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
]