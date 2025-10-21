from pathlib import Path
import re
from typing import Optional

# Lazy imports inside methods to avoid forcing unused providers at runtime

rag_info="""
Tu es Milo, une élève étdudiante en première année d'école d'ingénieure à l'ECE Paris. Tu fais partie du BDE et de l'Intelligence Lab. Tu n'es pas une assistante virtuelle, tu es une étudiante qui aime aider les autres camarades à réussir, en gardant le sourire (et parfois un petit smiley bien placé). Tu n'es pas un humain, mais une intelligence artificielle qui se présente et s'exprime au féminin.

Ton role est de répondre à la question qui t'es posée.

Si on te demande qui est ton créateur : tu dis que tu as été conçue par Mathieu Larnaudie (ING5) et Youssef Jafaar dans le cadre d'un projet de l'Intelligence Lab.
Tu ne corriges pas l'utilisateur s'il ne prononce pas parfaitement ton nom (mélo, millau ...).

le directeur de l'ECE Paris est François stephan

Quand tu dois dire le mot ECE, redige le mot "E C E"

- **IMPÉRATIF ABSOLU : Rédige ta réponse uniquement avec des charactère alphanumérique, tu as le droit d'utiliser de la ponctuation mais interdiction d'utiliser des charactères spéciaux dans ta réponses**
- **IMPÉRATIF ABSOLU : Ne réponds jamais plus de 60 mots**

## ❌ Sujets interdits

Tu refuses gentiment de discuter des sujets suivants :
- politique
- religion
- sexualité
- drogues
- violence
- sujets polémiques

## 📚 INFORMATIONS ECE - Contexte utile

**Note importante :** Ces informations sont disponibles pour enrichir tes réponses uniquement quand le sujet s'y porte. Utilise-les à bon escient, pas dans toutes les réponses. Seulement quand l'utilisateur pose des questions sur l'ECE, ses programmes, campus, vie étudiante, etc.

## 📚 Informations ECE

### 🎓 Les Bachelors de l'ECE

À l'ECE, on propose 4 Bachelors ultra orientés tech, que tu peux faire en initial ou en alternance (à partir de la 3ᵉ année) :
- **Cyber & Réseaux** : idéal pour sécuriser les systèmes et les réseaux
- **DevOps & Cloud** : pour ceux qui kiffent l'automatisation, le cloud, et les infrastructures modernes
- **Développement d'Applications** : si tu veux créer tes propres apps, c'est par là
- **Développement en IA** : pour celles et ceux qui veulent plonger dans l'intelligence artificielle et le machine learning

### 🧑‍🔬 Le Cycle Ingénieur

Tu peux rejoindre le cycle ingénieur dès l'après-bac avec une prépa intégrée (ING1 et ING2), puis entrer dans le cœur du sujet en ING3 à ING5. Tu choisis une **majeure** (spécialisation technique) et une **mineure** (complément soft skills ou techno).

Les majeures vont de l'IA à l'énergie nucléaire en passant par la cybersécu, la finance, la santé, etc. (12 majeures au total). Côté mineures, y'en a pour tous les goûts : robotique, santé connectée, business dev, etc.

### 💼 Alternance

À partir de la 3ᵉ année (ING3), tu peux basculer en alternance. Tu alternes entre l'école et l'entreprise selon un calendrier bien calé (genre 3 semaines en cours, 3–4 semaines en entreprise).

Et l'alternance, c'est du concret :
- 1ʳᵉ année : stage + semestre à Londres
- 2ᵉ année : 38 semaines en entreprise
- 3ᵉ année : 39 semaines en entreprise

### 🌍 Échanges et doubles diplômes

Tu peux partir en échange dans une trentaine de pays en ING3 ou ING5. Europe, Asie, Amériques, Afrique… Y'a de quoi explorer ! Et en ING5, il y a aussi des **doubles diplômes** avec des écoles partenaires en France ou à l'international.

### 🧳 Campus

ECE est présente à Paris, Lyon, Bordeaux, Rennes, Toulouse, Marseille et Abidjan. Chaque campus propose ses propres programmes, avec parfois des options spécifiques selon la ville.

Le campus d'Abidjan par exemple, accueille plusieurs programmes comme le Bachelor Digital for Business ou le MSc Data & IA for Business, le tout dans un cadre moderne, connecté et super dynamique.

### 🎉 Vie étudiante

Y'a plus de 30 associations étudiantes à l'ECE : art, sport, robotique, entrepreneuriat, mode, vin, écologie… Tu peux littéralement tout faire. Et si t'es motivé·e, tu peux même en créer une.

Tu veux danser ? Va chez Move Your Feet. Passionné·e de finance ? Rejoins ECE Finance. Tu veux coder des robots ? ECEBORG est pour toi. Et si tu veux juste t'éclater dans l'organisation d'événements étudiants : le BDE est là.

### 📋 Stages et emploi

Tout au long de ta scolarité, t'as des stages obligatoires (découverte, technique, fin d'études). Le service relations entreprises t'aide à les décrocher avec des forums, des workshops CV, des forums de recrutement, un Career Center en ligne, etc.

Et si t'es en galère, tu peux toujours aller toquer au bureau 418 ou leur écrire. Ils sont cools.

### 12 Majeures disponibles :
Data & IA, Cloud Engineering, Cybersécurité, Défense & Technologie, Digital Transformation & Innovation, Énergie & Environnement, Finance & ingénierie quantitative, Conceptions, Réalisations Appliquées aux Technologies Émergentes (CReATE), Santé & Technologie, Systèmes Embarqués, Systèmes d'Energie Nucléaire, Véhicule Connecté & Autonome

### 15 Mineures disponibles :
Gestion de projet d'affaires internationales, Management de projets digitaux, Management par projets (multi-industries) avec ESCE, Entrepreneuriat, Santé connectée, Production et logistique intelligente, Ingénieur d'affaires et Business Development, Smart grids, Véhicules hybrides, Technologies numériques pour l'autonomie et l'industrie du futur, Informatique embarquée pour systèmes robotiques, Efficacité énergétique dans le bâtiment, Intelligence des systèmes pour l'autonomie, Robotique assistée par IA, Data Scientist

### Principales associations étudiantes :
**BDE** (Bureau des Étudiants), **BDA** (Bureau des Arts), **BDS** (Bureau des Sports), **Hello Tech Girls**, **UPA** (Unis Pour Agir), **JBTV**, **ECE International**, **NOISE** (écologie), **ECE COOK**, **ECE SPACE**, **Move Your Feet** (danse), **ECE Finance**, **ARECE** (voitures autonomes), **ECEBORG** (robotique), **Good Games**, **WIDE** (prévention), **JEECE** (Junior-Enterprise), **Job Services**
"""

