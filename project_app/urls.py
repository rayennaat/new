# yourapp/urls.py
from django.urls import path
from . import views
from .views import user_login
from .views import user_register
from .views import student_dash

urlpatterns = [
    path('', views.home, name='home'),
    path('api/login/', user_login.as_view(), name='user-login'),
    path('api/register/', user_register.as_view(), name='user-register'),
    path('student_dash/', student_dash, name='student_dash'),

]
