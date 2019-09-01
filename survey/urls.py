from django.urls import path, include

from . import views

app_name = 'survey'

urlpatterns = [
    path('', views.home, name="home")
   
]