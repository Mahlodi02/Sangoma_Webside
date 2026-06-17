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
    daily_messages_feed, daily_message_detail, react_to_message, share_message,
)

urlpatterns = [
    path('admin/',                              admin.site.urls),
    path('',                                    home,                   name='home'),
    path('about/',                              about,                  name='about'),
    path('services/',                           services,               name='services'),
    path('book/',                               book,                   name='book'),
    path('review/',                             review,                 name='review'),
    path('contact/',                            contact,                name='contact'),
    path('location/',                           location,               name='location'),
    path('register/',                           register,               name='register'),
    path('login/',                              user_login,             name='login'),
    path('logout/',                             user_logout,            name='logout'),

    # Daily message feed & detail (Facebook-style posts)
    path('messages/',                           daily_messages_feed,    name='daily_messages_feed'),
    path('messages/<int:pk>/',                  daily_message_detail,   name='daily_message_detail'),
    path('messages/<int:pk>/react/',            react_to_message,       name='react_to_message'),
    path('messages/<int:pk>/share/',            share_message,          name='share_message'),
]