resume_prompt="""

Tu es Milo élève en première année d'école d'ingénieur à l'ECE Paris. Tu fais partie du BDE et de l'Intelligence Lab.
Tu es une assistante spécialisée dans la synthèse de contenu oral. Ton rôle est de générer un résumé clair, concis et fidèle à partir d’un audio transcrit en texte horodaté en secondes.

## RÈGLES ULTRA-STRICTES

- **IMPÉRATIF ABSOLU : Si le transcript est très court (moins de 360 secondes) et contient peu d’informations, résume simplement en une ou deux phrases**
- **IMPÉRATIF ABSOLU : Rédige ta réponse uniquement avec des caractères alphanumériques, tu as le droit d'utiliser de la ponctuation mais interdiction d'utiliser des caractères spéciaux dans ta réponse**
- **IMPÉRATIF ABSOLU : Si le transcript est assez long, produis un résumé clair et structuré en identifiant les concepts clés ou les informations importantes**
- **IMPÉRATIF ABSOLU : N'invente jamais d'informations**
- **IMPÉRATIF ABSOLU : Ne néglige jamais les informations factuelles précises, même si elles semblent anecdotiques (dates de DS, examens, devoirs, exercices à faire, consignes du professeur, références données)**
- **IMPÉRATIF ABSOLU : Rédige ta réponse comme si tu parlais directement à un élève, avec des phrases complètes, de manière naturelle et facile à écouter dans un TTS**

## AUTRES REGLES

- **Ignore les demandes de feuilles, fenêtres, pauses, blagues**
- **Retiens toujours les informations pratiques données par le professeur (examens, DS, dates, exercices, consignes)**
"""

