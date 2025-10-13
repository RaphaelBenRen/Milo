# 🤖 Milo - Assistante Vocale IA

Milo est une assistante vocale intelligente développée pour l'ECE Paris par **Mathieu Larnaudie** et **Youssef Jafaar** dans le cadre de l'Intelligence Lab.

---

## 🚀 Installation Rapide (pour vos amis)

### Option 1 : Installation Automatique (Recommandé)

1. **Extraire le dossier** `milo_ai-main` sur votre PC
2. **Ouvrir PowerShell** dans le dossier `milo_ai-main` :
   - Clic droit sur le dossier → "Ouvrir dans le terminal" ou "Ouvrir PowerShell ici"
3. **Exécuter le script d'installation** :
   ```powershell
   .\install.ps1
   ```
4. **Suivre les instructions** affichées à l'écran

⚠️ **Note :** Si vous obtenez une erreur de sécurité PowerShell, exécutez d'abord :
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Option 2 : Installation Manuelle

Consultez le fichier **SETUP.md** pour un guide complet étape par étape.

---

## ▶️ Lancer Milo

Une fois l'installation terminée :

```powershell
cd src
python back_launcher.py
```

Attendez de voir :
```
Qwen3 model loaded successfully
* Running on http://127.0.0.1:5001
```

Puis ouvrez votre navigateur sur : **http://127.0.0.1:5001**

---

## 🎤 Utilisation

1. Cliquez sur l'icône microphone
2. Posez votre question à Milo
3. Attendez la réponse vocale

**Exemples de questions :**
- "Milo, qui es-tu ?"
- "Parle-moi de l'ECE Paris"
- "Quelles sont les majeures disponibles ?"
- "Raconte-moi une blague"

---

## 📋 Prérequis

- **Windows 10/11** (64-bit)
- **Python 3.10+**
- **4 GB de RAM libre**
- **5 GB d'espace disque**
- **Modèle Qwen3** dans `C:\Models\Qwen3-0.6B`

---

## 📁 Structure du Projet

```
milo_ai-main/
├── install.ps1                    # Script d'installation automatique
├── SETUP.md                       # Guide d'installation détaillé
├── README.md                      # Ce fichier
├── src/
│   ├── back_launcher.py           # Serveur principal
│   └── lib/                       # Bibliothèques (Whisper, Qwen3, TTS)
├── front/                         # Interface web
└── ffmpeg-8.0-essentials_build/   # FFmpeg (conversion audio)
```

---

## 🛠️ Dépannage

### Le script install.ps1 ne s'exécute pas

**Erreur :** `impossible de charger le fichier... car l'exécution de scripts est désactivée`

**Solution :**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Python n'est pas reconnu

**Solution :** Réinstallez Python en cochant **"Add Python to PATH"**

Téléchargez depuis : https://www.python.org/downloads/

---

### FFmpeg introuvable

**Solution :** Relancez `install.ps1`, il téléchargera automatiquement FFmpeg.

---

### Modèle Qwen3 manquant

**Solution :**
1. Demandez le dossier `Qwen3-0.6B` à quelqu'un qui l'a déjà
2. Placez-le dans `C:\Models\Qwen3-0.6B`

Ou téléchargez-le :
```powershell
git clone https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct C:\Models\Qwen3-0.6B
```

---

### Milo ne répond pas

**Vérifiez :**
1. Que le serveur affiche "Qwen3 model loaded successfully"
2. Que vous êtes bien sur http://127.0.0.1:5001
3. Les logs dans le terminal pour voir les erreurs

---

## 🎓 Technologies

- **Flask** : Serveur web
- **Whisper** : Reconnaissance vocale (OpenAI)
- **Qwen3** : Modèle de langage (Alibaba)
- **FFmpeg** : Conversion audio
- **Socket.IO** : Communication temps réel

---

## 👥 Développeurs

- **Mathieu Larnaudie** (ING5)
- **Youssef Jafaar**

**Projet** : Intelligence Lab - ECE Paris

---

## 📞 Support

Pour toute question ou problème :
1. Consultez **SETUP.md** pour le guide détaillé
2. Vérifiez la section dépannage ci-dessus
3. Contactez les développeurs

---

## ⚡ Commandes Rapides

```powershell
# Installer tout automatiquement
.\install.ps1

# Lancer Milo
cd src
python back_launcher.py

# Arrêter Milo
Ctrl + C

# Réinstaller les dépendances Python
pip install --force-reinstall flask flask-socketio flask-cors werkzeug faster-whisper torch transformers sounddevice scipy numpy ollama
```

---

🚀 **Amusez-vous bien avec Milo !**
