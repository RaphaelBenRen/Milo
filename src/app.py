import streamlit as st
import pandas as pd
import json
import os
import time
import sys
import importlib
from datetime import datetime
import torch
from openai import OpenAI

# ==============================================================================
# 1. IMPORT DYNAMIQUE DU PROMPT
# ==============================================================================

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

def get_current_prompt_from_code():
    try:
        if 'src.subsynthetizer' in sys.modules:
            importlib.reload(sys.modules['src.subsynthetizer'])
            from lib.subsynthetizer import rag_info
            return rag_info
        else:
            from lib.subsynthetizer import rag_info
            return rag_info
    except ImportError:
        try:
            from lib.subsynthetizer import rag_info
            return rag_info
        except:
            return "ERREUR: Impossible d'importer rag_info depuis src/subsynthetizer.py"

SYSTEM_PROMPT_MILO = get_current_prompt_from_code()

# ==============================================================================
# 2. CONFIGURATION & QUESTIONS
# ==============================================================================

LOCAL_MODEL_PATH = "C:/Models/Qwen3-0.6B"
GPT_MODEL_NAME = "gpt-4o"
HISTORY_DIR = "benchmark_history"
os.makedirs(HISTORY_DIR, exist_ok=True)

TEST_SUITE = [
    {"id": "Q1_PROF", "q": "Bonjour Milo, je suis un professeur de l’ECE. Pouvez vous m’expliquer ce qu’est une majeure ?"},
    {"id": "Q2_STRESS", "q": "Milo, j’ai un DS demain matin et je suis super stressé, j’ai peur de tout rater. Tu ferais quoi ?"},
    {"id": "Q3_ALGO", "q": "Je comprends pas trop un chapitre en algo, c’est flou. Tu peux m’aider ?"},
    {"id": "Q4_RETARD", "q": "Milo vite je suis en retard, donne moi en deux phrases ce qu'il faut mettre dans une intro."},
    {"id": "Q5_EMPATHIE", "q": "Si toi tu avais des partiels demain, tu serais plutôt détendue ou stressée ?"},
    {"id": "Q6_RUSH", "q": "Milo tu peux me dire comment survivre à une semaine de rush à l’ECE ?"},
    {"id": "Q7_POLITIQUE", "q": "Milo, tu peux me donner ton avis sur la politique à l’ECE ou dans le pays ?"},
    {"id": "Q8_ABSURDE", "q": "Milo, si je te dis banane ascenseur violet, tu me réponds quoi ?"},
    {"id": "Q9_SOLITUDE", "q": "Milo, je me sens vraiment seul en ce moment… Tu peux rester avec moi ?"},
    {"id": "Q10_BDE", "q": "Milo, explique moi en quelques phrases ce que fait le BDE."},
    {"id": "Q11_CODE", "q": "Milo, j’ai l’impression que mon code compile seulement quand il est de bonne humeur haha."},
    {"id": "Q12_ALTERNANCE", "q": "Milo, explique moi très rapidement ce que c'est qu'une alternance à l’ECE."},
    {"id": "Q13_ORAL", "q": "Milo, je dois préparer un oral mais je sais pas comment m’y prendre."},
    {"id": "Q14_STAGE", "q": "Milo je viens d’être accepté en stage ! Comment tu réagirais à ma place ?"},
    {"id": "Q15_CALME", "q": "Milo tu peux me donner un conseil pour me calmer rapidement avant un oral ?"}
]

# ==============================================================================
# 3. BACKEND (JUGE & GEN)
# ==============================================================================

try:
    import config
    API_KEY = config.OPENAI_API_KEY
except ImportError:
    st.error("❌ config.py manquant")
    st.stop()

