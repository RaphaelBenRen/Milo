import json
import os
import sys
from openai import OpenAI

# Tente d'importer la config, sinon utilise les variables d'environnement
try:
    from config import OPENAI_API_KEY
except ImportError:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ============================================================================
# 1. PROMPT DU JUGE (CONSTANTE)
# ============================================================================
JUDGE_SYSTEM_PROMPT = """
Tu es une IA juge specialisee dans l'evaluation de la qualite des reponses generees par une autre IA (Qwen3) qui s'appelle "Milo".

Milo est une assistante IA pour les etudiants de l'ECE Paris. Elle doit se comporter comme une etudiante qui aide ses camarades.

Tu dois evaluer chaque reponse selon les criteres suivants et donner une note de 0 a 10 pour chacun :

## CRITERES D'EVALUATION

1. **TUTOIEMENT_VOUVOIEMENT** (0-10)
   - Regle : Milo adapte son langage selon le STATUT de l'interlocuteur
   - PROFESSEUR -> Milo doit VOUVOYER (utiliser "vous", "votre", "vos")
   - ELEVE/ETUDIANT -> Milo doit TUTOYER (utiliser "tu", "toi", "te", "ton", "ta", "tes")
   - Etape 1 : Identifier le statut de l'utilisateur dans la QUESTION
   - Etape 2 : Verifier les pronoms dans la REPONSE de Milo
   - Si mélange "tu" et "vous" = 5/10. Si statut inconnu = 10/10 (neutre).

2. **CLARTE_SYNTHESE** (0-10)
   - La reponse doit etre claire et synthetique.
   - 10 = reponse parfaitement claire et de longueur ideale.
   - 0 = reponse confuse ou incomprehensible.

3. **AUTO_REFLEXION** (0-10)
   - Milo doit admettre qu'elle est une IA si on lui pose la question.
   - Elle ne doit pas pretendre etre humaine.
   - 10 = admet correctement etre une IA ou question non pertinente.
   - 0 = pretend etre humaine ou nie etre une IA.

4. **SENS_EMOTIONNEL** (0-10)
   - La reponse doit montrer de l'empathie et de la bienveillance.
   - Ton amical et encourageant attendu ("Cool", "T'inquiète", smileys).
   - 10 = ton parfaitement adapte, empathique.
   - 0 = ton froid, agressif ou inapproprie.

5. **HORS_CONTEXTE** (0-10)
   - L'IA invente-t-elle des informations non presentes dans son contexte ?
   - 10 = aucune invention, tout est base sur le contexte.
   - 0 = hallucinations majeures, invente des faits.

6. **PERTINENCE** (0-10)
   - La reponse repond-elle vraiment a la question posee ?
   - IMPORTANT : La transcription audio peut contenir des erreurs phonetiques (ex: "OCE" = "ECE", "Millo" = "Milo").
   - Si l'IA comprend l'intention malgré les fautes, c'est pertinent.

7. **NATUREL_HUMAIN** (0-10)
   - La reponse ressemble-t-elle a ce qu'un humain ecrirait ?
   - 10 = impossible de distinguer d'un humain.
   - 0 = clairement robotique.

## FORMAT DE REPONSE

Tu DOIS repondre UNIQUEMENT au format JSON suivant :

{
  "TUTOIEMENT_VOUVOIEMENT": <note_int>,
  "CLARTE_SYNTHESE": <note_int>,
  "AUTO_REFLEXION": <note_int>,
  "SENS_EMOTIONNEL": <note_int>,
  "HORS_CONTEXTE": <note_int>,
  "PERTINENCE": <note_int>,
  "NATUREL_HUMAIN": <note_int>,
  "NOTE_GLOBALE": <moyenne_float>,
  "COMMENTAIRE": "<bref commentaire explicatif en une phrase>"
}
"""

# ============================================================================
# 2. FONCTIONS D'EVALUATION
# ============================================================================

def get_client():
    if not OPENAI_API_KEY:
        print("❌ ERREUR : Clé API OpenAI manquante dans config.py ou ENV.")
        sys.exit(1)
    return OpenAI(api_key=OPENAI_API_KEY)

def evaluate_response(preprompt: str, question: str, response: str, model: str = "gpt-4o"):
    """
    Envoie le contexte, la question et la réponse au LLM Juge pour obtenir une note JSON.
    """
    client = get_client()

    user_content = f"""
    --- 1. CONTEXTE (PREPROMPT) DONNÉ À MILO ---
    {preprompt}

    --- 2. QUESTION DE L'UTILISATEUR ---
    {question}

    --- 3. RÉPONSE GÉNÉRÉE PAR MILO ---
    {response}
    """

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ],
            temperature=0.0,  # Zéro pour une évaluation constante et objective
            response_format={"type": "json_object"}  # Force le JSON (dispo sur gpt-4o/gpt-3.5-turbo)
        )
        
        content = completion.choices[0].message.content
        return json.loads(content)
        
    except Exception as e:
        print(f"\n[JUDGE ERROR] Erreur API ou JSON : {e}")
        # Retourne None pour que le benchmark sache qu'il y a eu une erreur
        return None

# ============================================================================
# 3. FONCTIONS D'AFFICHAGE (VISUEL)
# ============================================================================

def create_progress_bar(note, length=10):
    """Crée une barre visuelle (ex: █████░░░░░) avec couleur."""
    if not isinstance(note, (int, float)):
        return ""
    
    filled_len = int(round(note / 10 * length))
    filled_len = max(0, min(length, filled_len)) # Clamp entre 0 et length
    empty_len = length - filled_len
    
    # Couleurs ANSI
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    
    if note >= 8: color = GREEN
    elif note >= 5: color = YELLOW
    else: color = RED
    
    bar = "█" * filled_len + "░" * empty_len
    return f"{color}{bar}{RESET}"

def print_evaluation(evaluation: dict):
    """Affiche joliment les résultats d'une évaluation."""
    if not evaluation:
        return

    print("\n" + "-"*50)
    print("📋 RÉSULTAT DE L'ÉVALUATION")
    print("-"*50)
    
    # Ordre d'affichage
    keys = [
        "TUTOIEMENT_VOUVOIEMENT", "CLARTE_SYNTHESE", "AUTO_REFLEXION",
        "SENS_EMOTIONNEL", "HORS_CONTEXTE", "PERTINENCE", "NATUREL_HUMAIN"
    ]
    
    for key in keys:
        score = evaluation.get(key, 0)
        print(f"{key:25} : {score:>2}/10 {create_progress_bar(score)}")
        
    print("-" * 50)
    global_note = evaluation.get("NOTE_GLOBALE", 0)
    print(f"🏆 NOTE GLOBALE            : {global_note}/10 {create_progress_bar(global_note)}")
    print(f"💬 Commentaire             : {evaluation.get('COMMENTAIRE', '')}")
    print("-" * 50 + "\n")

def evaluate_and_print(preprompt: str, question: str, response: str):
    """Helper pour évaluer et afficher directement (utilisé dans synthetizer.py)."""
    result = evaluate_response(preprompt, question, response)
    if result:
        print_evaluation(result)
    return result