# core/tasks.py
from celery import shared_task
from .models import AudioFragment, VoiceAssignment
# Importa tus funciones auxiliares (debes moverlas a un archivo utils.py)
# from .utils import synthesize_text_to_speech 

# NOTA: Debes mover tu función `synthesize_text_to_speech` a un archivo
# `core/utils.py` y adaptarla para que funcione sin la `status_queue` de Tkinter.
# Esta es una versión simplificada de cómo se vería:

# Placeholder para la función real que debes importar
def synthesize_text_to_speech_logic(text_content, audio_path, voice_name):
    # ... Aquí iría la lógica de llamada a la API de Google ...
    # ... Guarda el MP3 en audio_path ...
    print(f"Sintetizando '{text_content[:30]}...' con voz {voice_name}")
    # En un caso real, esto puede fallar, así que necesitarías manejar errores.
    pass

@shared_task
def synthesize_fragment_task(fragment_id):
    try:
        fragment = AudioFragment.objects.get(pk=fragment_id)
        project = fragment.project
        assignment = VoiceAssignment.objects.get(project=project, role=fragment.role)
        
        # Define la ruta donde se guardará el archivo
        output_dir = f"media/project_audio/{project.id}/"
        os.makedirs(output_dir, exist_ok=True)
        audio_path = os.path.join(output_dir, f"fragment_{fragment.id}.mp3")

        # Llama a la lógica de síntesis real
        synthesize_text_to_speech_logic(
            text_content=fragment.text_content,
            audio_path=audio_path,
            voice_name=assignment.voice_name
        )

        # Guarda la ruta del archivo en el modelo y lo guarda
        fragment.audio_file.name = audio_path
        fragment.save()
        return f"Éxito: Fragmento {fragment_id} sintetizado."
    except AudioFragment.DoesNotExist:
        return f"Error: Fragmento con ID {fragment_id} no encontrado."
    except Exception as e:
        # Aquí podrías registrar el error para depuración
        return f"Error al sintetizar el fragmento {fragment_id}: {e}"
