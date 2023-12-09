from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import UserForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password


def home(request):
    return render(request, 'project_app/home.html')


def user_list(request):
    users = User.objects.all()
    return render(request, 'user/user_list.html', {'users': users})


def student_dash(request):
    users = User.objects.all()
    return render(request, 'project_app/student_dash.html', {'users': users})


def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'user/user_detail.html', {'user': user})


def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('user_detail', pk=user.pk)
    else:
        form = UserForm()
    return render(request, 'user/user_form.html', {'form': form})


def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            return redirect('user_detail', pk=user.pk)
    else:
        form = UserForm(instance=user)
    return render(request, 'user/user_form.html', {'form': form})


def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user/user_confirm_delete.html', {'user': user})


class user_login(APIView):
    def post(self, request, *args, **kwargs):
        mail = request.data.get('mail')
        password = request.data.get('password')
        user = authenticate(request, mail=mail, password=password)

        if user:
            login(request, user)  # This logs in the user

            # Check the user's role and redirect accordingly
            if user.role == 'admin':
                return redirect('admin_dash')
            elif user.role == 'teacher':
                return redirect('teacher_dash')
            elif user.role == 'student':
                return redirect('student_dash')

        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class user_register(APIView):
    def post(self, request, *args, **kwargs):

        if request.data.get('password') is None:
            return Response({'error': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = make_password(request.data["password"])
        request.data["password"] = hashed_password
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




def is_student(user):
    return user.role == 'Student'


def is_tutor_or_admin(user):
    return user.role in ['Tutor', 'Administrator']
