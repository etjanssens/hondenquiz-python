import streamlit as st
import random
import time
from pathlib import Path
from datetime import datetime, timedelta
from PIL import Image

st.set_page_config(page_title="Hondenrassenquiz 🐶", layout="centered")

st.markdown("""
    <style>
    /* Achtergrond met subtiel hondenpatroon */
    body {
        background-image: url('https://static.vecteezy.com/system/resources/previews/006/431/803/non_2x/seamless-dog-pattern-with-paw-prints-and-hearts-cat-foot-texture-pattern-with-doggy-pawprint-and-hearts-dog-texture-hand-drawn-illustration-in-doodle-style-on-white-background-vector.jpg');
        background-repeat: repeat;
        background-color: #ffeeff;
        color: #222;
    }

    /* Centrale container */
    .stApp {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 0 15px deeppink;
    }

    /* Titels */
    h1, h2, h3 {
        color: #ff66cc;
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 1px 1px #ff00ff;
        animation: gentleWobble 3s infinite ease-in-out;
    }

    @keyframes gentleWobble {
        0%, 100% { transform: rotate(-1deg); }
        50% { transform: rotate(1deg); }
    }

    /* Antwoordopties */
    .stRadio > div {
        background: linear-gradient(90deg, #fff0f5, #ccf2ff);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-size: 1.1rem;
        font-weight: bold;
        color: #333;
        box-shadow: 0 0 8px #ffaaff;
        transition: transform 0.2s ease-in-out;
    }

    .stRadio > div:hover {
        transform: scale(1.04);
    }

    /* Knoppen */
    button[kind="primary"] {
        background: radial-gradient(circle, #ffcc00, #ff8800);
        border-radius: 30px;
        font-size: 1.3rem;
        font-weight: bold;
        color: white;
        padding: 1rem 2rem;
        box-shadow: 0 0 12px #ff6600;
        animation: softBounce 1.2s infinite alternate;
    }

    @keyframes softBounce {
        from { transform: translateY(0); }
        to { transform: translateY(-4px); }
    }

    /* Feedback (correct/fout) */
    .stSuccess, .stError, .stWarning, .stInfo {
        font-size: 1.2rem;
        font-weight: bold;
        background: repeating-linear-gradient(
            -45deg,
            #ffffcc,
            #ffffcc 10px,
            #ffccff 10px,
            #ffccff 20px
        );
        color: #000 !important;
        padding: 1rem;
        border-radius: 12px;
    }

    /* Afbeelding: wiebelen */
    img {
        border: 4px solid deeppink;
        border-radius: 20px;
        box-shadow: 0 0 12px hotpink;
        margin-bottom: 1rem;
        animation: subtleWiggle 3s ease-in-out infinite;
    }

    @keyframes subtleWiggle {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(1deg); }
        75% { transform: rotate(-1deg); }
    }
    </style>
""", unsafe_allow_html=True)

# --- Quiz genereren ---
def maak_quiz():
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

    items = list(RASSEN.items())
    random.shuffle(items)
    quiz = []
    for foto, juist in items[:10]:
        opties = random.sample([v for v in RASSEN.values() if v != juist], 3)
        opties.append(juist)
        random.shuffle(opties)
        quiz.append({"foto": foto, "juist": juist, "opties": opties})
    return quiz

# --- Initialisatie bij eerste run ---
if "quiz" not in st.session_state:
    st.session_state.quiz = maak_quiz()
    st.session_state.vraag = 0
    st.session_state.score = 0
    st.session_state.gekozen = {}
    st.session_state.tijden = {}
    st.session_state.door_naar_volgende = False
    st.session_state.door_naar_feedback = False
    st.session_state.gekozen_juist = False

# --- Veilige rerun na score-update ---
if st.session_state.get("door_naar_feedback"):
    st.session_state.door_naar_feedback = False
    if st.session_state.get("gekozen_juist"):
        st.session_state.score += 1
    st.rerun()

# --- Veilige doorgang naar volgende vraag ---
if st.session_state.get("door_naar_volgende"):
    st.session_state.door_naar_volgende = False
    st.session_state.vraag += 1
    st.rerun()

# --- Einde quiz ---
if st.session_state.vraag >= len(st.session_state.quiz):
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
        st.session_state.clear()
        st.rerun()
    st.stop()

# --- Vraag tonen ---
vraag_index = st.session_state.vraag
vraag = st.session_state.quiz[vraag_index]
img_path = Path(__file__).resolve().parent / "images" / vraag["foto"]

st.title("🐶 Raad het hondenras")
st.write(f"Vraag {vraag_index + 1} van 10")

if not img_path.exists():
    st.error(f"Afbeelding niet gevonden: {img_path.name}")
    st.stop()

st.image(str(img_path), use_container_width=True)

antwoord = st.radio("Wat is het ras?", vraag["opties"], key=f"radio_{vraag_index}")

import time  # bovenaan toevoegen als je dat nog niet had

# --- Antwoordverwerking ---
tijdstip_str = st.session_state.tijden.get(vraag_index)
gekozen = st.session_state.gekozen.get(vraag_index)

if gekozen is None:
    if st.button("Controleer"):
        st.session_state.gekozen[vraag_index] = antwoord
        st.session_state.gekozen_juist = (antwoord == vraag["juist"])
        st.session_state.tijden[vraag_index] = datetime.now().isoformat()
        st.rerun()
    st.stop()
else:
    # --- Feedback tonen ---
    juist = vraag["juist"]
    if gekozen == juist:
        st.success("✅ Goed!")
    else:
        st.error(f"❌ Fout! Het juiste antwoord was: **{juist}**")

    # --- Voortgangsbalk van 1.5 seconde ---
    progress_bar = st.progress(0, text="Volgende vraag komt eraan...")

    for i in range(100):
        time.sleep(1.5 / 100)
        progress_bar.progress(i + 1, text="Volgende vraag komt eraan...")

    # --- Na 1.5s doorgaan ---
    st.session_state.vraag += 1
    if gekozen == juist:
        st.session_state.score += 1
    st.rerun()
