from django.urls import path

from app.views import auth_view

urlpatterns = [
    path('register/', auth_view.register, name='register'),
    path('login/', auth_view.login_view, name='login'),
    path('logout/', auth_view.logout_view, name='logout'),
]
