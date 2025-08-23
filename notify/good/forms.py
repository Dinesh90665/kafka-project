from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from good.models import Profile

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=True)
  

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            # Create or update profile
            Profile.objects.update_or_create(
                user=user,
                defaults={"phone_number": self.cleaned_data["phone"]},
               
                
                
            )
        return user
