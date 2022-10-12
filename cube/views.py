from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.http import JsonResponse
from rest_framework import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import cubeUser

# Create your views here.

home_page = lambda request: render(request, 'cube/dashboard.html')



def index(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return redirect('/login')


@login_required(login_url='/login')
def profile(request, username):
    return HttpResponse("userprofile")


@login_required(login_url='/login')
def dashboard(request):
    return render(request, 'cube/dashboard.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    elif request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        print(username, password)
        curr_user = authenticate(request, username=username, password=password)
        if curr_user is not None:
            login(request, curr_user)
            return redirect('/dashboard')
        else:
            return HttpResponse('Login Failed')
    return render(request, 'cube/login.html')


def user_signup(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact_number = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        currUser = cubeUser(user_name=user_name, first_name=first_name, last_name=last_name, email=email,
                            contact_number=contact_number, address=address)
        authUser = User.objects.create_user(user_name, email, password)
        authUser.save()
        currUser.save()
        print("user created successfully")
        return HttpResponse('user created successfully')
    return render(request, 'cube/signup.html')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/login')



def check_username(request):
    username = request.GET.get('username')
    data = {
        'username_exists': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def check_email(request):
    email = request.GET.get('email')
    data = {
        'email_exists': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)
