import streamlit as st
import easyocr
import numpy as np
from PIL import Image

# Inicjalizacja OCR
reader = easyocr.Reader(['en'])

def extract_odds_from_image(image):
    img_array = np.array(image)
    results = reader.readtext(img_array)

    odds = []
    for bbox, text, _ in results:
        text = text.replace(",", ".")
        try:
            val = float(text)
            if 1.01 <= val <= 10.0:  # zakładamy, że kursy są w tym zakresie
                odds.append(val)
        except:
            continue
    return odds

def calculate_probability(odds):
    return 1 / odds if odds != 0 else 0

def determine_winner(odds1, odds2):
    prob1 = calculate_probability(odds1)
    prob2 = calculate_probability(odds2)

    if prob1 > prob2:
        return f"Drużyna 1 ma większe szanse ({round(prob1*100, 1)}%)"
    elif prob2 > prob1:
        return f"Drużyna 2 ma większe szanse ({round(prob2*100, 1)}%)"
    else:
        return "Obie drużyny mają równe szanse"

# UI
st.title("Betclic SmartBet AI (OCR)")

uploaded_image = st.file_uploader("Prześlij screenshot z Betclic", type=["png", "jpg", "jpeg"])
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Wczytany obraz", use_column_width=True)

    with st.spinner("Analiza obrazu..."):
        odds = extract_odds_from_image(image)

    st.write(f"Znalezione kursy: {odds}")

    if len(odds) >= 2:
        result = determine_winner(odds[0], odds[1])
        st.success(result)
    else:
        st.warning("Nie udało się rozpoznać przynajmniej dwóch kursów. Upewnij się, że są wyraźne.")