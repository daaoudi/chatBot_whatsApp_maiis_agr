# chatBot_whatsApp_maiis_agr
chatBot intelligent pour petits agriculture Maiis 

# 🌱 ChatBot WhatsApp "Maïs-Agr" - Assistant Intelligent pour Petits Agriculteurs


[![Python 3.12+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)

## 📌 Description
Chatbot intelligent pour les petits agriculteurs de maïs, accessible via WhatsApp. Fournit:
- Conseils agricoles en temps réel
- Diagnostic des maladies du maïs
- Rappels des périodes de semis/récolte
- Alertes météo personnalisées
- Marchés et prix locaux

## 🌟 Fonctionnalités Clés
| Fonctionnalité | Technologie | Description |
|---------------|------------|-------------|
| Traitement des messages texte | Sentence-Transformers (MiniLM-L12-v2) | Compréhension des questions en français/arabe |
| Traitement vocal | FFmpeg + Whisper | Conversion .ogg→.wav + transcription |
| Gestion des conversations | Twilio API | Connectivité WhatsApp |
| Développement local | Ngrok | Tunnel sécurisé pour tests |
| Base de connaissances | Intentions prédéfinies | 50+ scénarios agricoles couverts |

## 🛠 Installation

### Prérequis
- Python 3.12+
- Compte Twilio avec sandbox WhatsApp
-Ngrok
-openai-whisper
-ffmpeg

```bash
# 1. Cloner le dépôt
git clone https://github.com/votreuser/chatBot_whatsApp_mais_agr.git
cd chatBot_whatsApp_mais_agr

# 2. Installer les dépendances
# 3. installer ffmpeg
# 4. telecharger ngrok et cree de compte 

