import streamlit as st
import pandas as pd
import plotly.express as px

# Laad het CSV-bestand in plaats van de API-aanroep
df_global = pd.read_csv('global_top_50_playlist.csv')

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

# Wereldwijd pagina met de metrics en interactieve plots
if menu == 'Wereldwijd':
    st.header("Wereldwijd: Global Top 50")

    # Bereken de metrics
    most_popular_track = df_global.loc[df_global['Popularity'].idxmax(), 'Track']
    most_popular_artist = df_global['Artist'].value_counts().idxmax()  # Meest gestreamde artiest op basis van aantal tracks
    most_common_genre = df_global['Genre'].value_counts().idxmax()

    col1, col2, col3 = st.columns(3)

    # Metric voor populairste track met kleinere fontgrootte
    col1.markdown(f"<h3 style='font-size:20px;'>Populairste Track</h3><p style='font-size:16px;'>{most_popular_track}</p>", unsafe_allow_html=True)
    col2.markdown(f"<h3 style='font-size:20px;'>Meest Gestreamde Artiest</h3><p style='font-size:16px;'>{most_popular_artist}</p>", unsafe_allow_html=True)
    col3.markdown(f"<h3 style='font-size:20px;'>Meest Voorkomende Genre</h3><p style='font-size:16px;'>{most_common_genre}</p>", unsafe_allow_html=True)

    # Barplot 1
    genre_options = ['All'] + list(df_global['Genre'].unique())

    # Dropdown menu voor genres 
    selected_genre = st.selectbox("Kies een genre", genre_options)

    # Sliders voor filtering
    popularity_filter = st.slider('Filter op Populariteit', 50, 100, (50, 100))
    danceability_filter = st.slider('Filter op Danceability', 0.0, 1.0, (0.0, 1.0))
    acousticness_filter = st.slider('Filter op Acousticness', 0.0, 1.0, (0.0, 1.0))

    # Filter de dataset: als 'All' is geselecteerd, toon alles, anders filter op genre
    df_filtered = df_global[
        (df_global['Popularity'] >= popularity_filter[0]) & (df_global['Popularity'] <= popularity_filter[1]) &
        (df_global['Danceability'] >= danceability_filter[0]) & (df_global['Danceability'] <= danceability_filter[1]) &
        (df_global['Acousticness'] >= acousticness_filter[0]) & 
        ((df_global['Genre'] == selected_genre) if selected_genre != 'All' else True)
    ]

    # Sorteert de gefilterde dataset op populariteit en toont de top 5
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

    # Checkbox voor Track Length
    track_length_checkbox = st.checkbox("Track Length")
    
    # Als Track Length is geselecteerd, disable de andere checkboxes
    if track_length_checkbox:
        danceability_checkbox = False
        acousticness_checkbox = False
    else:
        # Checkboxes voor Danceability en Acousticness als Track Length niet is geselecteerd
        danceability_checkbox = st.checkbox("Danceability")
        acousticness_checkbox = st.checkbox("Acousticness")

    # Scatter plot 2. Maakt een lege lijst voor de geselecteerde features en kleuren
    selected_features = []
    selected_colors = []

    # Voegt de geselecteerde features toe aan de lijst
    if track_length_checkbox:
        selected_features.append('Duration (min)')
        selected_colors.append('blue')  # Blauwe kleur voor track length

    if danceability_checkbox:
        selected_features.append('Danceability')
        selected_colors.append('green')  # Groene kleur voor danceability

    if acousticness_checkbox:
        selected_features.append('Acousticness')
        selected_colors.append('red')  # Rode kleur voor acousticness

    # Controleert of er geen checkboxes zijn aangevinkt
    if not selected_features:
        st.write("Selecteer minstens één feature om de data te zien.")
    else:
        # Maakt een lege scatterplot
        fig = px.scatter()

        # Voegt elke geselecteerde feature toe aan de plot
        for i, feature in enumerate(selected_features):
            fig.add_scatter(x=df_global[feature], y=df_global['Popularity'], 
                            mode='markers', name=feature, 
                            marker=dict(color=selected_colors[i], size=6))  # Normale marker grootte

        # Update de layout van de plot
        fig.update_layout(
            xaxis_title=', '.join(selected_features),
            yaxis_title='Popularity',
            height=600,
            margin=dict(l=150)
        )

        st.plotly_chart(fig)

