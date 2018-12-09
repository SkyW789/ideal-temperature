from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('current_temps/', views.current_temps, name='current_temps'),
    path('add_sensor/', views.add_sensor, name='add_sensor'),
    path('sensors/', views.sensors, name='sensors'),
    path('accounts/', include('django.contrib.auth.urls')),
]
