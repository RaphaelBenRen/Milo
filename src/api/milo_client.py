from openai import OpenAI
import os

# Gestion des imports selon le dossier d'exécution
try:
    from config import MILO_API_KEY, MILO_API_URL, MILO_MODEL_NAME
except ImportError:
    from ..config import MILO_API_KEY, MILO_API_URL, MILO_MODEL_NAME

# Client compatible OpenAI (pour Ollama, vLLM, Together, etc.)
client = OpenAI(
    base_url=MILO_API_URL,
    api_key=MILO_API_KEY
)

def generate_milo_response(system_prompt: str, user_message: str) -> str:
    """
    Connecte l'interface à l'IA Milo pour générer une réponse.
    """
    try:
        completion = client.chat.completions.create(
            model=MILO_MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,      # Un peu de créativité pour le naturel
            max_tokens=200,       # Pas de roman, on veut de la synthèse
            top_p=0.9
        )
        return completion.choices[0].message.content.strip()

    except Exception as e:
        return f"[ERREUR CONNECTION MILO] : Impossible de contacter le modèle sur {MILO_API_URL}. Erreur : {e}"