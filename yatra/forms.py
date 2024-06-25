from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Booking

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(user=user, phone_number=self.cleaned_data['phone_number'])
            print(f"User {user.username} saved with email {user.email} and phone number {self.cleaned_data['phone_number']}")
        return user

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['destination', 'travel_date']



