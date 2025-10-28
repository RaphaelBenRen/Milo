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

1. **Démarrez Redis** (dans un premier terminal) :
```powershell
C:\Redis\redis-server.exe
```

2. **Lancez Milo** (dans un second terminal) :
```powershell
cd milo_ai-main
python src\back_launcher.py
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
- **Connexion Internet** (pour télécharger les dépendances et le modèle Qwen3)

**Note:** Redis 5.0+ et le modèle Qwen3 sont installés automatiquement par le script d'installation

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

**Le modèle s'installe normalement automatiquement avec `install.ps1`.**

Si le téléchargement automatique échoue:

**Option 1:** Demandez le dossier `Qwen3-0.6B` à quelqu'un qui l'a déjà et placez-le dans `C:\Models\`

**Option 2:** Téléchargez manuellement :
```powershell
pip install huggingface-hub
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='Qwen/Qwen2.5-0.5B-Instruct', local_dir='C:/Models/Qwen3-0.6B')"
```

---

### Erreur Qwen2ForCausalLM

**Erreur :** `ModuleNotFoundError: Could not import module 'Qwen2ForCausalLM'`

**Solution :**
```powershell
pip install --upgrade transformers
```

Cette erreur signifie que votre version de `transformers` est trop ancienne (< 4.37.0).

---

### Erreurs Redis

**Erreur :** `Error 10061 connecting to localhost:6379` ou `unknown command 'XREAD'`

**Solution :**
1. Vérifiez que Redis est lancé : `C:\Redis\redis-server.exe`
2. Si l'erreur `unknown command 'XREAD'` persiste, vous avez une vieille version de Redis
3. Téléchargez Redis 5.0+ depuis : https://github.com/tporadowski/redis/releases
4. Extrayez dans `C:\Redis\`

---

### Milo ne répond pas

**Vérifiez :**
1. Que Redis est bien lancé (pas d'erreurs `Error 10061`)
2. Que le serveur affiche "Qwen3 model loaded successfully"
3. Que vous êtes bien sur http://127.0.0.1:5001
4. Les logs dans le terminal pour voir les erreurs

---

## 🎓 Technologies

- **Flask** : Serveur web
- **Whisper** : Reconnaissance vocale (OpenAI)
- **Qwen3** : Modèle de langage (Alibaba)
- **Redis** : Message broker pour communication entre services
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
