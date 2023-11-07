from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email', 
            'password1', 
            'password2',
            'user_role',
            'contact_number',
            'address',
            'first_name',
            'last_name',
            'contact_number'
        ]