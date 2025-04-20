#!/usr/bin/python3
import streamlit as st
import json
import random
from pathlib import Path

# --- Chargement des mots ---
with open("words.json", "r", encoding="utf-8") as f:
    words = json.load(f)

# --- Chargement ou initialisation du progrès ---
progress_file = Path("progress.json")

if progress_file.exists():
    with open(progress_file, "r", encoding="utf-8") as f:
        progress = json.load(f)
else:
    progress = {entry["fr"]: {"en": entry["en"], "score": 0} for entry in words}

# --- Mode sélection ---
mode = st.sidebar.radio("Choisis un mode", ["Évaluation initiale", "Révision quotidienne"])

# --- Nombre de mots ---
N = st.sidebar.slider("Nombre de mots aujourd'hui", 5, 50, 20)

# --- Sélection des mots à travailler ---
def mots_a_travailler():
    if mode == "Évaluation initiale":
        return [k for k, v in progress.items() if v["score"] == 0][:N]
    else:
        return sorted(progress.items(), key=lambda x: x[1]["score"])[:N]

# --- Interface ---
st.title("🌱 Apprentissage du vocabulaire anglais")
st.write(f"Mode : **{mode}**")

mots = mots_a_travailler()
réponses = {}

if mots:
    for i, mot in enumerate(mots, 1):
        fr = mot if isinstance(mot, str) else mot[0]
        st.subheader(f"{i}. {fr}")
        réponse = st.text_input(f"Traduction anglaise de « {fr} »", key=fr)
        réponses[fr] = réponse.lower().strip()
else:
    st.success("🎉 Tu as fini cette section !")

# --- Bouton valider ---
if st.button("Valider mes réponses"):
    bonne_reponses = 0
    for fr, user_answer in réponses.items():
        correct = progress[fr]["en"].lower()
        if user_answer == correct:
            st.success(f"✔️ {fr} = {correct}")
            progress[fr]["score"] += 1
            bonne_reponses += 1
        else:
            st.error(f"❌ {fr} → {user_answer} | Réponse attendue : {correct}")
            progress[fr]["score"] = max(progress[fr]["score"] - 1, 0)

    st.info(f"✅ {bonne_reponses}/{len(réponses)} bonnes réponses")

    # Sauvegarde
    with open(progress_file, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)
