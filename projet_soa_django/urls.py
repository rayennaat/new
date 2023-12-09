"""
URL configuration for projet_soa_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.urls import path
from django.contrib.auth.decorators import login_required
from project_app.views import *


urlpatterns = [
    path('', include('project_app.urls')),
    path('admin/', admin.site.urls),
    path('', include('project_app.urls')),
    path('users/', user_list, name='user_list'),
    path('user/<int:pk>/', user_detail, name='user_detail'),
    path('user/new/', user_create, name='user_create'),
    path('user/<int:pk>/edit/', user_update, name='user_update'),
    path('user/<int:pk>/delete/', user_delete, name='user_delete'),
    path('student_dash/', login_required(student_dash), name='student_dash'),

]
