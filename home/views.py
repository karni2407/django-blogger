from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from .utils.accepted_domains import check_email_domain


def homepage(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("home:homepage")

    if request.method == 'POST':
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("password2", "").strip()

        if not username or not email or not password or not confirm_password:
            messages.error(request, "All fields are required")
            return render(request, "register.html")

        if check_email_domain(email):
            messages.error(request, "Email domain is not accepted")
            return render(request, "register.html")

        if password != confirm_password:
            messages.error(request, "Passwords don't match!")
            return render(request, "register.html")
        '''below if statement will check unique usernames so that an account can't be created with same username twice.'''
        if User.objects.filter(email=email).exists() and User.objects.filter(
                username=username).exists():
            messages.error(request, "Email or Username is already in use!")
            return render(request, "register.html")
        try:
            validate_password(password)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, "register.html")
        try:
            with transaction.atomic():
                '''
                transaction.atomic lib uses a method that only creates unique users for each submission, this prevent the cause when form is submitted with an error but backend still creates database entry and next time when someone tries it shows that user is already created
                '''
                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password)
        except IntegrityError:
            messages.error(request, "Something went wrong! Please try again")
            return render(request, "register.html")
        except Exception:
            messages.error(request, "Unexcepected error")
            return render(request, "register.html")
        '''
        the below function will login user when userr is created.
        '''
        try:
            auth_login(request, user)
            messages.error(request,
                             "Account created and logged in succesfully!")
            return redirect("home:homepage")
        except Exception as e:
            messages.error(request, "User is created but error in login")
            return redirect('home:login')

    else:
        return render(request, "register.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("home:homepage")

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            next_url = request.GET.get("next")
            messages.success(request, f"Welcome back , {user}!")
            return redirect(next_url if next_url else "home:homepage")

        messages.error(request, "Invalid username or password!")
        return render(request, "login.html")
    else:
        return render(request, "login.html")


def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("home:homepage")