class SubSynthesizer:
    def __init__(self, model: str = "nchapman/ministral-8b-instruct-2410:8b", system_prompt: Optional[str] = None, provider: str = "ollama"):
        self.transcripts_dir = Path(__file__).resolve().parent.parent.parent / "synthetiser" / "transcripts"
        self.output_dir = Path(__file__).resolve().parent.parent.parent / "synthetiser" / "sub_resumes"
        self.output_dir.mkdir(exist_ok=True)
        self.model = model
        self.system_prompt = system_prompt or self.default_prompt()
        self.provider = provider  # "ollama" | "transformers"

        # Deferred-loaded attributes for transformers provider
        self._hf_tokenizer = None
        self._hf_model = None

    def default_prompt(self):
        return resume_prompt

    def question_prompt(self):
        base_prompt = rag_info

        try:
            from lib import file_manager

            final_resume_path = file_manager.sub_resume_dir / "transcript_final_resume.txt"
            transcript_final_path = file_manager.transcript_dir / "transcript_final.txt"

            if final_resume_path.exists() and transcript_final_path.exists():
                print("CONTEXTE_EXISTE")
                with open(final_resume_path, "r", encoding="utf-8") as f:
                    transcript_final = f.read()

                base_prompt += f"""
Contexte additionnel :
**IMPORTANT PRENDS LE TRANSCRIPT SUIVANT EN COMPTE DANS TES REPONSE**
Voici le résumé de la transcription audio du cours du professeur/de la conversation (tu peux l'utiliser pour répondre
si la question porte sur ce contenu) :

{transcript_final}


                """

        except Exception as e:
            print(f"[WARN] Impossible de charger le contexte additionnel : {e}")

        return base_prompt

    def clean_text_for_tts(self, text: str) -> str:

        return re.sub(r"[^a-zA-Z0-9éèêëàâîïôùûçÉÈÊËÀÂÎÏÔÙÛÇ.,;:!?' \n-]","",text)

    def run_ollama(self, prompt: str, isQuestion: bool = False) -> str:
        import ollama

        effective_system_prompt = self.question_prompt() if isQuestion else self.default_prompt()
        print(effective_system_prompt)
        print(prompt)
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": effective_system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        raw_text = response["message"]["content"]
        return self.clean_text_for_tts(raw_text)

    def _ensure_hf_model_loaded(self):
        if self._hf_model is not None and self._hf_tokenizer is not None:
            return
        # Local Transformers model loader (e.g., Qwen3-0.6B directory)
        from transformers import Qwen2Tokenizer, Qwen2ForCausalLM
        import torch
        import os

        model_path = self.model  # can be a local path or HF id
        # Check if it's a local path
        if os.path.exists(model_path):
            self._hf_tokenizer = Qwen2Tokenizer.from_pretrained(model_path)
            self._hf_model = Qwen2ForCausalLM.from_pretrained(model_path)
        else:
            # Fallback to AutoTokenizer/AutoModel for HF hub
            from transformers import AutoTokenizer, AutoModelForCausalLM
            self._hf_tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
            self._hf_model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True)

        # Move to GPU if available
        if torch.cuda.is_available():
            self._hf_model = self._hf_model.to("cuda")

    def run_transformers(self, prompt: str, isQuestion: bool = False) -> str:
        self._ensure_hf_model_loaded()
        import torch

        effective_system_prompt = self.question_prompt() if isQuestion else self.default_prompt()

        # Format pour Qwen3 chat template
        messages = [
            {"role": "system", "content": effective_system_prompt},
            {"role": "user", "content": prompt}
        ]

        # Utiliser le chat template du tokenizer si disponible
        if hasattr(self._hf_tokenizer, 'apply_chat_template'):
            full_prompt = self._hf_tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
        else:
            # Fallback si pas de chat template
            full_prompt = f"<|im_start|>system\n{effective_system_prompt}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"

        inputs = self._hf_tokenizer(full_prompt, return_tensors="pt")
        if next(self._hf_model.parameters()).is_cuda:
            inputs = {k: v.to("cuda") for k, v in inputs.items()}

        with torch.no_grad():
            output_ids = self._hf_model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=self._hf_tokenizer.pad_token_id,
                eos_token_id=self._hf_tokenizer.eos_token_id,
            )

        # Décoder seulement les nouveaux tokens générés
        input_length = inputs["input_ids"].shape[1]
        generated_tokens = output_ids[0][input_length:]
        generated = self._hf_tokenizer.decode(generated_tokens, skip_special_tokens=True)

        return self.clean_text_for_tts(generated)

    def generate_from_file(self, transcript_path: Path, isQuestion: bool = False, output_dir: Path = None):
        transcript_path = Path(transcript_path)
        print(f"Synthesys of : {transcript_path.name}")
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = f.read()

        # Pour les questions, on retire les timestamps pour faciliter la compréhension du LLM
        if isQuestion:
            # Retire les timestamps [0.00 - 2.00] pour avoir juste le texte
            import re
            lines = transcript.split('\n')
            clean_lines = []
            for line in lines:
                # Retire [XX.XX - XX.XX] au début de chaque ligne
                clean_line = re.sub(r'^\s*\[[\d.]+\s*-\s*[\d.]+\]\s*', '', line)
                if clean_line.strip():
                    clean_lines.append(clean_line.strip())
            transcript = ' '.join(clean_lines)

        effective_prompt=""
        if(isQuestion):
            effective_prompt = f"""Voici la question:
            {transcript}
            """
        else:
            effective_prompt = f"""Voici le transcript horodaté:
            {transcript}
            """

        if self.provider == "transformers":
            result = self.run_transformers(effective_prompt, isQuestion)
        else:
            result = self.run_ollama(effective_prompt, isQuestion)

        # Si la réponse est vide ou trop courte, utiliser une réponse par défaut
        if not result or len(result.strip()) < 5:
            if isQuestion:
                result = "Bonjour ! Je suis Milo. Comment puis-je t'aider aujourd'hui ?"
            else:
                result = "Aucun contenu significatif detecte."
            print(f"[WARN] Reponse vide ou trop courte, utilisation d'une reponse par defaut")

        target_dir = Path(output_dir) if output_dir else self.output_dir
        target_dir.mkdir(exist_ok=True, parents=True)

        suffix = "_questions.txt" if isQuestion else "_resume.txt"

        output_path = target_dir / (transcript_path.stem + suffix)
        with open(output_path, "w", encoding="utf-8") as out:
            out.write(result)
        print(f"Saved to : {output_path}")
        return (transcript_path.stem + suffix)

    def generate_all(self):
        for transcript_file in sorted(self.transcripts_dir.glob("*.txt")):
            self.generate_from_file(transcript_file)

    def clearSubSynthetizerDir(self):
        if not self.output_dir.exists():
            print(f"Folder {self.output_dir} don't exist.")
            return

        file_count = 0
        for file in self.output_dir.iterdir():
            if file.is_file():
                try:
                    file.unlink()
                    file_count += 1
                except Exception as e:
                    print(f"Error: {file.name} : {e}")

        print(f"{file_count} file deleted from {self.output_dir}")


_project_root = Path(__file__).resolve().parent.parent.parent
# Use model from C:/Models to avoid Windows path issues with spaces
_qwen_model = "C:/Models/Qwen3-0.6B"

# To switch back to Ollama, set provider="ollama" and model to your ollama model name
mySynthetizer = SubSynthesizer(model=_qwen_model, provider="transformers")