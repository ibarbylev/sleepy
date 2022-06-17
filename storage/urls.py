from django.urls import path, include
from storage import views

app_name = 'api'
urlpatterns = [
    # path('api/is_exist/', views.ClientList.as_view()),
    path('is_exist/', views.ClientIsExists.as_view(), name='is_exist'),  # method POST
    path('delete-sleeps/<int:pk>/', views.ClientDeleteClientSleeps.as_view()),  # method PUT
    path('add-sleeps/<int:pk>/', views.ClientAddSleeps.as_view()),  # method PUT
    path('consultants/', views.ConsultantList.as_view()),  # method GET
    path('languages/', views.LanguageList.as_view()),  # method GET

]
