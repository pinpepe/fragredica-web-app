# core/serializers.py
from rest_framework import serializers
from .models import Project, VoiceAssignment, AudioFragment

class AudioFragmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFragment
        fields = ['id', 'text_content', 'audio_file', 'role', 'order']

class VoiceAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceAssignment
        fields = ['role', 'voice_name']

class ProjectSerializer(serializers.ModelSerializer):
    fragments = AudioFragmentSerializer(many=True, read_only=True)
    voice_assignments = VoiceAssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'output_filename', 'fragments', 'voice_assignments']
