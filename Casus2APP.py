import streamlit as st

# Basis layout voor de app
st.set_page_config(page_title="Spotify API", layout="centered")

# Header en navigatieknoppen
st.title("API Case 2 - Groep 3")

# Sidebar met navigatieknoppen
menu = st.sidebar.radio("Navigatie", ['Intro', 'Wereldwijd', 'Nederland'])

# Intro pagina
if menu == 'Intro':
    st.header("Spotify API")

    # Eventueel een logo toevoegen (logo moet lokaal opgeslagen zijn, bijvoorbeeld "spotify_logo.png")
    st.image("Spotify_logo_with_text.svg.webp", width=300) 
    
    # Korte uitleg
    st.write("""
        Dit project heeft als doel om Spotify-data te analyseren. Je kunt hier de meest populaire artiesten en genres
        wereldwijd en in Nederland vergelijken. De gegevens zijn verzameld via de Spotify API en visualisaties helpen 
        om de trends en verschillen tussen regio's te begrijpen.
    """)
    
    # Bronnen
    st.write("### Gebruikte Bronnen:")
    st.write("""
        - [Spotify API](https://developer.spotify.com/documentation/web-api/)
        - [Spotipy Python Library](https://spotipy.readthedocs.io/en/2.19.0/)
        - [Spotify Logo](https://en.m.wikipedia.org/wiki/File:Spotify_logo_with_text.svg)
    """) 

# Placeholder voor de andere knoppen (Wereldwijd en Nederland)
if menu == 'Wereldwijd':
    st.write("Wereldwijd data komt hier later.")

if menu == 'Nederland':
    st.write("Nederland data komt hier later.")


