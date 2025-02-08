from django import forms
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm

class CustomSetPasswordForm(SetPasswordForm):
    """
    Custom password reset form that only includes new password fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Custom form for changing password that includes old password verification.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})
