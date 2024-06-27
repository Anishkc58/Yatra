from django.contrib import admin
from django.urls import path
from .views import signup_view, login_view, tour_view, booking_view, booking_confirmation_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('', tour_view, name='tour'),
    path('book/', booking_view, name='book'),
    path('booking_confirmation/', booking_confirmation_view, name='booking_confirmation'),
]
