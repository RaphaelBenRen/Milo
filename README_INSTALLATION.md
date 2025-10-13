# 🤖 MILO AI - Guide d'Installation

**Assistant vocal intelligent pour l'ECE Paris**
Développé par Mathieu Larnaudie (ING5) & Youssef Jafaar
Intelligence Lab - ECE Paris

---

## 🚀 Installation Rapide (Méthode Automatique)

### Prérequis
- **Python 3.12** ou supérieur
- **Windows** (testé sur Windows 10/11)
- **Connexion Internet** (environ 1.2 GB à télécharger)

### Installation en 2 étapes

1. **Lancer le script d'installation**
   ```bash
   python INSTALL.py
   ```

2. **Attendre la fin** (peut prendre 10-20 minutes selon votre connexion)

C'est tout ! Le script va automatiquement :
- ✅ Installer tous les packages Python nécessaires
- ✅ Télécharger le modèle Qwen3 (943 MB)
- ✅ Télécharger le modèle de synthèse vocale français (73 MB)
- ✅ Télécharger et installer FFmpeg (184 MB)
- ✅ Vérifier que tout fonctionne

---

## 🎯 Démarrer Milo

Une fois l'installation terminée :

```bash
cd src
python back_launcher.py
```

**Attendre 30 secondes** que les modèles se chargent.

Vous verrez :
```
 * Running on http://127.0.0.1:5000
```

---

## 🌐 Utiliser Milo

1. **Ouvrir votre navigateur**
2. **Aller sur** : `http://127.0.0.1:5000`

   ⚠️ **IMPORTANT** : N'ouvrez PAS le fichier HTML directement !
   Utilisez impérativement l'URL `http://127.0.0.1:5000`

3. **Cliquer sur le bouton microphone** (bouton avec l'icône de micro)
4. **Autoriser l'accès au microphone** quand le navigateur le demande
5. **Poser votre question** clairement (ex: "Bonjour Milo, peux-tu te présenter ?")
6. **Cliquer à nouveau** pour arrêter l'enregistrement
7. **Attendre 25-30 secondes** pendant le traitement
8. **Écouter la réponse** de Milo

---

## 💡 Conseils pour de meilleures réponses

### ✅ Bonnes pratiques
- Parler clairement et assez fort
- Poser des questions complètes avec du contexte
- Exemples de bonnes questions :
  - "Bonjour Milo, qui es-tu ?"
  - "Explique-moi l'alternance à l'ECE"
  - "Quelles sont les majeures disponibles ?"
  - "Parle-moi des associations étudiantes"

### ❌ À éviter
- Questions trop courtes : "Bonjour" seul
- Parler trop bas ou avec du bruit de fond
- Poser plusieurs questions en même temps

---

## 📊 Temps de traitement

Le traitement complet prend environ **25-30 secondes** :
- Conversion audio : ~1 seconde
- Transcription Whisper : ~20-22 secondes ⏰ (le plus long)
- Génération de réponse Qwen3 : ~1-3 secondes
- Synthèse vocale : ~5 secondes

> **Note** : Le temps peut varier selon la puissance de votre ordinateur.
> Tout fonctionne sur CPU (pas besoin de carte graphique).

---

## 🛠️ Résolution de problèmes

### Le script d'installation échoue

**Problème** : Erreur lors du téléchargement du modèle Qwen3

**Solution** : Téléchargement manuel
1. Aller sur https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/tree/main
2. Télécharger tous les fichiers
3. Les placer dans `C:/Models/Qwen3-0.6B/`

---

### Le serveur ne démarre pas

**Problème** : Erreur "ModuleNotFoundError"

**Solution** : Réinstaller les packages
```bash
pip install flask flask-socketio flask-cors werkzeug transformers torch huggingface-hub faster-whisper coqui-tts piper-tts redis ollama
```

---

### Milo ne répond pas / réfléchit à l'infini

**Vérifier** :
1. Que vous utilisez bien `http://127.0.0.1:5000` (pas `file:///...`)
2. Que le serveur Python est bien lancé
3. La console du navigateur (F12) pour voir les erreurs
4. Les logs du serveur Python

**Solution** : Redémarrer le serveur
```bash
# Arrêter avec Ctrl+C
# Relancer
python back_launcher.py
```

---

### FFmpeg introuvable

**Problème** : Erreur "FFmpeg not found"

**Solution** : Vérifier l'installation
```bash
C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe -version
```

Si ça ne marche pas, télécharger manuellement :
1. https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip
2. Extraire dans `C:/ffmpeg/`

---

### Réponses incohérentes ou étranges

**C'est normal !** Qwen3-0.6B est un **très petit modèle** (600M paramètres).

**Pour améliorer** :
- Poser des questions plus claires et détaillées
- Parler plus fort et distinctement
- Donner du contexte dans vos questions

---

## 📁 Structure du projet

```
milo_ai-main/
├── INSTALL.py              ← Script d'installation automatique
├── README_INSTALLATION.md  ← Ce fichier
├── src/
│   ├── back_launcher.py    ← Serveur Flask principal
│   └── lib/
│       ├── transcriber.py  ← Transcription audio (Whisper)
│       ├── subsynthetizer.py ← Génération de réponse (Qwen3)
│       ├── tts.py          ← Synthèse vocale (Piper)
│       └── ...
├── front/
│   ├── index.html          ← Interface web
│   └── scripts/
│       ├── buttons.js      ← Gestion des boutons
│       └── audioPlay.js    ← Lecture audio
└── audio/
    └── tts_models/         ← Modèle vocal français
```

**Fichiers externes (installés automatiquement)** :
- `C:/Models/Qwen3-0.6B/` : Modèle de langage
- `C:/ffmpeg/` : Convertisseur audio

---

## 🎓 Fonctionnalités de Milo

### Mode Question/Réponse (Bouton 3 - Microphone)
- Pose une question à Milo
- Obtiens une réponse vocale
- Idéal pour des questions sur l'ECE

### Mode Résumé de Cours (Bouton 2 - REC)
- Enregistre un cours en continu
- Génère un résumé automatique
- Utile pour réviser

---

## 📞 Support

En cas de problème :
1. Vérifier cette documentation
2. Consulter les logs du serveur Python
3. Ouvrir la console du navigateur (F12)
4. Contacter les développeurs :
   - Mathieu Larnaudie (ING5)
   - Youssef Jafaar

---

## 🏆 Crédits

**Développé par** :
- Mathieu Larnaudie (ING5)
- Youssef Jafaar

**Dans le cadre de** :
- Intelligence Lab - ECE Paris

**Technologies utilisées** :
- Qwen2.5-0.5B-Instruct (Alibaba Cloud)
- Faster Whisper (OpenAI)
- Piper TTS (Rhasspy)
- Flask + SocketIO
- FFmpeg

---

**Version** : 1.0
**Dernière mise à jour** : Octobre 2025

---

🎉 **Bon usage de Milo !**
