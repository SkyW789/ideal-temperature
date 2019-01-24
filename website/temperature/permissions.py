from rest_framework import permissions
from .models import TemperatureSensor

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            # If no data is being posted to allow it
            if not request.data:
                return True
            sensor = TemperatureSensor.objects.get(name=request.data['sensorName'])
            return sensor.owner == request.user
        return False
