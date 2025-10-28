# ========================================
# 🤖 MILO - Script d'Installation Automatique
# ========================================
# Développé par : Mathieu Larnaudie & Youssef Jafaar
# Pour : Intelligence Lab - ECE Paris
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   MILO - Installation Automatique    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Variables
$PROJECT_DIR = Get-Location
$FFMPEG_DIR = "$PROJECT_DIR\ffmpeg-8.0-essentials_build"
$QWEN_MODEL = "C:\Models\Qwen3-0.6B"
$REDIS_DIR = "C:\Redis"
$PYTHON_MIN_VERSION = "3.10"

# ========================================
# Fonction : Vérifier Python
# ========================================
function Check-Python {
    Write-Host "[1/5] Verification de Python..." -ForegroundColor Yellow

    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+\.\d+)") {
            $version = $matches[1]
            Write-Host "  [OK] Python $version detecte" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "  [ERREUR] Python n'est pas installe" -ForegroundColor Red
        Write-Host ""
        Write-Host "  ACTION REQUISE :" -ForegroundColor Yellow
        Write-Host "  1. Telechargez Python depuis : https://www.python.org/downloads/" -ForegroundColor White
        Write-Host "  2. COCHEZ 'Add Python to PATH' lors de l'installation" -ForegroundColor White
        Write-Host "  3. Relancez ce script apres l'installation" -ForegroundColor White
        Write-Host ""
        return $false
    }
}

# ========================================
# Fonction : Installer FFmpeg
# ========================================
function Install-FFmpeg {
    Write-Host ""
    Write-Host "[2/5] Verification de FFmpeg..." -ForegroundColor Yellow

    if (Test-Path "$FFMPEG_DIR\bin\ffmpeg.exe") {
        Write-Host "  [OK] FFmpeg deja installe" -ForegroundColor Green
        return $true
    }

    Write-Host "  -> Telechargement de FFmpeg..." -ForegroundColor Cyan
    try {
        $ffmpegZip = "$PROJECT_DIR\ffmpeg.zip"
        Invoke-WebRequest -Uri "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -OutFile $ffmpegZip

        Write-Host "  -> Extraction de FFmpeg..." -ForegroundColor Cyan
        Expand-Archive -Path $ffmpegZip -DestinationPath $PROJECT_DIR -Force
        Remove-Item $ffmpegZip

        Write-Host "  [OK] FFmpeg installe avec succes" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "  [ERREUR] Erreur lors de l'installation de FFmpeg : $_" -ForegroundColor Red
        return $false
    }
}

# ========================================
# Fonction : Installer Redis
# ========================================
function Install-Redis {
    Write-Host ""
    Write-Host "[3/6] Verification de Redis..." -ForegroundColor Yellow

    if (Test-Path "$REDIS_DIR\redis-server.exe") {
        Write-Host "  [OK] Redis deja installe" -ForegroundColor Green
        return $true
    }

    Write-Host "  -> Telechargement de Redis 5.0.14..." -ForegroundColor Cyan
    try {
        New-Item -Path $REDIS_DIR -ItemType Directory -Force | Out-Null
        $redisZip = "$REDIS_DIR\Redis.zip"
        Invoke-WebRequest -Uri "https://github.com/tporadowski/redis/releases/download/v5.0.14.1/Redis-x64-5.0.14.1.zip" -OutFile $redisZip

        Write-Host "  -> Extraction de Redis..." -ForegroundColor Cyan
        Expand-Archive -Path $redisZip -DestinationPath $REDIS_DIR -Force
        Remove-Item $redisZip

        Write-Host "  [OK] Redis 5.0.14 installe avec succes" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "  [ERREUR] Erreur lors de l'installation de Redis : $_" -ForegroundColor Red
        return $false
    }
}

# ========================================
# Fonction : Vérifier Qwen3
# ========================================
function Check-Qwen3 {
    Write-Host ""
    Write-Host "[4/6] Verification du modele Qwen3..." -ForegroundColor Yellow

    if (Test-Path "$QWEN_MODEL\model.safetensors") {
        Write-Host "  [OK] Modele Qwen3 detecte" -ForegroundColor Green
        return $true
    }

    Write-Host "  [ERREUR] Modele Qwen3 non trouve" -ForegroundColor Red
    Write-Host ""
    Write-Host "  ACTION REQUISE :" -ForegroundColor Yellow
    Write-Host "  Le modele Qwen3 doit etre place dans : C:\Models\Qwen3-0.6B" -ForegroundColor White
    Write-Host ""
    Write-Host "  Option 1 : Copier depuis un autre PC" -ForegroundColor Cyan
    Write-Host "  - Demandez le dossier Qwen3-0.6B a quelqu'un qui l'a deja" -ForegroundColor White
    Write-Host "  - Copiez-le dans C:\Models\" -ForegroundColor White
    Write-Host ""
    Write-Host "  Option 2 : Telecharger (necessite Git)" -ForegroundColor Cyan
    Write-Host "  - Installez Git : https://git-scm.com/download/win" -ForegroundColor White
    Write-Host "  - Executez : git clone https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct C:\Models\Qwen3-0.6B" -ForegroundColor White
    Write-Host ""

    $response = Read-Host "  Voulez-vous continuer sans le modele ? (o/n)"
    if ($response -eq "o" -or $response -eq "O") {
        Write-Host "  [ATTENTION] Installation continue, mais Milo ne pourra pas generer de reponses" -ForegroundColor Yellow
        return $true
    }
    return $false
}

