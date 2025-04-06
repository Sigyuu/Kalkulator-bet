import easyocr
import re
import numpy as np

# Funkcja do obliczania prawdopodobieństwa z kursu
def calculate_probability(odd):
    return 1 / odd

# Funkcja do wykrywania typów zakładów z obrazu
def analyze_bet_type(image_path):
    reader = easyocr.Reader(['pl', 'en'])  # Wybieramy języki: polski, angielski
    result = reader.readtext(image_path)

    # Typy zakładów, które chcemy rozpoznać
    bet_types = {
        '1X2': r"(Wygra drużyna A|Remis|Wygra drużyna B)",
        'Handicap': r"(\+|\-)\d+",
        'Over/Under': r"(Powyżej|Ponżej)\s\d+(\.\d+)?"
    }

    detected_bet_types = []
    odds = []  # Przechowujemy kursy
    # Analiza wykrytych tekstów
    for (_, text, _) in result:
        for bet_type, pattern in bet_types.items():
            if re.search(pattern, text, re.IGNORECASE):
                detected_bet_types.append((bet_type, text))
        # Szukamy kursów
        odds_match = re.search(r"\d+\.\d+", text)
        if odds_match:
            odds.append(float(odds_match.group()))

    return detected_bet_types, odds

# Funkcja do sugerowania najlepszych zakładów na podstawie kursów
def suggest_best_bet(odds, bet_types):
    probabilities = [calculate_probability(odd) for odd in odds]
    
    best_bet_index = np.argmax(probabilities)  # Największe prawdopodobieństwo
    best_bet = bet_types[best_bet_index]
    best_odds = odds[best_bet_index]
    best_probability = probabilities[best_bet_index] * 100

    print("Suggested Bet:")
    print(f"Zakład: {best_bet} | Kurs: {best_odds} | Prawdopodobieństwo: {best_probability:.2f}%")
    return best_bet, best_odds, best_probability

# Przykład użycia
def main():
    image_path = 'screen_from_betclic.png'  # Ścieżka do obrazu z Betclic
    bet_types, odds = analyze_bet_type(image_path)
    
    if not bet_types:
        print("Nie wykryto żadnych typów zakładów.")
        return

    print("Wykryte typy zakładów:", bet_types)
    print("Wykryte kursy:", odds)

    if odds:
        suggest_best_bet(odds, [bet_type[1] for bet_type in bet_types])  # Sugerowanie najlepszego zakładu

if __name__ == "__main__":
    main()