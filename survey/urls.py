from django.urls import path, include

from . import views

app_name = 'survey'

urlpatterns = [
    path('', views.home, name="home"),
    path('building', views.get_buildings),
    path('add_building', views.add_buildings),
]