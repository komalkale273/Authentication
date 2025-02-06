from django.shortcuts import render

# Create your views here.
# def index(request):
#     return render(request, 'index.html')
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail

# Home Page (Login Page)
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Redirect to Dashboard after login
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


# Sign Up Page
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Account created successfully! Please log in.")
                return redirect("login")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "signup.html")


# Forgot Password Page
def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            # Simulating a password reset link
            reset_link = "http://127.0.0.1:8000/reset-password/"
            send_mail(
                "Password Reset Request",
                f"Click the link to reset your password: {reset_link}",
                "admin@example.com",
                [email],
                fail_silently=False,
            )
            messages.success(request, "Password reset instructions have been sent to your email")
        else:
            messages.error(request, "No user found with this email")

    return render(request, "forgot_password.html")


# Change Password Page (Only accessible if logged in)
@login_required
def change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in
            messages.success(request, "Your password was successfully updated!")
            return redirect("dashboard")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "change_password.html", {"form": form})


# Dashboard (Only accessible if logged in)
@login_required
def dashboard_view(request):
    return render(request, "dashboard.html", {"user": request.user})


# Profile Page (Only accessible if logged in)
@login_required
def profile_view(request):
    return render(request, "profile.html", {"user": request.user})


# Logout User
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
