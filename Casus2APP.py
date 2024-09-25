import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import plotly.express as px

# Spotify API authenticatie
CLIENT_ID = '346bbc8224994730b926c4f852bf2869'  # Vul je eigen client_id in
CLIENT_SECRET = '163040f0613a45d3ab5fd773520ae7a4'  # Vul je eigen client_secret in

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# Functie om Global Top 50 playlist data en audiofeatures op te halen
def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks_data = []
    track_ids = []

    # Verzamel basisinformatie en track ID's
    for item in results['items']:
        track = item['track']
        artist_name = track['artists'][0]['name']
        track_name = track['name']
        popularity = track['popularity']
        duration_ms = track['duration_ms'] / 1000  # Zet duur om naar seconden
        release_date = track['album']['release_date']
        track_id = track['id']  # Haal track ID op
        track_ids.append(track_id)

        # Haal genres op per artiest (eerste artiest van de track)
        artist_info = sp.artist(track['artists'][0]['id'])
        genres = ', '.join(artist_info['genres']) if artist_info['genres'] else 'Geen genre beschikbaar'
        
        tracks_data.append({
            'Artist': artist_name, 
            'Track': track_name, 
            'Popularity': popularity,
            'Duration (s)': duration_ms, 
            'Release Date': release_date,
            'Genre': genres,
            'Track ID': track_id  # Voeg track ID toe voor audiofeatures
        })
    
    # Haal audiofeatures op voor alle tracks in één API-call
    audio_features = sp.audio_features(track_ids)
    
    # Voeg de audiofeatures toe aan de dataset
    for i, features in enumerate(audio_features):
        tracks_data[i]['Danceability'] = features['danceability']
        tracks_data[i]['Energy'] = features['energy']
        tracks_data[i]['Acousticness'] = features['acousticness']
        tracks_data[i]['Tempo'] = features['tempo']

    return pd.DataFrame(tracks_data)

# Haal de data van de Global Top 50 playlist op
playlist_id = '37i9dQZEVXbMDoHDwVN2tF'  # Global Top 50 playlist
df_global = get_playlist_tracks(playlist_id)

# Basis layout voor de app
st.set_page_config(page_title="Spotify API", layout="centered")

# Header en navigatieknoppen
st.title("API Case 2 - Groep 3")

# Sidebar met navigatieknoppen
menu = st.sidebar.radio("Navigatie", ['Intro', 'Wereldwijd', 'Nederland'])

# Intro pagina
if menu == 'Intro':
    st.header("Spotify API")

    # Spotify logo
    st.image("Spotify_logo_with_text.svg.webp", width=300) 
    
    # Korte uitleg
    st.write("""
        korte uitleg.
    """)
    
    # Bronnen
    st.write("### Gebruikte Bronnen:")
    st.write("""
        - [Spotify API](https://developer.spotify.com/documentation/web-api/)
        - [Spotipy Python Library](https://spotipy.readthedocs.io/en/2.19.0/)
        - [Spotify logo](https://en.m.wikipedia.org/wiki/File:Spotify_logo_with_text.svg)
        - [Youtube filmpje](https://www.youtube.com/watch?v=aFZOzmcmfcY&t=1241s)
        - [Streamlit documentatie](https://docs.streamlit.io/)
    """)

# Wereldwijd pagina met de Global Top 50 data en plots
if menu == 'Wereldwijd':
    st.header("Wereldwijd: Global Top 50")
    
    # Toon het dataframe met alle informatie, inclusief audiofeatures
    st.write("Hier is de Global Top 50 playlist met extra informatie zoals trackduur, releasedatum, en genres.")
    st.dataframe(df_global)

    # Dropdown menu voor x-as keuze (audiofeatures)
    feature = st.selectbox(
        'Kies een audiofeature voor de x-as:',
        ['Danceability', 'Energy', 'Acousticness', 'Tempo']
    )

    # Maak een interactieve plot met de gekozen audiofeature
    fig = px.bar(df_global.head(10), x=feature, y='Track', title=f'Top 10 Tracks by {feature}', orientation='h')
    st.plotly_chart(fig)

    # Genre verdeling plot
    genre_counts = df_global['Genre'].value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Count']
    
    fig_genre = px.bar(genre_counts, x='Count', y='Genre', title='Genre Distribution in Global Top 50', orientation='h')
    st.plotly_chart(fig_genre)

# Placeholder voor de Nederland pagina
if menu == 'Nederland':
    st.write("Nederland data komt hier later.")



