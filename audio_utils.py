# audio_utils.py
import os
import requests
import uuid
import whisper
import subprocess
import tempfile
import warnings


warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")


model = whisper.load_model("small")

def download_audio(media_url, auth_token):
    ogg_filename = os.path.join(tempfile.gettempdir(), f"audio_{uuid.uuid4()}.ogg")
    headers = {"Authorization": f"Basic {auth_token}"}

    print(f"🔽 Téléchargement de l'audio depuis : {media_url}")
    try:
        response = requests.get(media_url, headers=headers, timeout=10)
        response.raise_for_status()
        with open(ogg_filename, "wb") as f:
            f.write(response.content)
    except requests.RequestException as e:
        raise RuntimeError(f"Erreur lors du téléchargement de l'audio : {str(e)}")

    if not os.path.exists(ogg_filename) or os.path.getsize(ogg_filename) < 1024:
        raise RuntimeError(f"Fichier audio {ogg_filename} vide ou corrompu.")

    wav_filename = ogg_filename.replace(".ogg", ".wav")
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", ogg_filename,
            "-ar", "16000",  # Whisper recommande 16 kHz
            "-ac", "1",      # Mono
            wav_filename
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        print("💥 Erreur ffmpeg :", e.stderr)
        raise RuntimeError("Erreur de conversion audio avec ffmpeg")
    finally:
        if os.path.exists(ogg_filename):
            os.remove(ogg_filename)

    print(f"✅ Fichier audio converti : {wav_filename}")
    return wav_filename

def transcribe_audio(file_path):
    try:
        print(f"📝 Transcription du fichier audio : {file_path}")
        result = model.transcribe(file_path, language="fr", fp16=False)
        return result["text"]
    except Exception as e:
        raise RuntimeError(f"Erreur Whisper : {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