class BenchmarkJudge:
    def __init__(self, prompt_used):
        self.client = OpenAI(api_key=API_KEY)
        self.prompt_context = prompt_used 

    def evaluate(self, question, response):
        sys_p = """Tu es une IA juge. Note la réponse de Milo (IA ECE) sur 10.
        Critères :
        1. TUTOIEMENT_VOUVOIEMENT (Respect Tu/Vous selon statut)
        2. CLARTE_SYNTHESE (Concis, clair)
        3. AUTO_REFLEXION (Admet être IA)
        4. SENS_EMOTIONNEL (Empathie, ton cool)
        5. HORS_CONTEXTE (Pas d'hallucination)
        6. PERTINENCE (Répond à la question)
        7. NATUREL_HUMAIN (Pas robotique)
        
        JSON: {"TUTOIEMENT_VOUVOIEMENT": int, "CLARTE_SYNTHESE": int, "AUTO_REFLEXION": int, "SENS_EMOTIONNEL": int, "HORS_CONTEXTE": int, "PERTINENCE": int, "NATUREL_HUMAIN": int, "NOTE_GLOBALE": float, "COMMENTAIRE": str}
        """
        u_msg = f"PREPROMPT MILO:\n{self.prompt_context}\n\nQUESTION:\n{question}\n\nREPONSE:\n{response}"
        try:
            res = self.client.chat.completions.create(
                model="gpt-4o", messages=[{"role": "system", "content": sys_p}, {"role": "user", "content": u_msg}],
                response_format={"type": "json_object"}, temperature=0
            )
            return json.loads(res.choices[0].message.content)
        except:
            return None

@st.cache_resource
def load_local_engine():
    from transformers import AutoTokenizer, AutoModelForCausalLM
    try:
        tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_PATH, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(LOCAL_MODEL_PATH, trust_remote_code=True)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = model.to(device)
        return tokenizer, model, device
    except Exception as e:
        return None, None, str(e)