# Nederland pagina
if menu == 'Nederland': 
    st.header("Nederland: Top 50 Nederland")
    
    # Laad het CSV-bestand voor de Nederlandse Top 50 playlist
    df_netherlands = pd.read_csv('nederland_top_50_playlist.csv')

    # Rank toevoegen aan beide datasets
    df_netherlands['Rank'] = df_netherlands.index + 1
    df_global['Rank'] = df_global.index + 1

    # Selecteer de top 5 artiesten op basis van de volgorde in de dataset
    df_top5_netherlands = df_netherlands.head(5)

    # Voeg een checkbox toe om de Global top 5 toe te voegen
    add_global_checkbox = st.checkbox("Voeg Global Top 5 Tracks toe")

    # Voeg een kolom 'Region' toe om onderscheid te maken tussen Nederland en Global
    df_top5_netherlands['Region'] = 'Netherlands'

    # Begin met alleen de Nederlandse data
    df_combined = df_top5_netherlands

    # Als de checkbox is aangevinkt, voeg Global top 5 toe
    if add_global_checkbox:
        df_top5_global = df_global.head(5)
        df_top5_global['Region'] = 'Global'
        df_combined = pd.concat([df_combined, df_top5_global])

    # Plot voor de gecombineerde top 5 van Nederland en eventueel Global
    fig_combined = px.bar(df_combined, 
                          x='Track', y='Rank', 
                          color='Region', 
                          title='Top 5 Tracks: Netherlands vs Global', 
                          barmode='group',  # Balken naast elkaar
                          color_discrete_map={'Netherlands': '#FFA500', 'Global': '#636EFA'})  # Oranje voor Nederland, Blauw voor Global

    # Layout voor de plot
    fig_combined.update_layout(
        xaxis_title='Track',
        yaxis_title='Rank',
        yaxis_title_standoff=35,
        height=600,
        margin=dict(l=150)
    )

    # Toon de gecombineerde plot
    st.plotly_chart(fig_combined)

    # Voeg een checkbox toe om de Global top 5 genres toe te voegen
    add_global_checkbox_2 = st.checkbox("Voeg Global Top 5 Genres toe")

    # Bereken de top 5 meest voorkomende genres voor Nederland
    df_top5_netherlands_genres = df_netherlands['Genre'].value_counts().head(5).reset_index()
    df_top5_netherlands_genres.columns = ['Genre', 'Count']
    df_top5_netherlands_genres['Region'] = 'Netherlands'

    # Begin met alleen de Nederlandse data
    df_combined_genres = df_top5_netherlands_genres

    # Als de checkbox is aangevinkt, voeg de Global top 5 genres toe
    if add_global_checkbox_2:
        # Bereken de top 5 meest voorkomende genres voor Global
        df_top5_global_genres = df_global['Genre'].value_counts().head(5).reset_index()
        df_top5_global_genres.columns = ['Genre', 'Count']
        df_top5_global_genres['Region'] = 'Global'

        # Combineer de Nederlandse en Global genres in één dataset
        df_combined_genres = pd.concat([df_combined_genres, df_top5_global_genres])

    # Plot voor de gecombineerde top 5 genres van Nederland en eventueel Global
    fig_combined_genres = px.bar(df_combined_genres, 
                                 x='Genre', y='Count', 
                                 color='Region', 
                                 title='Top 5 Meest Voorkomende Genres: Netherlands vs Global', 
                                 barmode='group',  # Balken naast elkaar
                                 color_discrete_map={'Netherlands': '#FFA500', 'Global': '#636EFA'})  # Oranje voor Nederland, Blauw voor Global

    # Layout voor de plot
    fig_combined_genres.update_layout(
        xaxis_title='Genre',
        yaxis_title='Aantal',
        yaxis_title_standoff=35,
        height=600,
        margin=dict(l=150)
    )

    # Toon de gecombineerde plot
    st.plotly_chart(fig_combined_genres)



