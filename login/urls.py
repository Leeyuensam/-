from django.contrib import admin
from django.urls import path, include
from login.views import *

urlpatterns = [
    path('', login.as_view())
]