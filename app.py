import streamlit as st
import pickle
import requests

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="centered"
)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:9]

    recommended_movies = []
    recommended_movie_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        ## fetching the movie poster from the API
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movie_posters



def fetch_poster(movie_id):
    response = response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=fd38b4a1337671b770f719097818e929&language=en-US'.format(movie_id))
    data = response.json()

    
    if data.get('poster_path'):
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://placehold.co/500x750?text=No+Poster+Available"


movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = movies_list

similarity = pickle.load(open('similarity.pkl', 'rb'))



## HEADER 

st.markdown(
    """
    <h1 style='text-align: center; white-space: nowrap;'>
        🎬 Movie Recommendation System
    </h1>
    """,
    unsafe_allow_html=True
)

st.divider()


## Search Section

st.markdown(
    "<h3 style='text-align: center;'>Choose a Movie</h3>",
    unsafe_allow_html=True
)

left, middle, right = st.columns([1, 4, 1])

with middle:
    selected_movie_name = st.selectbox(
        "Select a movie",
        movies['title'].values,
        index=None,
        placeholder="🔍 Type or search for a movie...",
        label_visibility="collapsed"
    )

    recommend_clicked = st.button(
        "🎯 Get Recommendations",
        type="primary",
        use_container_width=True
    )

## Recommendation Section

if recommend_clicked:

    if selected_movie_name is None:
        st.warning("Please select a movie first.")

    else:

        with st.spinner("Finding the best matches for you..."):
            names, posters = recommend(selected_movie_name)

        st.divider()

        st.subheader("🍿 Recommended Movies")

        st.markdown(
            f"Because you liked **{selected_movie_name}**, "
            "here are the movies you might enjoy:"
        )

        st.write("")

        ## Row 1

        col1, col2, col3, col4 = st.columns(4, gap="medium")

        with col1:
            st.image(posters[0], caption=names[0], use_container_width=True)

        with col2:
            st.image(posters[1], caption=names[1], use_container_width=True)

        with col3:
            st.image(posters[2], caption=names[2], use_container_width=True)

        with col4:
            st.image(posters[3], caption=names[3], use_container_width=True)

        st.write("")

        
        ## Row 2

        col1, col2, col3, col4 = st.columns(4, gap="medium")

        with col1:
            st.image(posters[4], caption=names[4], use_container_width=True)

        with col2:
            st.image(posters[5], caption=names[5], use_container_width=True)

        with col3:
            st.image(posters[6], caption=names[6], use_container_width=True)

        with col4:
            st.image(posters[7], caption=names[7], use_container_width=True)
