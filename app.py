import streamlit as st
import random
from PIL import Image
from pathlib import Path

st.set_page_config(page_title="Hondenrassenquiz 🐶", layout="centered")

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

# --- Logica ---
fotos = list(RASSEN.items())
random.shuffle(fotos)
quiz = fotos[:10]

if "antwoorden" not in st.session_state:
    st.session_state.antwoorden = [""] * 10
if "score" not in st.session_state:
    st.session_state.score = None

st.title("🐶 Raad het hondenras")
st.write("Bekijk de afbeelding en typ het juiste ras in. Er zijn 10 vragen.")

for i, (bestand, rasnaam) in enumerate(quiz):
    st.markdown(f"### Vraag {i+1}/10")
    img_path = Path("images") / bestand
    st.image(str(img_path), use_column_width=True)
    antwoord = st.text_input(f"Wat is het ras? ({i+1})", key=f"antwoord_{i}")
    st.session_state.antwoorden[i] = antwoord

if st.button("Controleer antwoorden"):
    score = 0
    for i, (_, juist) in enumerate(quiz):
        if st.session_state.antwoorden[i].strip().lower() == juist.lower():
            score += 1
    st.session_state.score = score
    st.success(f"🎉 Je haalde {score}/10 goed!")
    st.code(f"Ik haalde {score}/10 in de hondenrassenquiz! 🐶")

if st.session_state.score is not None:
    if st.button("Opnieuw spelen"):
        st.session_state.antwoorden = [""] * 10
        st.session_state.score = None
        st.experimental_rerun()
