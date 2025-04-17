from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('movie_list')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            next_page = request.GET.get('next', 'movie_list')
            return redirect(next_page)
        else:
            # Check if username exists
            from django.contrib.auth.models import User
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Incorrect password. Please try again.')
            else:
                messages.error(request, 'Username does not exist. Please check your username or sign up.')
            return render(request, 'user/login.html', {'username': username})
    else:
        return render(request, 'user/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('movie_list')
