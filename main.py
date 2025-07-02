# app.py
from flask import Flask, request, Response
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from chatbot import chatbot_respond
from audio_utils import download_audio, transcribe_audio
import base64
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)

# Read from environment
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_WHATSAPP_NUMBER = os.getenv("TWILIO_FROM_WHATSAPP")

# Construct the basic auth
BASIC_AUTH = base64.b64encode(f"{ACCOUNT_SID}:{AUTH_TOKEN}".encode()).decode()

# Auth Twilio


client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_whatsapp_message(to_number, message):
    try:
        client.messages.create(
            body=message,
            from_=FROM_WHATSAPP_NUMBER,
            to=to_number
        )
        print(f"✅ Message envoyé à {to_number}")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi du message WhatsApp : {e}")
        raise

@app.route("/", methods=["GET"])
def home():
    return "🤖 Webhook WhatsApp avec audio OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body")
    num_media = int(request.form.get("NumMedia", 0))
    from_user = request.form.get("From")

    print(f"📨 Message de {from_user}")

    try:
        if num_media > 0:
            media_url = request.form.get("MediaUrl0")
            media_type = request.form.get("MediaContentType0")
            print(f"🔊 Audio reçu : {media_url} ({media_type})")

            if "audio" in media_type:
                local_file = download_audio(media_url, BASIC_AUTH)
                text = transcribe_audio(local_file)
                print(f"📄 Transcription : {text}")
                reply = chatbot_respond(text)
            else:
                reply = "⚠️ Seuls les fichiers audio sont pris en charge pour l’instant."
        else:
            reply = chatbot_respond(incoming_msg)

        send_whatsapp_message(from_user, reply)
        return Response("OK", status=200)

    except Exception as e:
        print("❌ Erreur globale dans le webhook :", str(e))
        return Response("Erreur serveur", status=500)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
