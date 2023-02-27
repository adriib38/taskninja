from .models import Project, Task
from rest_framework import viewsets, permissions
from .serializers import ProjectSerializer, TaskSerializer

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

'''
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
'''

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer
    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(user=user)
        
'''
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
'''

'''
Devuelve todas las tareas del usuario al que pertenece el token de autenticación
'''
class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)
    
        