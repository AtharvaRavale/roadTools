# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from .models import UserProfile
import re

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email'].lower()  # Ensure email is case insensitive
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            confirm_password = request.POST.get('confirm_password')

            # ✅ Check if email is already registered (case insensitive)
            if User.objects.filter(email__iexact=email).exists():
                messages.error(request, 'This email is already in use. Try logging in instead.')
                return render(request, 'accounts/register.html', {'form': form})

            # ✅ Validate email format (regex)
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, email):
                messages.error(request, 'Enter a valid email address.')
                return render(request, 'accounts/register.html', {'form': form})

            # ✅ Check if phone number is already registered
            if UserProfile.objects.filter(phone=phone).exists():
                messages.error(request, 'This phone number is already linked to an account.')
                return render(request, 'accounts/register.html', {'form': form})

            # ✅ Password validation (min 8 characters, 1 number, 1 special char)
            if len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                messages.error(request, 'Password must be at least 8 characters long and include a number and a special character.')
                return render(request, 'accounts/register.html', {'form': form})

            # ✅ Password confirmation check
            if password != confirm_password:
                messages.error(request, 'Passwords do not match. Please try again.')
                return render(request, 'accounts/register.html', {'form': form})

            # ✅ Create user and profile
            user = User.objects.create_user(username=email, email=email, first_name=first_name, last_name=last_name, password=password)
            user.save()
            UserProfile.objects.create(user=user, phone=phone)

            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()  # Normalize email
            password = form.cleaned_data['password']

            # ✅ Check if user exists
            if not User.objects.filter(email__iexact=email).exists():
                messages.error(request, "This email is not registered. Please sign up first.")
                return render(request, 'accounts/login.html', {'form': form})

            # ✅ Authenticate user
            user = authenticate(request, username=email, password=password)

            if user is not None:
                if not user.is_active:
                    messages.warning(request, "Your account is inactive. Contact support for assistance.")
                    return render(request, 'accounts/login.html', {'form': form})

                login(request, user)
                messages.success(request, 'Welcome back! You are now logged in.')
                return redirect('index')

            else:
                messages.error(request, "Invalid password. Please try again.")
                return render(request, 'accounts/login.html', {'form': form})

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    
    return render(request, 'accounts/profile.html', {
        'user': user,
        'user_profile': user_profile
    })

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
