import streamlit as st
import pytesseract
from PIL import Image
import cv2
import numpy as np

# Funkcja do przetwarzania obrazu i wyciągania kursów
def extract_odds_from_image(image):
    # Wczytanie obrazu
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Przetwarzanie obrazu (opcjonalne - np. konwersja na skale szarości)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # Rozpoznawanie tekstu
    text = pytesseract.image_to_string(thresh)
    
    # Szukamy kursów (przykładowe wzory kursów w formacie 2.5, 3.0, etc.)
    lines = text.splitlines()
    odds = []
    for line in lines:
        if "Kurs" in line:  # Zakładając, że kursy są opisane słowem "Kurs"
            parts = line.split()  # Dzielimy linie na części
            for part in parts:
                try:
                    odds.append(float(part))  # Próbujemy przekonwertować na float
                except ValueError:
                    continue
    return odds

# Funkcja do obliczania prawdopodobieństw na podstawie kursów
def calculate_probability_from_odds(odds):
    return 1 / odds

# Funkcja do określania, która drużyna ma większe szanse na wygraną
def determine_winner(odds_team_1, odds_team_2):
    probability_team_1 = calculate_probability_from_odds(odds_team_1)
    probability_team_2 = calculate_probability_from_odds(odds_team_2)
    
    if probability_team_1 > probability_team_2:
        return "Drużyna 1 ma większe szanse na wygraną."
    elif probability_team_1 < probability_team_2:
        return "Drużyna 2 ma większe szanse na wygraną."
    else:
        return "Obie drużyny mają równe szanse na wygraną."

# Interfejs użytkownika w Streamlit
def main():
    st.title("Analiza zakładów Betclic na podstawie screenshotu")
    
    # Załaduj screenshot
    uploaded_image = st.file_uploader("Załaduj screenshot z Betclic", type=["png", "jpg", "jpeg"])
    
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        
        # Wyciągamy kursy z obrazu
        odds = extract_odds_from_image(image)
        
        if len(odds) >= 2:
            st.write(f"Kursy wyciągnięte z obrazu: {odds[0]} dla drużyny 1, {odds[1]} dla drużyny 2")
            # Obliczanie, która drużyna ma większe szanse na wygraną
            result = determine_winner(odds[0], odds[1])
            st.write("### Wynik:")
            st.write(result)
        else:
            st.write("Nie udało się wyciągnąć kursów z obrazu. Spróbuj załadować inny screenshot.")
    
if __name__ == "__main__":
    main()