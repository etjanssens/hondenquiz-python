import streamlit as st
import random
from pathlib import Path
from datetime import datetime, timedelta
from PIL import Image

st.set_page_config(page_title="Hondenrassenquiz 🐶", layout="centered")

# --- Veilige rerun na score-update ---
if st.session_state.get("door_naar_feedback"):
    st.session_state.door_naar_feedback = False
    if st.session_state.get("gekozen_juist"):
        st.session_state.score += 1
    st.experimental_rerun()

# --- Veilige doorgang naar volgende vraag ---
if st.session_state.get("door_naar_volgende"):
    st.session_state.door_naar_volgende = False
    st.session_state.vraag += 1
    st.experimental_rerun()

# --- Hondenrassen ---
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

# --- Quiz genereren ---
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

# --- Initialiseer sessie ---
if "quiz" not in st.session_state:
    st.session_state.quiz = maak_quiz()
    st.session_state.vraag = 0
    st.session_state.score = 0
    st.session_state.gekozen = {}
    st.session_state.tijden = {}
    st.session_state.door_naar_volgende = False
    st.session_state.door_naar_feedback = False
    st.session_state.gekozen_juist = False

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
        st.experimental_rerun()
    st.stop()

# --- Huidige vraag ---
vraag_index = st.session_state.vraag
vraag = st.session_state.quiz[vraag_index]
img_path = Path(__file__).parent / "images" / vraag["foto"]

st.title("🐶 Raad het hondenras")
st.write(f"Vraag {vraag_index + 1} van 10")
st.image(str(img_path), use_container_width=True)

antwoord = st.radio("Wat is het ras?", vraag["opties"], key=f"radio_{vraag_index}")

# --- Vraag nog niet beantwoord ---
if vraag_index not in st.session_state.gekozen:
    if st.button("Controleer"):
        st.session_state.gekozen[vraag_index] = antwoord
        st.session_state.tijden[vraag_index] = datetime.now().isoformat()
        st.session_state.gekozen_juist = (antwoord == vraag["juist"])
        st.session_state.door_naar_feedback = True
        st.stop()
    st.stop()

# --- Feedback tonen ---
gekozen = st.session_state.gekozen[vraag_index]
juist = vraag["juist"]

if gekozen == juist:
    st.success("✅ Goed!")
else:
    st.error(f"❌ Fout! Het juiste antwoord was: **{juist}**")

# --- Automatisch doorgaan na 1.5 seconde ---
tijdstip_str = st.session_state.tijden.get(vraag_index)
if tijdstip_str:
    tijdstip = datetime.fromisoformat(tijdstip_str)
    if datetime.now() - tijdstip > timedelta(seconds=1.5):
        st.session_state.door_naar_volgende = True
        st.stop()
    else:
        st.stop()
else:
    st.stop()
