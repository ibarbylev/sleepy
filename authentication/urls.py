from django.contrib import admin
from django.urls import path, include
from authentication import views

urlpatterns = [
    path('', include('storage.urls')),
    # path('login/', views.login, name='login'),
]
