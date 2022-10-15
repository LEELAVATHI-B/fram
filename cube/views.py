from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.http import JsonResponse
from rest_framework import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import cubeUser, Note
from django.views.generic import CreateView
from django_summernote.widgets import SummernoteInplaceWidget
from .forms import Noteform, ProfilePicUpdate
from django.core.files import File
import datetime
from django.views.decorators.http import require_http_methods
from PIL import Image


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return redirect('/login')


@login_required(login_url='/login')
def profile(request):
    if request.method == 'POST':
        curr_user = cubeUser.objects.get(user_name=request.user)
        if request.FILES.get('profile_photo'):
            img = request.FILES.get('profile_photo')
            curr_user.profile_pic.save(img.name, File(img))
            return redirect('/profile')
        else:
            cubeUser.objects.filter(user_name=request.user).update(first_name=request.POST.get('first_name'),
                                                                   last_name=request.POST.get('last_name'),
                                                                   contact_number=request.POST.get('phone'),
                                                                   email=request.POST.get('email'),
                                                                   address=request.POST.get('address'))
            return redirect('/profile')
    curr_userobj = cubeUser.objects.get(user_name=request.user.username)
    return render(request, 'cube/profile.html', {'curr_userobj': curr_userobj, 'pic_form': ProfilePicUpdate})


@login_required(login_url='/login')
def dashboard(request):
    curr_notes = Note.objects.all().filter(user=request.user)
    return render(request, 'cube/dashboard.html', {'curr_notes': curr_notes})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    elif request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        print(username, password)
        curr_user = authenticate(request, username=username, password=password)
        if curr_user.is_superuser:
            return redirect('/admin')
        elif curr_user is not None:
            login(request, curr_user)
            return redirect('/dashboard')
        else:
            return HttpResponse('Login Failed')
    return render(request, 'cube/login.html')


def user_signup(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
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
        return redirect('/login')
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


@login_required(login_url='/login')
def NoteView(request):
    if request.method == 'POST':
        form = Noteform(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            print(title, content)
            currNote = Note(user=request.user, title=title, content=content, date_created=datetime.datetime.now())
            currNote.save()
            return redirect('/dashboard')
    else:
        form = Noteform()
    return render(request, 'cube/addtask.html', {'form': form})


@login_required(login_url='/login')
def view_task(request, note_id):
    note = Note.objects.get(id=note_id)
    return render(request, 'cube/view_task.html', {'note': note})
