from django.contrib.auth.forms import \
    PasswordResetForm as BuiltinPasswordResetForm

from .models import User


class PasswordResetForm(BuiltinPasswordResetForm):

    def get_users(self, email):
        active_users = User.objects.filter(**{
            'email__iexact': email,
            'verified': True,
        })
        return (u for u in active_users if u.has_usable_password())
