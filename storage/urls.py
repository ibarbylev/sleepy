from django.urls import path, include
from storage.views import index_view

app_name = 'blog'
urlpatterns = [
    path('', index_view, name='index'),
]
