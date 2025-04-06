import streamlit as st

# Funkcja do obliczania prawdopodobieństwa na podstawie kursów
def calculate_probability_from_odds(odds):
    return 1 / odds

# Funkcja do obliczania, która drużyna ma większe szanse na wygraną
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
    st.title("Obliczanie szans na wygraną drużyn")
    
    st.sidebar.header("Wprowadź dane o kursach")
    odds_team_1 = st.sidebar.number_input("Kurs na drużynę 1", min_value=1.0, value=2.5)
    odds_team_2 = st.sidebar.number_input("Kurs na drużynę 2", min_value=1.0, value=3.0)
    
    st.write("### Kursy wprowadzone:")
    st.write(f"Kurs na drużynę 1: {odds_team_1}")
    st.write(f"Kurs na drużynę 2: {odds_team_2}")
    
    # Obliczanie, która drużyna ma większe szanse na wygraną
    result = determine_winner(odds_team_1, odds_team_2)
    st.write("### Wynik:")
    st.write(result)

if __name__ == "__main__":
    main()