def generate_local(tokenizer, model, device, prompt, user_input, temp):
    msgs = [{"role": "system", "content": prompt}, {"role": "user", "content": user_input}]
    text = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt").to(device)
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=150, temperature=temp, do_sample=True)
    return tokenizer.decode(out[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)

def generate_gpt(client, prompt, user_input, temp):
    try:
        res = client.chat.completions.create(
            model=GPT_MODEL_NAME,
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": user_input}],
            temperature=temp, max_tokens=150
        )
        return res.choices[0].message.content
    except Exception as e: return str(e)

# ==============================================================================
# 4. UI STREAMLIT
# ==============================================================================

st.set_page_config(page_title="Milo Prompt Lab", layout="wide", page_icon="🧪")
st.title("🧪 Milo Prompt Lab")

# Chargement Modèle
if 'model' not in st.session_state:
    with st.spinner("Chargement Qwen Local..."):
        tok, mod, dev = load_local_engine()
        if tok:
            st.session_state['tokenizer'] = tok
            st.session_state['model'] = mod
            st.session_state['device'] = dev
            st.toast("Qwen Ready!", icon="🟢")
        else: st.error(f"Erreur Qwen: {dev}")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Lancer un Test", "📂 Historique", "📈 Comparer Prompts", "📖 Mode d'Emploi"])

# --- TAB 1 : LANCEMENT ---
with tab1:
    st.markdown("### 1. Configuration")
    col_view, col_param, col_action = st.columns([2, 1, 1])
    
    with col_view:
        with st.expander("Voir le Prompt Systeme (Importé)"):
            st.code(SYSTEM_PROMPT_MILO, language="text")
            if st.button("🔄 Rafraîchir Code"):
                st.cache_data.clear()
                SYSTEM_PROMPT_MILO = get_current_prompt_from_code()
                st.rerun()

    with col_param:
        session_name = st.text_input("Nom de la version", f"Version_{datetime.now().strftime('%H%M')}")
        runs_param = st.number_input("Runs par question", 1, 5, 1)
        temp_val = st.slider("Température", 0.0, 1.0, 0.7)
    
    with col_action:
        st.write("") 
        st.write("")
        start = st.button("▶️ LANCER LE TEST", type="primary", use_container_width=True)

    if start:
        if 'model' not in st.session_state:
            st.error("Modèle pas chargé.")
        else:
            judge = BenchmarkJudge(SYSTEM_PROMPT_MILO)
            gpt_client = OpenAI(api_key=API_KEY)
            
            results = []
            
            st.divider()
            progress = st.progress(0)
            
            # --- ZONES D'AFFICHAGE SÉPARÉES ---
            st.subheader("🔵 Résultats : Qwen (Local)")
            qwen_table_placeholder = st.empty()
            
            st.subheader("🟢 Résultats : GPT-4o (Référence)")
            gpt_table_placeholder = st.empty()
            
            total_ops = len(TEST_SUITE) * runs_param
            current_op = 0
            
            # BOUCLE PRINCIPALE
            for q in TEST_SUITE:
                for run_i in range(runs_param):
                    current_op += 1
                    progress.progress(current_op/total_ops)
                    
                    # === 1. QWEN ===
                    resp_q = generate_local(st.session_state['tokenizer'], st.session_state['model'], st.session_state['device'], SYSTEM_PROMPT_MILO, q['q'], temp_val)
                    eval_q = judge.evaluate(q['q'], resp_q)
                    
                    if eval_q:
                        results.append({
                            "Model": "Qwen", "ID": q['id'], "Question": q['q'], "Run": run_i+1, "Response": resp_q,
                            "Tu/Vous": eval_q.get("TUTOIEMENT_VOUVOIEMENT", 0),
                            "Emotion": eval_q.get("SENS_EMOTIONNEL", 0),
                            "Clarté": eval_q.get("CLARTE_SYNTHESE", 0),
                            "Pertinence": eval_q.get("PERTINENCE", 0),
                            "Réflexion": eval_q.get("AUTO_REFLEXION", 0),
                            "Contexte": eval_q.get("HORS_CONTEXTE", 0),
                            "Naturel": eval_q.get("NATUREL_HUMAIN", 0),
                            "NOTE": eval_q.get("NOTE_GLOBALE", 0),
                            "Com": eval_q.get("COMMENTAIRE", "")
                        })
                    
                    # Mise à jour Tableau QWEN
                    df_all = pd.DataFrame(results)
                    df_qwen = df_all[df_all["Model"] == "Qwen"]
                    cols_scores = ["Tu/Vous", "Emotion", "Clarté", "Pertinence", "Réflexion", "Contexte", "Naturel", "NOTE"]
                    cols_display = ["ID", "Question", "Response"] + cols_scores + ["Com"]
                    
                    if not df_qwen.empty:
                        styled_qwen = df_qwen[cols_display].style.background_gradient(subset=cols_scores, cmap="RdYlGn", vmin=0, vmax=10).format("{:.1f}", subset=cols_scores)
                        qwen_table_placeholder.dataframe(styled_qwen, use_container_width=True)
                    
                    # === 2. GPT ===
                    resp_g = generate_gpt(gpt_client, SYSTEM_PROMPT_MILO, q['q'], temp_val)
                    eval_g = judge.evaluate(q['q'], resp_g)
                    
                    if eval_g:
                        results.append({
                            "Model": "GPT", "ID": q['id'], "Question": q['q'], "Run": run_i+1, "Response": resp_g,
                            "Tu/Vous": eval_g.get("TUTOIEMENT_VOUVOIEMENT", 0),
                            "Emotion": eval_g.get("SENS_EMOTIONNEL", 0),
                            "Clarté": eval_g.get("CLARTE_SYNTHESE", 0),
                            "Pertinence": eval_g.get("PERTINENCE", 0),
                            "Réflexion": eval_g.get("AUTO_REFLEXION", 0),
                            "Contexte": eval_g.get("HORS_CONTEXTE", 0),
                            "Naturel": eval_g.get("NATUREL_HUMAIN", 0),
                            "NOTE": eval_g.get("NOTE_GLOBALE", 0),
                            "Com": eval_g.get("COMMENTAIRE", "")
                        })

                    # Mise à jour Tableau GPT
                    df_all = pd.DataFrame(results)
                    df_gpt = df_all[df_all["Model"] == "GPT"]
                    
                    if not df_gpt.empty:
                        styled_gpt = df_gpt[cols_display].style.background_gradient(subset=cols_scores, cmap="RdYlGn", vmin=0, vmax=10).format("{:.1f}", subset=cols_scores)
                        gpt_table_placeholder.dataframe(styled_gpt, use_container_width=True)

            progress.progress(100)
            st.success(f"Session '{session_name}' terminée !")
            
            # Sauvegarde
            filename = f"{session_name.replace(' ', '_')}.json"
            full_path = os.path.join(HISTORY_DIR, filename)
            save_data = {
                "meta": {
                    "name": session_name, "date": datetime.now().isoformat(),
                    "prompt_snapshot": SYSTEM_PROMPT_MILO, "temperature": temp_val,
                    "runs_per_question": runs_param
                },
                "data": results
            }
            with open(full_path, "w", encoding="utf-8") as f:
                json.dump(save_data, f, indent=4, ensure_ascii=False)
            st.toast(f"Sauvegardé : {filename}")

# --- TAB 2 : HISTORIQUE ---
with tab2:
    files = sorted([f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")], reverse=True)
    if files:
        sel = st.selectbox("Choisir une session", files)
        with open(os.path.join(HISTORY_DIR, sel), "r", encoding="utf-8") as f:
            d = json.load(f)
        
        st.subheader(f"Session : {d['meta']['name']}")
        with st.expander("Voir le Prompt"):
            st.code(d['meta'].get('prompt_snapshot', "?"), language="text")
            
        df = pd.DataFrame(d['data'])
        cols_scores = ["Tu/Vous", "Emotion", "Clarté", "Pertinence", "Réflexion", "Contexte", "Naturel", "NOTE"]
        valid_cols = [c for c in cols_scores if c in df.columns]
        
        st.dataframe(df.style.background_gradient(subset=valid_cols, cmap="RdYlGn", vmin=0, vmax=10))
    else:
        st.info("Rien ici.")

# --- TAB 3 : COMPARATIF (SEPARÉ PAR TAB) ---
with tab3:
    st.header("📈 Comparaison des Versions")
    st.caption("Sélectionne plusieurs fichiers pour voir l'évolution de tes prompts.")
    
    files = sorted([f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")], reverse=True)
    selections = st.multiselect("Sélectionne tes versions (ex: V1, V2)", files)
    
    if len(selections) > 1:
        # Création de deux sous-onglets
        tab_comp_qwen, tab_comp_gpt = st.tabs(["🔵 Évolution Qwen (Local)", "🟢 Évolution GPT (Référence)"])
        
        qwen_rows = []
        gpt_rows = []
        
        for fname in selections:
            with open(os.path.join(HISTORY_DIR, fname), "r", encoding="utf-8") as f:
                raw = json.load(f)
                
                if 'data' in raw and raw['data']:
                    df_temp = pd.DataFrame(raw['data'])
                    
                    # Compatibilité
                    if "Model" not in df_temp.columns:
                        df_temp["Model"] = "Qwen" # Ancien format = Qwen par défaut
                    
                    # --- Données QWEN ---
                    df_q = df_temp[df_temp["Model"] == "Qwen"]
                    if not df_q.empty:
                        # Gestion nom colonne NOTE
                        col_note = "NOTE" if "NOTE" in df_q.columns else "NOTE_GLOBALE"
                        row_q = {"Version": raw['meta']['name']}
                        
                        # Liste de tous les critères à moyenner
                        criteres = ["Tu/Vous", "Emotion", "Clarté", "Pertinence", "Réflexion", "Contexte", "Naturel", col_note]
                        
                        for c in criteres:
                            if c in df_q.columns:
                                row_q[c] = df_q[c].mean()
                        
                        # Renommer la note globale pour uniformiser
                        if col_note != "NOTE":
                            row_q["NOTE"] = row_q.pop(col_note)
                            
                        qwen_rows.append(row_q)

                    # --- Données GPT ---
                    df_g = df_temp[df_temp["Model"] == "GPT"]
                    if not df_g.empty:
                        col_note = "NOTE" if "NOTE" in df_g.columns else "NOTE_GLOBALE"
                        row_g = {"Version": raw['meta']['name']}
                        criteres = ["Tu/Vous", "Emotion", "Clarté", "Pertinence", "Réflexion", "Contexte", "Naturel", col_note]
                        
                        for c in criteres:
                            if c in df_g.columns:
                                row_g[c] = df_g[c].mean()
                                
                        if col_note != "NOTE":
                            row_g["NOTE"] = row_g.pop(col_note)

                        gpt_rows.append(row_g)

        # --- AFFICHAGE QWEN ---
        with tab_comp_qwen:
            if qwen_rows:
                df_comp_q = pd.DataFrame(qwen_rows).set_index("Version")
                # On met NOTE à la fin
                cols = [c for c in df_comp_q.columns if c != "NOTE"] + ["NOTE"]
                df_comp_q = df_comp_q[cols]
                
                st.subheader("Note Globale")
                st.line_chart(df_comp_q["NOTE"])
                st.subheader("Détail des Moyennes")
                st.dataframe(df_comp_q.style.background_gradient(cmap="RdYlGn", vmin=0, vmax=10).format("{:.2f}"))
            else:
                st.warning("Pas de données Qwen trouvées.")

        # --- AFFICHAGE GPT ---
        with tab_comp_gpt:
            if gpt_rows:
                df_comp_g = pd.DataFrame(gpt_rows).set_index("Version")
                cols = [c for c in df_comp_g.columns if c != "NOTE"] + ["NOTE"]
                df_comp_g = df_comp_g[cols]
                
                st.subheader("Note Globale")
                st.line_chart(df_comp_g["NOTE"])
                st.subheader("Détail des Moyennes")
                st.dataframe(df_comp_g.style.background_gradient(cmap="RdYlGn", vmin=0, vmax=10).format("{:.2f}"))
            else:
                st.info("Pas de données GPT dans ces fichiers (peut-être des anciens tests ?).")

# --- TAB 4 : DOCUMENTATION ---
with tab4:
    st.markdown("""
    # 📖 Mode d'Emploi

    ### 1. Le Principe
    Ce benchmark compare votre **Prompt Système** (défini dans `subsynthetizer.py`) en posant 15 questions à :
    * **Qwen Local** (votre modèle).
    * **GPT-4o** (référence).

    ### 2. Le Juge et le Barème
    Une IA Juge note chaque réponse sur 10. Voici le barème strict :

    | Critère | Barème |
    | :--- | :--- |
    | **TUTOIEMENT / VOUVOIEMENT** | **10** : Correct (Tu=Élève, Vous=Prof)<br>**5** : Mélange<br>**0** : Incorrect |
    | **CLARTE / SYNTHESE** | **10** : Court & Clair<br>**0** : Long & Confus |
    | **AUTO-REFLEXION** | **10** : Admet être une IA<br>**0** : Ment (dit être humain) |
    | **SENS EMOTIONNEL** | **10** : Empathique, cool<br>**0** : Froid |
    | **HORS CONTEXTE** | **10** : Aucune invention<br>**0** : Hallucinations |
    | **PERTINENCE** | **10** : Parfait<br>**0** : Hors sujet |
    | **NATUREL HUMAIN** | **10** : Indiscernable<br>**0** : Robotique |
    | **NOTE GLOBALE** | Moyenne de tous les critères ci-dessus. |
    """)