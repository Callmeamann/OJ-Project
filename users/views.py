from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Role
from submissions.models import Submission
from django.core.paginator import Paginator
from .forms import UserUpdateForm, ProfileUpdateForm

def register_user(request):
    if request.method == 'POST':
        messages.get_messages(request).used = True  # Clear previous messages

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check for empty fields
        if not username or not password or not email:
            messages.error(request, 'Username, email, and password are required')
            return redirect('/auth/register/')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'User with this username already exists')
            return redirect('/auth/register/')

        try:
            # Create the user
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()

            messages.success(request, 'User created successfully')
            return redirect('/auth/login/')

        except Exception as e:
            messages.error(request, f'Error creating user: {e}')
            return redirect('/auth/register/')

    return render(request, 'users/register.html')


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
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # Fetch user submissions
    submissions_list = Submission.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(submissions_list, 10)  # Show 10 submissions per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'page_obj': page_obj,
    }

    return render(request, 'users/profile.html', context)


def home(request):
    template = loader.get_template('users/home.html')
    context = {
        'user': request.user
    }
    return HttpResponse(template.render(context, request))
