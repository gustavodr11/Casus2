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

# Wereldwijd pagina met de metrics en interactieve plot
if menu == 'Wereldwijd':
    st.header("Wereldwijd: Global Top 50")

    # Bereken de metrics
    most_popular_track = df_global.loc[df_global['Popularity'].idxmax(), 'Track']
    most_popular_artist = df_global['Artist'].value_counts().idxmax()  # Meest gestreamde artiest op basis van aantal tracks
    most_common_genre = df_global['Genre'].value_counts().idxmax()

    # Toon de metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Populairste Track", most_popular_track)
    col2.metric("Meest Gestreamde Artiest", most_popular_artist)
    col3.metric("Meest Voorkomende Genre", most_common_genre)

    # Dropdown menu voor genres
    selected_genre = st.selectbox("Kies een genre", df_global['Genre'].unique())

    # Sliders voor filtering
    popularity_filter = st.slider('Filter op Populariteit', 50, 100, (50, 100))
    danceability_filter = st.slider('Filter op Danceability', 0.0, 1.0, (0.0, 1.0))
    acousticness_filter = st.slider('Filter op Acousticness', 0.0, 1.0, (0.0, 1.0))

    # Filter de dataset op basis van de gekozen filters
    df_filtered = df_global[
        (df_global['Popularity'] >= popularity_filter[0]) & (df_global['Popularity'] <= popularity_filter[1]) &
        (df_global['Danceability'] >= danceability_filter[0]) & (df_global['Danceability'] <= danceability_filter[1]) &
        (df_global['Acousticness'] >= acousticness_filter[0]) & (df_global['Acousticness'] <= acousticness_filter[1]) &
        (df_global['Genre'] == selected_genre)
    ]

    # Sorteer de gefilterde dataset op populariteit en toon de top 5
    df_top5 = df_filtered.sort_values(by='Popularity', ascending=False).head(5)

    # Interactieve plot van de gefilterde top 5
    if not df_top5.empty:
        fig = px.bar(df_top5, x='Popularity', y='Track', color='Popularity', 
                     title=f'Top 5 Tracks in {selected_genre}', orientation='h', color_continuous_scale='Blues')
        fig.update_layout(
            xaxis_title='Popularity',
            yaxis_title='Track',
            yaxis_title_standoff=1,
            yaxis={'categoryorder':'total ascending'},
            height=600,
            margin=dict(l=150)
        )
        fig.update_traces(marker_line_color='black', marker_line_width=0.75)
        st.plotly_chart(fig)
    else:
        st.write("Geen nummers gevonden met de gekozen filters.")

# Placeholder voor de Nederland pagina
if menu == 'Nederland':
    st.write("Nederland data komt hier later.")


