import streamlit as st
import random
import time
from pathlib import Path
from PIL import Image

# --- Configuratie ---
RASSEN = {
    "akita.jpg": "Akita Inu",
    "appenzeller.jpeg": "Appenzeller",
    "beagle.jpeg": "Beagle",
    "bernersennen.jpg": "Berner Sennen",
    "bichonfrise.jpg": "Bichon Frisé",
    "bordercollie.jpg": "Border Collie",
    "bostonterrier.jpeg": "Boston Terriër",
    "chihuahua.jpg": "Chihuahua",
    "cockerspaniel.jpg": "Cocker Spaniël",
    "dalmatier.jpg": "Dalmatiër",
    "dobermann.jpg": "Dobermann",
    "duitsedog.jpg": "Duitse Dog",
    "duitseherder.jpeg": "Duitse Herder",
    "engelsebulldog.jpg": "Engelse Bulldog",
    "fransebulldog.jpeg": "Franse Bulldog",
    "goldenretriever.jpg": "Golden Retriever",
    "husky.jpg": "Husky",
    "jackrussel.jpg": "Jack Russel",
    "labrador.jpg": "Labrador",
    "maltezer.jpg": "Maltezer",
    "poedel.jpg": "Poedel",
    "rottweiler.jpg": "Rottweiler",
    "shetlandsheepdog.jpeg": "Shetland Sheepdog",
    "shitzu.jpeg": "Shih Tzu",
    "sintbernard.jpg": "Sint Bernard",
    "staffordshirebulterrier.jpg": "Staffordshire Bull Terriër",
    "teckel.jpg": "Teckel",
    "whippet.jpg": "Whippet"
}

def maak_quiz():
    items = list(RASSEN.items())
    random.shuffle(items)
    quiz = []
    for foto, juist in items[:10]:
        opties = random.sample([v for v in RASSEN.values() if v != juist], 3)
        opties.append(juist)
        random.shuffle(opties)
        quiz.append({"foto": foto, "juist": juist, "opties": opties})
    return quiz

# --- Session State ---
if "quiz" not in st.session_state:
    st.session_state.quiz = maak_quiz()
    st.session_state.vraag = 0
    st.session_state.score = 0
    st.session_state.resultaat = None

# --- UI ---
st.title("🐶 Raad het hondenras")
st.write(f"Vraag {st.session_state.vraag + 1} van 10")

from datetime import datetime, timedelta

# --- Toon de vraag ---
vraag = st.session_state.quiz[st.session_state.vraag]
img_path = Path(__file__).parent / "images" / vraag["foto"]
st.image(str(img_path), use_container_width=True)

antwoord = st.radio("Wat is het ras?", vraag["opties"], key=f"keuze_{st.session_state.vraag}")

# --- Knop controleren ---
if f"beantwoord_{st.session_state.vraag}" not in st.session_state:
    if st.button("Controleer"):
        st.session_state[f"beantwoord_{st.session_state.vraag}"] = antwoord
        st.session_state[f"beantwoord_tijd_{st.session_state.vraag}"] = datetime.now().isoformat()
        if antwoord == vraag["juist"]:
            st.session_state.score += 1
        st.experimental_rerun()

# --- Feedback tonen ---
elif f"beantwoord_{st.session_state.vraag}" in st.session_state:
    gegeven = st.session_state[f"beantwoord_{st.session_state.vraag}"]
    juist = vraag["juist"]
    if gegeven == juist:
        st.success("✅ Goed!")
    else:
        st.error(f"❌ Fout! Het juiste antwoord was: **{juist}**")

    # Check of er al 1.5 seconde voorbij is
    tijdstip = datetime.fromisoformat(st.session_state[f"beantwoord_tijd_{st.session_state.vraag}"])
    if datetime.now() - tijdstip > timedelta(seconds=1.5):
        st.session_state.vraag += 1
        st.experimental_rerun()

# --- Eindscherm ---
if st.session_state.vraag >= 10:
    st.header("🎉 Je bent klaar!")
    score = st.session_state.score
    st.write(f"Je haalde **{score}/10** goed!")

    if score == 10:
        st.success("🐾 Jij bent een ultieme hondenkenner!")
    elif score >= 7:
        st.info("🐕 Jij houdt duidelijk van honden!")
    elif score >= 4:
        st.warning("🐶 Je weet er wat van, maar er is ruimte voor groei.")
    else:
        st.error("🐾 Tijd om wat meer hondenrassen te leren kennen!")

    if st.button("Speel opnieuw"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()
