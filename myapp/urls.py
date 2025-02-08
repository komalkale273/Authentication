from django.urls import path
from django.contrib.auth import views as auth_views
from myapp.forms import CustomSetPasswordForm, CustomPasswordChangeForm

from .views import (
    login_view,
    signup_view,
    logout_view,
    reset_password_view,  # Updated name
    change_password_view,  # Correct function
    forget_password_view,  # ✅ Fixed function name
    dashboard_view,
    profile_view,
    CustomPasswordResetView  # ✅ Import this view from views.py
)

urlpatterns = [
    path("", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("profile/", profile_view, name="profile"),
    path("logout/", logout_view, name="logout"),

    # 🔐 Forgot Password & Reset
    path("forget-password/", CustomPasswordResetView.as_view(), name="forget_password"),  # ✅ Ensure this is correctly imported
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"), name="password_reset"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_confirm.html",
        form_class=CustomSetPasswordForm  # ✅ Ensure this form exists
    ), name="password_reset_confirm"),

    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),

    # Change Password
  path("change-password/", change_password_view, name="change_password"),
]
