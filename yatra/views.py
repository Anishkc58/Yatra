from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, BookingForm
from .models import Destination, Booking
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages


class CustomUserCreationForm(CustomUserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email',  'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            # user = form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            # print(f"User {user.username} created successfully.")
            # login(request, user)
            return redirect('login')
        else:
            print(form.errors)
    
    else:
        form = CustomUserCreationForm()
    context = {'form':form}
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('tour')
        else:
            messages.info(request, 'Username or Password is incorrect')
            context = {}
            return render(request, 'login.html', context)

        form = AuthenticationForm(request, data=request.POST)
        # if form.is_valid():
        #     user = form.get_user()
        #     # print(f"Welcome back {user.username}.")
        #     # login(request, user)
        #     return redirect('tour')
    else:
        form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'login.html', {'form': form})

def tour_view(request):
    destinations = Destination.objects.all()
    return render(request, 'tour.html', {'destinations': destinations})

def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('booking_confirmation')
    else:
        form = BookingForm()
    return render(request, 'booking.html', {'form': form})

def booking_confirmation_view(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_confirmation.html', {'bookings': bookings})

def travel_view(request):
     return render(request, 'travel.html')
