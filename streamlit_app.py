import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="SmartBet AI OCR Bot", layout="wide")
st.title("SmartBet AI OCR Bot v2.5")
st.markdown("**Załaduj screen z Betclic – bot rozpozna kursy, zakłady, wynik i zasugeruje najlepszy zakład.**")

uploaded_file = st.file_uploader("Wgraj screena (Betclic)", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Załadowany screen", use_column_width=True)

    with st.spinner("Analiza obrazu..."):
        reader = easyocr.Reader(['pl', 'en'], gpu=False)
        result = reader.readtext(np.array(image), detail=0)

    st.subheader("Wykryty tekst:")
    clean_lines = [line.strip() for line in result if len(line.strip()) > 0]
    for line in clean_lines:
        st.text(line)

    st.subheader("Szacowanie kursów i prawdopodobieństw:")
    odds = [float(w.replace(",", ".")) for w in clean_lines if w.replace(",", ".").replace(".", "").isdigit()]
    labels = ["1", "X", "2", "Over", "Under", "BTTS", "DoubleChance"]
    grouped = dict(zip(labels, odds[:len(labels)]))

    fair_probs = {k: 1/v for k, v in grouped.items()}
    margin = sum(fair_probs.values())
    normalized_probs = {k: round((p / margin) * 100, 2) for k, p in fair_probs.items()}

    for bet, prob in normalized_probs.items():
        st.write(f"**{bet}** — Szansa: {prob}% — Kurs: {grouped[bet]}")

    best_bet = max(normalized_probs, key=normalized_probs.get)
    value = round((normalized_probs[best_bet]/100) * grouped[best_bet], 2)

    st.subheader("Rekomendacja:")
    st.markdown(f"**Obstaw: {best_bet}** — Value: `{value}`")

    if value > 1.05:
        st.success("To wygląda na **value bet**!")
    else:
        st.info("Brak oczywistego value — graj ostrożnie.")

else:
    st.info("Wgraj screena, by rozpocząć analizę.")
