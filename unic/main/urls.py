from django.urls import path
from .views import *

urlpatterns = [
    path('', main),
    path('favicon.ico', favicon),
]