import streamlit as st
import random
import time
from pathlib import Path
from datetime import datetime, timedelta
from PIL import Image

st.set_page_config(page_title="Hondenrassenquiz 🐶", layout="centered")

# --- Stijl injecteren ---
st.markdown("""
    <style>
    /* Achtergrond: glitter en hondenpootjes */
    body {
        background-image: url('https://media.giphy.com/media/3oriO0OEd9QIDdllqo/giphy.gif');
        background-size: cover;
        background-attachment: fixed;
        color: #fff;
    }

    /* Centrale container transparant + schaduw */
    .stApp {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 0 30px hotpink;
        animation: pulseBox 3s infinite alternate;
    }

    /* Pulse-effect voor container */
    @keyframes pulseBox {
        from { box-shadow: 0 0 20px #ff00ff; }
        to { box-shadow: 0 0 40px #00ffff; }
    }

    /* Header */
    h1, h2, h3 {
        color: #ffcc00;
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 2px 2px #ff00ff;
        animation: wobble 2s infinite ease-in-out;
    }

    @keyframes wobble {
        0%, 100% { transform: rotate(-2deg); }
        50% { transform: rotate(2deg); }
    }

    /* Antwoordopties */
    .stRadio > div {
        background: linear-gradient(90deg, #ff99cc, #66ffff);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-size: 1.2rem;
        font-weight: bold;
        color: #000;
        box-shadow: 0 0 10px #ff00ff;
        transition: transform 0.2s ease-in-out;
    }

    .stRadio > div:hover {
        transform: scale(1.05);
    }

    /* Knoppen */
    button[kind="primary"] {
        background: radial-gradient(circle, #ff9900, #ff0000);
        border-radius: 50px;
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        box-shadow: 0 0 20px #ff6600;
        padding: 1rem 2rem;
        animation: bounce 1s infinite alternate;
    }

    @keyframes bounce {
        from { transform: translateY(0); }
        to { transform: translateY(-5px); }
    }

    /* Score feedback */
    .stSuccess, .stError, .stWarning, .stInfo {
        font-size: 1.3rem;
        font-weight: bold;
        background: repeating-linear-gradient(
            -45deg,
            #ffff00,
            #ffff00 10px,
            #ff00ff 10px,
            #ff00ff 20px
        );
        color: black !important;
        padding: 1rem;
        border-radius: 12px;
    }

    /* Afbeelding styling */
    img {
        border: 6px dashed hotpink;
        border-radius: 30px;
        box-shadow: 0 0 20px yellow;
        margin-bottom: 1rem;
        animation: spinDog 4s linear infinite;
    }

    @keyframes spinDog {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
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
