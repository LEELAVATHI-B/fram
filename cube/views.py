from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import cubeUser, Note, APIkey
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from .serializers import cubeUserSerializer
from django_summernote.widgets import SummernoteInplaceWidget
from .forms import Noteform, ProfilePicUpdate
from django.core.files import File
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime


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
        elif request.POST.get('first_name'):
            cubeUser.objects.filter(user_name=request.user).update(first_name=request.POST.get('first_name'),
                                                                   last_name=request.POST.get('last_name'),
                                                                   contact_number=request.POST.get('phone'),
                                                                   email=request.POST.get('email'),
                                                                   address=request.POST.get('address'))
            return redirect('/profile')
        else:
            auth_user = User.objects.get(username=request.user)
            cube_user = cubeUser.objects.get(user_name=request.user)
            auth_user.delete()
            cube_user.delete()
            return redirect('/login')
    curr_userobj = cubeUser.objects.get(user_name=request.user.username)
    return render(request, 'cube/profile.html', {'curr_userobj': curr_userobj, 'pic_form': ProfilePicUpdate})


@login_required(login_url='/login')
def dashboard(request):
    if not request.user.is_superuser:
        curr_notes = Note.objects.all().filter(user=request.user)
        curr_notes = curr_notes.order_by('-date_created')
        paginator = Paginator(curr_notes, 5)
        page_number = request.GET.get('page')
        curr_notes = paginator.get_page(page_number)
        return render(request, 'cube/dashboard.html', {'curr_notes': curr_notes})
    return redirect('/admin')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    elif request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        print(username, password)
        curr_user = authenticate(request, username=username, password=password)
        if not curr_user:
            return render(request, 'cube/login.html', {'error': 'Invalid Credentials'})
        elif curr_user.is_superuser:
            return redirect('/admin')
        else:
            login(request, curr_user)
            return redirect('/dashboard')
    return render(request, 'cube/login.html')


def user_signup(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    elif request.method == 'POST':
        user_name = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact_number = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        if User.objects.filter(username=user_name).exists():
            return redirect('/login')
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
            tags = request.POST.get('tags')
            currNote = Note(user=request.user, title=title, content=content, tags=tags,
                            date_created=datetime.datetime.now())
            currNote.save()
            return redirect('/dashboard')
    else:
        form = Noteform()
    return render(request, 'cube/addtask.html', {'form': form})


@login_required(login_url='/login')
def view_task(request, note_id):
    note = Note.objects.get(id=note_id)
    return render(request, 'cube/view_task.html', {'note': note})


class UserCrudView(APIView):
    def get(self, request):
        if APIkey.objects.filter(key=request.GET.get('apikey')).exists():
            if not request.GET.get('random_user'):
                if not request.GET.get('all_users'):
                    users = cubeUser.objects.all()
                    page_number = request.GET.get('page_number', 1)
                    page_size = request.GET.get('page_size', 5)
                    paginator = Paginator(users, page_size)
                    try:
                        serializer = cubeUserSerializer(paginator.page(page_number), many=True)
                        return JsonResponse(serializer.data, safe=False)
                    except:
                        return JsonResponse({'error': 'Invalid Page Number'}, safe=False)
                else:
                    return JsonResponse(cubeUserSerializer(cubeUser.objects.all(), many=True).data, safe=False)
            else:
                random_user = cubeUser.objects.order_by('?').first()
                return JsonResponse(cubeUserSerializer(random_user).data, safe=False)
        return JsonResponse({'error': 'Invalid API Key'}, status=400)

    def post(self, request):
        if APIkey.objects.filter(key=request.GET.get('apikey')).exists():
            serializer = cubeUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                User.objects.create_user(request.data['user_name'], request.data['email'], request.data['password'])
                return JsonResponse(serializer.data, status=201)
            password_req = {'password': ['This field is required.']}
            required_fields = {**serializer.errors, **password_req}
            return JsonResponse(required_fields, status=400)
        return JsonResponse({'error': 'Invalid API Key'}, status=400)

    def put(self, request):
        if APIkey.objects.filter(key=request.GET.get('apikey')).exists():
            pk = request.GET.get('pk')
            user = cubeUser.objects.get(pk=pk)
            serializer = cubeUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse({'error': 'Invalid API Key'}, status=400)

    def delete(self, request):
        if APIkey.objects.filter(key=request.GET.get('apikey')).exists():
            pk = request.GET.get('pk')
            user = cubeUser.objects.get(pk=pk)
            auth_user = User.objects.get(username=user.user_name)
            auth_user.delete()
            user.delete()
            return JsonResponse({
                'message': 'User deleted successfully'
            })
        return JsonResponse({'error': 'Invalid API Key'}, status=400)

    def patch(self, request):
        if APIkey.objects.filter(key=request.GET.get('apikey')).exists():
            pk = request.GET.get('pk')
            user = cubeUser.objects.get(pk=pk)
            serializer = cubeUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse({'error': 'Invalid API Key'}, status=400)


def search_result(request, search_query):
    notes = Note.objects.filter(user=request.user, title__icontains=search_query)
    return render(request, 'cube/search_results.html', {'curr_notes': notes})


def delete_note(request, note_id):
    note = Note.objects.get(id=note_id)
    note.delete()
    return redirect('/dashboard')


def editNote(request, note_id):
    if request.method == "POST":
        form = Noteform(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            note = Note.objects.get(pk=note_id)
            note.title = title
            note.content = content
            note.save()
            return redirect('/dashboard')
    note = Note.objects.get(pk=note_id)
    intial_data = {
        'title': note.title,
        'content': note.content,
    }
    editForm = Noteform(request.POST or None, initial=intial_data)
    return render(request, 'cube/edit_task.html', {'form': editForm})
