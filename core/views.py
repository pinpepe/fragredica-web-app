# core/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Project, AudioFragment
from .serializers import ProjectSerializer, AudioFragmentSerializer
from .tasks import synthesize_fragment_task

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated] # Solo usuarios autenticados

    def get_queryset(self):
        # Los usuarios solo pueden ver sus propios proyectos
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Asignar el proyecto al usuario actual al crearlo
        serializer.save(owner=self.request.user)

class AudioFragmentViewSet(viewsets.ModelViewSet):
    queryset = AudioFragment.objects.all()
    serializer_class = AudioFragmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Los usuarios solo pueden ver fragmentos de sus propios proyectos
        return AudioFragment.objects.filter(project__owner=self.request.user)

    @action(detail=True, methods=['post'])
    def synthesize(self, request, pk=None):
        fragment = self.get_object()
        # Lanzar la tarea en segundo plano
        task = synthesize_fragment_task.delay(fragment.id)
        return Response(
            {'status': 'synthesis_started', 'task_id': task.id},
            status=status.HTTP_202_ACCEPTED
        )
