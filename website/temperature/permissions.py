from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            # If no data is being posted to allow it
            if not request.data:
                return True
            sensor = view.sensor_class.objects.get(name=request.data['sensorName'])
            return sensor.owner == request.user
        return False
