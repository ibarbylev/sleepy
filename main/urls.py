from django.contrib import admin
from django.urls import path, include
from storage import views

urlpatterns = [
    path('', include('storage.urls')),
    path('admin/', admin.site.urls),
    path('api/is_exist/', views.ClientList.as_view()),
    path('api/is_exist/<int:pk>/', views.ClientDetail.as_view()),
    path('api/add-sleeps/<int:pk>', views.ClientAddSleeps.as_view()),
]
