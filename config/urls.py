# =====================================================
#  Ntatemoholo Seromo — Sangoma Wisdom
#  URL Configuration
#  File: config/urls.py  (REPLACE the whole file)
# =====================================================

from django.contrib import admin
from django.urls import path
from core.views import (
    home, about, services, book,
    review, contact, location,
    register, user_login, user_logout,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',            home,        name='home'),
    path('about/',      about,       name='about'),
    path('services/',   services,    name='services'),
    path('book/',       book,        name='book'),
    path('review/',     review,      name='review'),
    path('contact/',    contact,     name='contact'),
    path('location/',   location,    name='location'),
    path('register/',   register,    name='register'),
    path('login/',      user_login,  name='login'),
    path('logout/',     user_logout, name='logout'),
]