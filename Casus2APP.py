import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import plotly.express as px

# Spotify API authenticatie
CLIENT_ID = '346bbc8224994730b926c4f852bf2869'  # Vul je eigen client_id in
CLIENT_SECRET = '355d1998b5bf4f098c06d7b5f8f4ae78'  # Vul je eigen client_secret in

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
        duration_min = track['duration_ms'] / 1000 / 60  # Zet duur om naar minuten
        release_date = track['album']['release_date']
        track_id = track['id']  # Haal track ID op
        track_ids.append(track_id)

        # Haal genres op per artiest (eerste artiest van de track)
        artist_info = sp.artist(track['artists'][0]['id'])
        genres = artist_info['genres'][0] if artist_info['genres'] else 'Geen genre beschikbaar'
        
        tracks_data.append({
            'Artist': artist_name, 
            'Track': track_name, 
            'Popularity': popularity,
            'Duration (min)': round(duration_min, 2),  # Duur in minuten, afgerond
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
    
    # Tabel tonen met geselecteerde kolommen
    st.write("Hier is de Global Top 50 playlist met extra informatie zoals trackduur, releasedatum, en genres.")
    st.dataframe(df_global[['Artist', 'Track', 'Popularity', 'Duration (min)', 'Release Date', 'Genre']])

    # Dropdown menu voor x-as keuze (audiofeatures en Popularity)
    feature = st.selectbox(
        'Kies een feature voor de x-as:',
        ['Popularity', 'Danceability', 'Energy', 'Acousticness', 'Tempo']
    )

    # Sorteer de dataframe op basis van de gekozen feature
    df_sorted = df_global.sort_values(by=feature, ascending=False)

    # Slider met labels voor Audiofeatures en Genre Distributie
    slider_option = st.select_slider(
        'Selecteer plot type',
        options=['Top 10 Audiofeatures', 'Genre Distributie'],
        value='Top 10 Audiofeatures'
    )
    
    if slider_option == 'Top 10 Audiofeatures':
        # Interactieve plot met de gekozen feature, gesorteerd
        fig = px.bar(df_sorted.head(10), x=feature, y='Track', color=feature, 
                     title=f'Top 10 Tracks by {feature}', orientation='h', color_continuous_scale='Blues')
        fig.update_layout(
            xaxis_title=feature,
            yaxis_title='Track',
            yaxis_title_standoff=1,
            yaxis={'categoryorder':'total ascending'},
            height=600,
            margin=dict(l=150)
        )
        fig.update_traces(marker_line_color='black', marker_line_width=0.75)
        st.plotly_chart(fig)
    
    elif slider_option == 'Genre Distributie':
        # Genre verdeling plot (alleen hoofdcategorieën)
        genre_counts = df_global['Genre'].value_counts().reset_index()
        genre_counts.columns = ['Genre', 'Count']
        
        fig_genre = px.bar(genre_counts, x='Count', y='Genre', title='Genre Distribution in Global Top 50', orientation='h')
        st.plotly_chart(fig_genre)

# Placeholder voor de Nederland pagina
if menu == 'Nederland':
    st.write("Nederland data komt hier later.")


