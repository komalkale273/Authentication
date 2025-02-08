import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.template.loader import render_to_string
from .models import Profile  # Ensure Profile model exists
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from myapp.forms import CustomPasswordChangeForm


def validate_password(password, username, email):
    if username.lower() in password.lower() or email.split('@')[0].lower() in password.lower():
        raise ValidationError("Your password can’t be too similar to your personal information.")
    
    if password.isnumeric():
        raise ValidationError("Your password can’t be entirely numeric.")
    
    if len(password) < 8:
        raise ValidationError("Your password must contain at least 8 characters.")
    
    common_passwords = ["password", "123456", "qwerty", "letmein"]
    if password.lower() in common_passwords:
        raise ValidationError("Your password can’t be a commonly used password.")



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")



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
                try:
                    validate_password(password, username, email)
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    messages.success(request, "Account created successfully! Please log in.")
                    return redirect("login")
                except ValidationError as e:
                    messages.error(request, e.message)
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "signup.html")




@login_required
def logout_view(request):
    logout(request)
    return redirect("login")



def send_password_reset_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    domain = get_current_site(request).domain
    protocol = "https" if request.is_secure() else "http"

    reset_link = f"{protocol}://{domain}/reset-password/{uid}/{token}/"

    email_subject = "Password Reset Request"
    email_body = f"""
    Hello {user.username},

    You requested a password reset. Click the link below to reset your password:

    {reset_link}

    If you didn't request this, please ignore this email.

    Thanks!
    """

    send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)



class CustomPasswordResetView(PasswordResetView):
    template_name = "forget_password.html"  # ✅ Make sure this file exists!
    email_template_name = "password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")

    
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        users = User.objects.filter(email=email)

        if users.exists():
            for user in users:
                send_password_reset_email(self.request, user)

        return super().form_valid(form)



def forget_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, 'No user found with this email.')
            return redirect('forget_password')

        send_password_reset_email(request, user)  # Send reset email

        messages.success(request, 'An email has been sent with password reset instructions.')
        return redirect('forget_password')

    return render(request, 'forget_password.html')

def reset_password_view(request, uidb64, token):  # Changed function name
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, 'change_password.html', {"valid": True})

            user.set_password(new_password)
            user.save()

            messages.success(request, "Password changed successfully. You can now log in.")
            return redirect('login')
    else:
        messages.error(request, "Invalid or expired token.")
        return redirect('forget_password')

    return render(request, 'change_password.html', {"valid": True})
@login_required
@login_required
def change_password_view(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevents logout after password change
            return redirect("dashboard")  # Redirect after successful change
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, "change_password.html", {"form": form, "user_id": request.user.id})


def profile_view(request):
    return render(request, 'profile.html')



def dashboard_view(request):
    return render(request, 'dashboard.html')
