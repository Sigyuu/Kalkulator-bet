import streamlit as st
import matplotlib.pyplot as plt

# Funkcja do obliczania prawdopodobieństwa na podstawie kursów
def calculate_probability_from_odds(odds):
    return 1 / odds

# Funkcja do wykrywania value betów
def detect_value_bet(probability, odds):
    fair_odds = 1 / probability
    if odds > fair_odds:
        return True  # Value bet found
    else:
        return False  # No value bet

# Funkcja do generowania rekomendacji zakładów
def recommend_bet(odds, probability):
    fair_odds = 1 / probability
    if odds > fair_odds:
        return "Value Bet: Obstawiaj"
    else:
        return "Brak value betu: Zrezygnuj z tego zakładu"

# Funkcja do analizy na żywo meczu (na podstawie wyniku i minuty)
def live_match_analysis(score, time):
    if time > 80:  # Po 80. minucie meczu
        if score[0] > score[1]:  # Drużyna 1 prowadzi
            return "Drużyna 1 ma większe szanse na wygraną"
        else:
            return "Drużyna 2 ma większe szanse na wygraną"
    else:
        return "Mecz w toku, szanse równomierne"

# Funkcja do wyświetlania wyników na stronie Streamlit
def display_bet_recommendations(odds_team_1, odds_team_2, probability_team_1, probability_team_2):
    st.title("Rekomendacje zakładów")
    
    # Obliczanie prawdopodobieństw
    probability_1 = calculate_probability_from_odds(odds_team_1)
    probability_2 = calculate_probability_from_odds(odds_team_2)
    
    # Wykrywanie value betów
    value_bet_1 = detect_value_bet(probability_team_1, odds_team_1)
    value_bet_2 = detect_value_bet(probability_team_2, odds_team_2)
    
    st.write(f"Prawdopodobieństwo wygranej drużyny 1: {probability_1:.2f}")
    st.write(f"Prawdopodobieństwo wygranej drużyny 2: {probability_2:.2f}")
    
    if value_bet_1:
        st.write("Value Bet! Obstawiaj drużynę 1.")
    if value_bet_2:
        st.write("Value Bet! Obstawiaj drużynę 2.")
    
    # Propozycje zakładów
    st.write(recommend_bet(odds_team_1, probability_team_1))
    st.write(recommend_bet(odds_team_2, probability_team_2))

# Funkcja do rysowania wykresu zmieniających się kursów
def plot_odds(odds_data):
    times = odds_data['times']
    odds = odds_data['odds']
    plt.plot(times, odds)
    plt.title('Zmiana kursów w czasie')
    plt.xlabel('Czas')
    plt.ylabel('Kursy')
    st.pyplot(plt)

# Interfejs użytkownika w Streamlit
def main():
    # Wprowadź kursy drużyn i ich prawdopodobieństwa
    st.sidebar.header("Wprowadź dane o kursach")
    odds_team_1 = st.sidebar.number_input("Kurs na drużynę 1", min_value=1.0, value=2.5)
    odds_team_2 = st.sidebar.number_input("Kurs na drużynę 2", min_value=1.0, value=3.0)
    
    probability_team_1 = st.sidebar.number_input("Prawdopodobieństwo wygranej drużyny 1", min_value=0.0, max_value=1.0, value=0.4)
    probability_team_2 = st.sidebar.number_input("Prawdopodobieństwo wygranej drużyny 2", min_value=0.0, max_value=1.0, value=0.5)
    
    # Wyświetlenie rekomendacji
    display_bet_recommendations(odds_team_1, odds_team_2, probability_team_1, probability_team_2)
    
    # Wprowadź dane dla wykresu kursów
    st.sidebar.header("Wprowadź dane do wykresu")
    times = st.sidebar.text_area("Czas", "0,10,20,30,40,50")  # Przykładowe dane
    odds = st.sidebar.text_area("Kursy", "2.5,2.6,2.7,2.8,2.9,3.0")  # Przykładowe dane
    
    times = [int(t) for t in times.split(',')]
    odds = [float(o) for o in odds.split(',')]
    
    plot_odds({'times': times, 'odds': odds})

if __name__ == "__main__":
    main()