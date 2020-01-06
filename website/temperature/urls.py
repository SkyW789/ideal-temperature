from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.index, name='index'),
    path('current_status/', views.current_status, name='current_status'),
    path('add_sensor/', views.add_sensor, name='add_sensor'),
    path('sensors/', views.sensors, name='sensors'),
    path('chart/', views.chart, name='chart'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/temp_records/', views.TemperatureRecordList.as_view()),
    path('api/temp_records/<int:pk>/', views.TemperatureRecordDetail.as_view()),
    path('api/door_records/', views.DoorRecordList.as_view()),
    path('api/door_records/<int:pk>/', views.DoorRecordDetail.as_view()),
    path('api/light_records/', views.LightRecordList.as_view()),
    path('api/light_records/<int:pk>/', views.LightRecordDetail.as_view()),
    path('api/temp_list/', views.TemperaturesBySensor.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
