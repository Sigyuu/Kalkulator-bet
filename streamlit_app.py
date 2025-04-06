import streamlit as st

# Funkcja obliczająca value bet (przykład)
def calculate_value_bet(odds_1, odds_2, odds_draw, prob_1, prob_2, prob_draw):
    expected_value_1 = (prob_1 * odds_1) - 1
    expected_value_2 = (prob_2 * odds_2) - 1
    expected_value_draw = (prob_draw * odds_draw) - 1

    value_bet = {'Team 1': expected_value_1, 'Team 2': expected_value_2, 'Draw': expected_value_draw}
    return value_bet

# Interfejs użytkownika w Streamlit
st.title("SmartBet AI - Kalkulator Value Bet")

st.header("Podaj dane:")
odds_1 = st.number_input("Kurs dla drużyny 1", min_value=1.0)
odds_2 = st.number_input("Kurs dla drużyny 2", min_value=1.0)
odds_draw = st.number_input("Kurs na remis", min_value=1.0)

prob_1 = st.slider("Prawdopodobieństwo wygranej drużyny 1 (%)", 0, 100, 50)
prob_2 = st.slider("Prawdopodobieństwo wygranej drużyny 2 (%)", 0, 100, 50)
prob_draw = st.slider("Prawdopodobieństwo remisu (%)", 0, 100, 0)

# Przeliczenie i wynik
if st.button("Oblicz Value Bet"):
    prob_1 /= 100
    prob_2 /= 100
    prob_draw /= 100
    
    value_bet = calculate_value_bet(odds_1, odds_2, odds_draw, prob_1, prob_2, prob_draw)
    
    st.subheader("Wyniki Value Bet")
    st.write(f"Drużyna 1: {value_bet['Team 1']:.2f}")
    st.write(f"Drużyna 2: {value_bet['Team 2']:.2f}")
    st.write(f"Remis: {value_bet['Draw']:.2f}")

    best_bet = max(value_bet, key=value_bet.get)
    st.write(f"Najlepszy zakład: {best_bet}")