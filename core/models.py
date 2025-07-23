# core/models.py
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=200)
    original_text = models.TextField(blank=True, null=True)
    output_filename = models.CharField(max_length=255, default='output.mp3')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class VoiceAssignment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='voice_assignments')
    role = models.CharField(max_length=100)
    voice_name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('project', 'role') # No se puede repetir un rol en el mismo proyecto

    def __str__(self):
        return f"{self.role}: {self.voice_name}"

class AudioFragment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='fragments')
    text_content = models.TextField()
    audio_file = models.FileField(upload_to='audio_fragments/', blank=True, null=True)
    role = models.CharField(max_length=100, default='Narrator')
    order = models.PositiveIntegerField() # Para mantener el orden de los fragmentos

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Fragment {self.order} for {self.project.name}"
