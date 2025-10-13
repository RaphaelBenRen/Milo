#!/usr/bin/env python3
"""
Script d'installation automatique pour Milo AI
Auteur: Mathieu Larnaudie & Youssef Jafaar
Projet: Intelligence Lab - ECE Paris
"""

import os
import sys
import urllib.request
import zipfile
from pathlib import Path

def print_step(step, message):
    print(f"\n{'='*60}")
    print(f"ÉTAPE {step}: {message}")
    print('='*60)

def install_packages():
    print_step(1, "Installation des packages Python")
    print("Cela peut prendre 5-10 minutes...")
    os.system("pip install flask flask-socketio flask-cors werkzeug transformers torch huggingface-hub faster-whisper coqui-tts piper-tts redis ollama")

def download_qwen():
    print_step(2, "Téléchargement du modèle Qwen3 (943 MB)")
    try:
        from huggingface_hub import snapshot_download
        os.makedirs("C:/Models", exist_ok=True)
        print("Téléchargement en cours (cela peut prendre plusieurs minutes)...")
        snapshot_download(
            repo_id='Qwen/Qwen2.5-0.5B-Instruct',
            local_dir='C:/Models/Qwen3-0.6B'
        )
        print("✅ Modèle Qwen3 installé dans C:/Models/Qwen3-0.6B")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("\nVeuillez télécharger manuellement:")
        print("1. Aller sur https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/tree/main")
        print("2. Télécharger tous les fichiers")
        print("3. Les placer dans C:/Models/Qwen3-0.6B/")
        input("Appuyez sur Entrée une fois le téléchargement manuel terminé...")

def download_tts():
    print_step(3, "Téléchargement du modèle TTS français (73 MB)")
    os.makedirs("audio/tts_models", exist_ok=True)

    print("Téléchargement du modèle vocal...")
    urllib.request.urlretrieve(
        "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/upmc/medium/fr_FR-upmc-medium.onnx",
        "audio/tts_models/fr_FR-upmc-medium.onnx"
    )
    print("Téléchargement de la configuration...")
    urllib.request.urlretrieve(
        "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/upmc/medium/fr_FR-upmc-medium.onnx.json",
        "audio/tts_models/fr_FR-upmc-medium.onnx.json"
    )
    print("✅ Modèle TTS installé dans audio/tts_models/")

def download_ffmpeg():
    print_step(4, "Téléchargement de FFmpeg (184 MB)")

    print("Téléchargement en cours...")
    urllib.request.urlretrieve(
        "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
        "ffmpeg.zip"
    )

    print("Extraction en cours...")
    with zipfile.ZipFile("ffmpeg.zip", 'r') as zip_ref:
        zip_ref.extractall("C:/ffmpeg/")

    os.remove("ffmpeg.zip")
    print("✅ FFmpeg installé dans C:/ffmpeg/ffmpeg-master-latest-win64-gpl/")

def verify_installation():
    print_step(5, "Vérification de l'installation")

    checks = {
        "Modèle Qwen3": Path("C:/Models/Qwen3-0.6B/config.json").exists(),
        "Modèle TTS": Path("audio/tts_models/fr_FR-upmc-medium.onnx").exists(),
        "FFmpeg": Path("C:/ffmpeg/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe").exists(),
    }

    print("\nRésultats de la vérification:")
    for name, status in checks.items():
        symbol = "✅" if status else "❌"
        print(f"  {symbol} {name}: {'OK' if status else 'MANQUANT'}")

    all_ok = all(checks.values())

    if all_ok:
        print("\n" + "="*60)
        print("🎉 INSTALLATION COMPLÈTE AVEC SUCCÈS!")
        print("="*60)
        print("\nPour lancer Milo:")
        print("  1. Ouvrir un terminal dans le dossier du projet")
        print("  2. Exécuter: cd src")
        print("  3. Exécuter: python back_launcher.py")
        print("  4. Ouvrir votre navigateur sur: http://127.0.0.1:5000")
        print("\n⚠️  IMPORTANT: N'ouvrez PAS le fichier HTML directement!")
        print("    Utilisez l'URL: http://127.0.0.1:5000")
        print("\n💡 Le premier démarrage peut prendre 30 secondes (chargement des modèles)")
    else:
        print("\n" + "="*60)
        print("⚠️  INSTALLATION INCOMPLÈTE")
        print("="*60)
        print("\nCertains composants manquent. Vérifiez les erreurs ci-dessus.")
        print("Vous pouvez réessayer en relançant ce script.")

if __name__ == "__main__":
    print("="*60)
    print("      INSTALLATION AUTOMATIQUE DE MILO AI")
    print("      Intelligence Lab - ECE Paris")
    print("="*60)
    print("\nCe script va télécharger environ 1.2 GB de données.")
    print("Assurez-vous d'avoir une connexion Internet stable.\n")

    response = input("Voulez-vous continuer? (oui/non): ").lower()
    if response not in ['oui', 'o', 'yes', 'y']:
        print("Installation annulée.")
        sys.exit(0)

    try:
        install_packages()
        download_qwen()
        download_tts()
        download_ffmpeg()
        verify_installation()
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation interrompue par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        print("\nSi l'erreur persiste, consultez le README ou contactez les développeurs.")
        sys.exit(1)

    input("\nAppuyez sur Entrée pour fermer...")
