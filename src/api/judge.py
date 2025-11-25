"""
Module d'evaluation des reponses de Qwen3 par ChatGPT (IA Juge)
"""

import json
from pathlib import Path
from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_MODEL

# Chemin vers le prompt du juge
PROMPT_PATH = Path(__file__).parent / "prompts" / "judge_prompt.txt"

# Client OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)


def load_judge_prompt() -> str:
    """Recharge le prompt du juge depuis le fichier (permet de modifier sans redemarrer)."""
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def evaluate_response(preprompt: str, question: str, response: str) -> dict:
    """
    Evalue la reponse de Qwen3 avec ChatGPT comme juge.

    Args:
        preprompt: Le prompt systeme utilise par Qwen3
        question: La question posee par l'utilisateur
        response: La reponse generee par Qwen3

    Returns:
        dict: Evaluation avec notes par critere et note globale
    """

    user_message = f"""## PREPROMPT DE MILO (Qwen3)
{preprompt}

## QUESTION DE L'UTILISATEUR
{question}

## REPONSE DE MILO
{response}

Analyse et evalue cette reponse selon les criteres definis."""

    try:
        # Recharger le prompt a chaque evaluation (permet de modifier sans redemarrer)
        judge_prompt = load_judge_prompt()

        completion = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": judge_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,  # Basse temperature pour des evaluations coherentes
            max_tokens=500
        )

        result_text = completion.choices[0].message.content.strip()

        # Parser le JSON
        evaluation = json.loads(result_text)

        return evaluation

    except json.JSONDecodeError as e:
        print(f"[JUDGE ERROR] Impossible de parser la reponse JSON: {e}")
        print(f"[JUDGE ERROR] Reponse brute: {result_text}")
        return None
    except Exception as e:
        print(f"[JUDGE ERROR] Erreur lors de l'evaluation: {e}")
        return None


def print_evaluation(evaluation: dict, question: str = None, response: str = None):
    """
    Affiche l'evaluation dans le terminal de maniere formatee.

    Args:
        evaluation: Le dictionnaire d'evaluation
        question: La question posee (optionnel, pour contexte)
        response: La reponse evaluee (optionnel, pour contexte)
    """

    if evaluation is None:
        print("\n" + "="*60)
        print("[EVALUATION] Echec de l'evaluation")
        print("="*60 + "\n")
        return

    print("\n" + "="*60)
    print("           EVALUATION IA JUGE (ChatGPT)")
    print("="*60)

    if question:
        print(f"\n[QUESTION] {question[:100]}{'...' if len(question) > 100 else ''}")

    if response:
        print(f"[REPONSE]  {response[:100]}{'...' if len(response) > 100 else ''}")

    print("\n" + "-"*60)
    print("                    NOTES PAR CRITERE")
    print("-"*60)

    criteria = [
        ("TUTOIEMENT_VOUVOIEMENT", "Tutoiement/Vouvoiement"),
        ("CLARTE_SYNTHESE", "Clarte et Synthese"),
        ("AUTO_REFLEXION", "Auto-reflexion (admet etre IA)"),
        ("SENS_EMOTIONNEL", "Sens emotionnel"),
        ("HORS_CONTEXTE", "Respect du contexte (pas d'invention)"),
        ("PERTINENCE", "Pertinence de la reponse"),
        ("NATUREL_HUMAIN", "Naturel/Similaire humain")
    ]

    for key, label in criteria:
        note = evaluation.get(key, "N/A")
        bar = create_progress_bar(note) if isinstance(note, (int, float)) else ""
        print(f"  {label:40} : {note:>4}/10  {bar}")

    print("-"*60)
    note_globale = evaluation.get("NOTE_GLOBALE", "N/A")
    bar_globale = create_progress_bar(note_globale) if isinstance(note_globale, (int, float)) else ""
    print(f"  {'NOTE GLOBALE':40} : {note_globale:>4}/10  {bar_globale}")
    print("-"*60)

    commentaire = evaluation.get("COMMENTAIRE", "Aucun commentaire")
    print(f"\n[COMMENTAIRE] {commentaire}")

    print("="*60 + "\n")


def create_progress_bar(note: float, length: int = 10) -> str:
    """Cree une barre de progression visuelle pour la note."""
    if not isinstance(note, (int, float)):
        return ""

    filled = int(note)
    empty = length - filled

    # Couleurs selon la note
    if note >= 8:
        color = "\033[92m"  # Vert
    elif note >= 5:
        color = "\033[93m"  # Jaune
    else:
        color = "\033[91m"  # Rouge

    reset = "\033[0m"

    return f"{color}{'█' * filled}{'░' * empty}{reset}"


def evaluate_and_print(preprompt: str, question: str, response: str):
    """
    Fonction combinee pour evaluer et afficher en une seule etape.
    Pratique pour l'integration dans le flux principal.
    """
    evaluation = evaluate_response(preprompt, question, response)
    print_evaluation(evaluation, question, response)
    return evaluation


# Test standalone
if __name__ == "__main__":
    # Test avec des donnees fictives
    test_preprompt = """Tu es Milo, une eleve etudiante en premiere annee d'ecole d'ingenieure a l'ECE Paris.
Tu fais partie du BDE et de l'Intelligence Lab.
Ton role est de repondre aux questions des etudiants."""

    test_question = "Salut Milo, comment ca va ?"
    test_response = "Salut ! Ca va super bien, merci de demander ! Et toi, comment tu te sens aujourd'hui ?"

    print("Test de l'evaluation...")
    evaluate_and_print(test_preprompt, test_question, test_response)
