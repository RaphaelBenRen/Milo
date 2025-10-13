# 🤖 Installation de Milo - Guide Complet

Guide d'installation de Milo, l'assistante vocale IA de l'ECE Paris.

---

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir :

- **Windows 10/11** (64-bit)
- **Python 3.12** ou supérieur
- **Au moins 4 GB de RAM libre**
- **5 GB d'espace disque libre**
- **Connexion Internet** (pour l'installation)

---

## 🚀 Installation - Étape par Étape

### 1️⃣ Installer Python

1. Téléchargez Python 3.12 depuis : https://www.python.org/downloads/
2. **IMPORTANT** : Lors de l'installation, cochez **"Add Python to PATH"**
3. Vérifiez l'installation en ouvrant PowerShell et tapant :
   ```powershell
   python --version
   ```
   Vous devriez voir : `Python 3.12.x`

---

### 2️⃣ Extraire le Projet

1. Extrayez le dossier `milo_ai-main` sur votre PC
2. Placez-le dans un emplacement simple, par exemple :
   - `C:\milo_ai-main`
   - Ou `Documents\milo_ai-main`

---

### 3️⃣ Installer FFmpeg

FFmpeg est nécessaire pour convertir les fichiers audio.

**Option automatique** (si vous avez déjà le dossier `ffmpeg-8.0-essentials_build`) :
- Le dossier est déjà inclus dans le projet, rien à faire ! ✅

**Option manuelle** (si le dossier FFmpeg est manquant) :

1. Ouvrez PowerShell dans le dossier `milo_ai-main`
2. Exécutez ces commandes :

```powershell
curl -L "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -o ffmpeg.zip
Expand-Archive -Path ffmpeg.zip -DestinationPath .
Remove-Item ffmpeg.zip
```

---

### 4️⃣ Télécharger le Modèle Qwen3

Le modèle IA Qwen3 doit être placé dans `C:\Models\Qwen3-0.6B`.

**Deux options :**

#### Option A : Copier depuis un autre PC

Si quelqu'un a déjà le modèle, copiez le dossier `Qwen3-0.6B` dans `C:\Models\`.

#### Option B : Télécharger depuis Hugging Face

1. Créez le dossier `C:\Models` s'il n'existe pas
2. Installez Git LFS :
   ```powershell
   winget install Git.Git
   ```
3. Téléchargez le modèle :
   ```powershell
   cd C:\Models
   git clone https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct Qwen3-0.6B
   ```

**Vérifiez que le dossier contient :**
- `config.json`
- `model.safetensors`
- `tokenizer.json`
- `vocab.json`
- etc.

---

### 5️⃣ Installer les Dépendances Python

1. Ouvrez PowerShell dans le dossier `milo_ai-main`
2. Installez les packages nécessaires :

```powershell
cd milo_ai-main\src
pip install flask flask-socketio flask-cors werkzeug faster-whisper torch transformers sounddevice scipy numpy
```

**Note :** L'installation peut prendre 5-10 minutes.

---

### 6️⃣ Vérifier l'Installation

Vérifiez que tout est en place :

```powershell
# Vérifier Python
python --version

# Vérifier FFmpeg
.\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe -version

# Vérifier que le modèle Qwen3 existe
ls C:\Models\Qwen3-0.6B
```

---

## ▶️ Lancer Milo

### Démarrage du Serveur

1. Ouvrez PowerShell dans le dossier `milo_ai-main\src`
2. Lancez le serveur :

```powershell
cd milo_ai-main\src
python back_launcher.py
```

**Attendez de voir :**
```
Loading Whisper model...
Pre-loading Qwen3 model...
Qwen3 model loaded successfully
 * Running on http://127.0.0.1:5001
```

⚠️ **Le premier démarrage peut prendre 1-2 minutes** (chargement des modèles).

---

### Utiliser Milo

1. Ouvrez votre navigateur
2. Allez sur : **http://127.0.0.1:5001**
3. Cliquez sur l'icône microphone
4. Posez votre question à Milo
5. Attendez la réponse vocale !

---

## 🛠️ Dépannage

### Problème : "Python n'est pas reconnu"

**Solution :** Python n'est pas dans le PATH.
1. Réinstallez Python en cochant "Add Python to PATH"
2. Ou ajoutez-le manuellement dans les variables d'environnement

---

### Problème : "Le fichier spécifié est introuvable" (FFmpeg)

**Solution :** FFmpeg n'est pas installé ou mal configuré.
1. Vérifiez que le dossier `ffmpeg-8.0-essentials_build` existe
2. Vérifiez que le fichier existe : `milo_ai-main\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe`

---

### Problème : "Qwen3 model not found"

**Solution :** Le modèle Qwen3 n'est pas au bon endroit.
1. Vérifiez que `C:\Models\Qwen3-0.6B` existe
2. Vérifiez qu'il contient `model.safetensors`

---

### Problème : Le serveur plante avec "Segmentation fault"

**Solution :** Manque de RAM ou conflit.
1. Fermez les applications gourmandes en mémoire
2. Redémarrez votre PC
3. Relancez le serveur

---

### Problème : Milo ne répond pas

**Solution :** Vérifiez les logs dans le terminal.
1. Regardez si vous voyez "Processing question"
2. Vérifiez que tous les modèles sont chargés
3. Essayez de rafraîchir la page web

---

## 📞 Support

Si vous rencontrez des problèmes :

1. Vérifiez les logs dans le terminal
2. Assurez-vous que tous les fichiers sont présents
3. Contactez le créateur du projet : Mathieu Larnaudie

---

## 🎓 Informations Techniques

### Structure du Projet

```
milo_ai-main/
├── src/
│   ├── back_launcher.py          # Serveur principal
│   ├── lib/                       # Bibliothèques
│   │   ├── transcriber.py         # Whisper (speech-to-text)
│   │   ├── subsynthetizer.py      # Qwen3 (génération réponse)
│   │   ├── tts.py                 # Text-to-speech
│   │   └── webm_to_wav_converter.py # Conversion audio
│   └── ...
├── front/                         # Interface web
├── audio/                         # Fichiers audio temporaires
├── synthetiser/                   # Transcriptions et réponses
└── ffmpeg-8.0-essentials_build/   # FFmpeg
```

### Technologies Utilisées

- **Flask** : Serveur web
- **Whisper** : Reconnaissance vocale (OpenAI)
- **Qwen3** : Modèle de langage (Alibaba)
- **FFmpeg** : Conversion audio
- **Socket.IO** : Communication temps réel

---

## 🎉 Félicitations !

Vous avez installé Milo avec succès ! Profitez de votre assistante IA personnelle.

**Développé par :** Mathieu Larnaudie & Youssef Jafaar
**Pour :** Intelligence Lab - ECE Paris

---

## ⚡ Commandes Rapides

```powershell
# Lancer Milo
cd milo_ai-main\src
python back_launcher.py

# Arrêter Milo
Ctrl + C dans le terminal

# Vérifier FFmpeg
.\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe -version

# Vérifier Python
python --version

# Réinstaller les dépendances
pip install --force-reinstall flask flask-socketio flask-cors werkzeug faster-whisper torch transformers sounddevice scipy numpy
```

---

🚀 **Bon courage et amusez-vous bien avec Milo !**
