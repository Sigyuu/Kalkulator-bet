import streamlit as st

st.title("SmartBet AI – Analiza Value Bet (Betclic)")

st.markdown("### Wprowadź kursy z Betclic:")

# Sekcja 1X2
st.subheader("1X2 – Zwycięzca meczu")
odds_1 = st.number_input("Kurs na drużynę 1", min_value=1.01)
odds_x = st.number_input("Kurs na remis", min_value=1.01)
odds_2 = st.number_input("Kurs na drużynę 2", min_value=1.01)

# Sekcja Over/Under
st.subheader("Over/Under – Liczba goli/punktów")
odds_over = st.number_input("Kurs na Over (np. +2.5)", min_value=1.01)
odds_under = st.number_input("Kurs na Under (np. -2.5)", min_value=1.01)

# Sekcja Handicap
st.subheader("Handicap (np. +1.5, -1.5)")
odds_handicap_home = st.number_input("Kurs na gospodarzy z handicapem", min_value=1.01)
odds_handicap_away = st.number_input("Kurs na gości z handicapem", min_value=1.01)

# Sekcja BTTS
st.subheader("BTTS – Obie drużyny strzelą")
odds_btts_yes = st.number_input("Kurs na TAK", min_value=1.01)
odds_btts_no = st.number_input("Kurs na NIE", min_value=1.01)

# Sekcja Double Chance
st.subheader("Double Chance")
odds_1x = st.number_input("Kurs 1X", min_value=1.01)
odds_12 = st.number_input("Kurs 12", min_value=1.01)
odds_x2 = st.number_input("Kurs X2", min_value=1.01)

# Sekcja Draw No Bet
st.subheader("Draw No Bet (Remis = zwrot)")
odds_dnb_1 = st.number_input("Kurs na drużynę 1", min_value=1.01)
odds_dnb_2 = st.number_input("Kurs na drużynę 2", min_value=1.01)

# --- Funkcja konwertująca kursy na prawdopodobieństwo i value bet ---
def convert_and_value(odds_dict):
    results = {}
    total_inverse = sum(1/o for o in odds_dict.values())
    for name, odds in odds_dict.items():
        implied_prob = (1 / odds) / total_inverse  # skalowane
        expected_value = (implied_prob * odds) - 1
        results[name] = round(expected_value * 100, 2)
    return results

# Przycisk obliczający
if st.button("Oblicz Value Bet dla wszystkich rynków"):
    st.subheader("Wyniki Value Bet:")

    # 1X2
    market_1x2 = {"Drużyna 1": odds_1, "Remis": odds_x, "Drużyna 2": odds_2}
    st.write("**1X2:**", convert_and_value(market_1x2))

    # Over/Under
    market_ou = {"Over": odds_over, "Under": odds_under}
    st.write("**Over/Under:**", convert_and_value(market_ou))

    # Handicap
    market_hc = {"Gospodarze": odds_handicap_home, "Goście": odds_handicap_away}
    st.write("**Handicap:**", convert_and_value(market_hc))

    # BTTS
    market_btts = {"Tak": odds_btts_yes, "Nie": odds_btts_no}
    st.write("**BTTS:**", convert_and_value(market_btts))

    # Double Chance
    market_dc = {"1X": odds_1x, "12": odds_12, "X2": odds_x2}
    st.write("**Double Chance:**", convert_and_value(market_dc))

    # Draw No Bet
    market_dnb = {"Drużyna 1": odds_dnb_1, "Drużyna 2": odds_dnb_2}
    st.write("**Draw No Bet:**", convert_and_value(market_dnb))