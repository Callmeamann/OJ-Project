from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def register_user(request):
    if request.method == 'POST':
        messages.get_messages(request).used = True  # Clear previous messages

        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check for empty fields
        if not username or not password:
            messages.error(request, 'Username and password are required')
            return redirect('/auth/register/')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'User with this username already exists')
            return redirect('/auth/register/')

        try:
            # Create the user
            user = User.objects.create_user(username=username)
            user.set_password(password)
            user.save()
            messages.success(request, 'User created successfully')
            return redirect('/auth/login/')
        except Exception as e:
            messages.error(request, f'Error creating user: {e}')
            return redirect('/auth/register/')

    template = loader.get_template('users/register.html')
    context = {}
    return HttpResponse(template.render(context, request))


def login_user(request):
    if request.method == "POST":
        messages.get_messages(request).used = True  # Clear previous messages

        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check for empty fields
        if not username or not password:
            messages.error(request, 'Username and password are required')
            return redirect('/auth/login/')

        # Check if the user exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'User with this username does not exist')
            return redirect('/auth/login/')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        # Check if the authentication was successful
        if user is None:
            messages.error(request, 'Invalid username or password')
            return redirect('/auth/login/')

        # Log the user in
        login(request, user)
        # messages.success(request, 'Login successful')
        return redirect('/home/')

    template = loader.get_template('users/login.html')
    context = {}
    return HttpResponse(template.render(context, request))


def logout_user(request):
    logout(request)
    messages.info(request, 'Logout successful')
    return redirect('/auth/login/')


@login_required
def profile(request):
    template = loader.get_template('users/profile.html')
    context = {
        'user': request.user
    }
    return HttpResponse(template.render(context, request))


def home(request):
    template = loader.get_template('users/home.html')
    context = {
        'user': request.user
    }
    return HttpResponse(template.render(context, request))