# ========================================
# Fonction : Installer les dépendances Python
# ========================================
function Install-PythonPackages {
    Write-Host ""
    Write-Host "[5/6] Installation des dependances Python..." -ForegroundColor Yellow
    Write-Host "  (Cela peut prendre 5-10 minutes)" -ForegroundColor Gray

    $packages = @(
        "flask",
        "flask-socketio",
        "flask-cors",
        "werkzeug",
        "faster-whisper",
        "torch",
        "transformers",
        "sounddevice",
        "scipy",
        "numpy",
        "ollama"
    )

    try {
        Write-Host "  -> Installation en cours..." -ForegroundColor Cyan
        pip install --upgrade pip | Out-Null

        foreach ($package in $packages) {
            Write-Host "    - $package" -ForegroundColor Gray
        }

        pip install $packages 2>&1 | Out-Null

        Write-Host "  [OK] Toutes les dependances sont installees" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "  [ERREUR] Erreur lors de l'installation des packages : $_" -ForegroundColor Red
        return $false
    }
}

# ========================================
# Fonction : Vérification finale
# ========================================
function Final-Check {
    Write-Host ""
    Write-Host "[6/6] Verification finale..." -ForegroundColor Yellow

    $allGood = $true

    # Vérifier Python
    if (python --version 2>&1) {
        Write-Host "  [OK] Python" -ForegroundColor Green
    } else {
        Write-Host "  [ERREUR] Python" -ForegroundColor Red
        $allGood = $false
    }

    # Vérifier FFmpeg
    if (Test-Path "$FFMPEG_DIR\bin\ffmpeg.exe") {
        Write-Host "  [OK] FFmpeg" -ForegroundColor Green
    } else {
        Write-Host "  [ERREUR] FFmpeg" -ForegroundColor Red
        $allGood = $false
    }

    # Vérifier Redis
    if (Test-Path "$REDIS_DIR\redis-server.exe") {
        Write-Host "  [OK] Redis" -ForegroundColor Green
    } else {
        Write-Host "  [ERREUR] Redis" -ForegroundColor Red
        $allGood = $false
    }

    # Vérifier Qwen3
    if (Test-Path "$QWEN_MODEL\model.safetensors") {
        Write-Host "  [OK] Modele Qwen3" -ForegroundColor Green
    } else {
        Write-Host "  [ATTENTION] Modele Qwen3 (optionnel pour le test)" -ForegroundColor Yellow
    }

    # Vérifier les packages Python
    try {
        python -c "import flask, flask_socketio, flask_cors, faster_whisper, torch, transformers" 2>&1 | Out-Null
        Write-Host "  [OK] Packages Python" -ForegroundColor Green
    } catch {
        Write-Host "  [ERREUR] Packages Python" -ForegroundColor Red
        $allGood = $false
    }

    return $allGood
}

# ========================================
# Fonction : Instructions finales
# ========================================
function Show-FinalInstructions {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "   Installation Terminee !             " -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Pour lancer Milo :" -ForegroundColor Cyan
    Write-Host "  1. Lancez Redis (terminal 1) :" -ForegroundColor White
    Write-Host "     C:\Redis\redis-server.exe" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. Lancez Milo (terminal 2) :" -ForegroundColor White
    Write-Host "     cd milo_ai-main" -ForegroundColor Gray
    Write-Host "     python src\back_launcher.py" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  3. Attendez le message 'Qwen3 model loaded successfully'" -ForegroundColor White
    Write-Host "  4. Ouvrez votre navigateur : http://127.0.0.1:5001" -ForegroundColor White
    Write-Host ""
    Write-Host "Le premier demarrage peut prendre 1-2 minutes." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Pour plus d'aide, consultez SETUP.md ou README.md" -ForegroundColor Gray
    Write-Host ""
}

# ========================================
# SCRIPT PRINCIPAL
# ========================================

# Vérifier si on est dans le bon dossier
if (-not (Test-Path "src\back_launcher.py")) {
    Write-Host "ERREUR : Ce script doit etre execute depuis le dossier milo_ai-main" -ForegroundColor Red
    Write-Host "Dossier actuel : $PROJECT_DIR" -ForegroundColor Gray
    exit 1
}

# Exécuter les étapes
$step1 = Check-Python
if (-not $step1) {
    Write-Host ""
    Write-Host "Installation interrompue. Veuillez installer Python et relancer ce script." -ForegroundColor Red
    exit 1
}

$step2 = Install-FFmpeg
if (-not $step2) {
    Write-Host ""
    Write-Host "Installation interrompue. Erreur lors de l'installation de FFmpeg." -ForegroundColor Red
    exit 1
}

$step3 = Install-Redis
if (-not $step3) {
    Write-Host ""
    Write-Host "Installation interrompue. Erreur lors de l'installation de Redis." -ForegroundColor Red
    exit 1
}

$step4 = Check-Qwen3
if (-not $step4) {
    Write-Host ""
    Write-Host "Installation interrompue. Le modele Qwen3 est requis." -ForegroundColor Red
    exit 1
}

$step5 = Install-PythonPackages
if (-not $step5) {
    Write-Host ""
    Write-Host "Installation interrompue. Erreur lors de l'installation des packages Python." -ForegroundColor Red
    exit 1
}

$finalCheck = Final-Check
if ($finalCheck) {
    Show-FinalInstructions
} else {
    Write-Host ""
    Write-Host "Installation incomplete. Veuillez corriger les erreurs ci-dessus." -ForegroundColor Red
    exit 1
}
