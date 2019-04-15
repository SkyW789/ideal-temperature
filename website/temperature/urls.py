from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.index, name='index'),
    path('current_status/', views.current_status, name='current_status'),
    path('add_sensor/', views.add_sensor, name='add_sensor'),
    path('sensors/', views.sensors, name='sensors'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/temp_records/', views.TemperatureRecordList.as_view()),
    path('api/temp_records/<int:pk>/', views.TemperatureRecordDetail.as_view()),
    path('api/garage_records/', views.GarageRecordList.as_view()),
    path('api/garage_records/<int:pk>/', views.GarageRecordDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
