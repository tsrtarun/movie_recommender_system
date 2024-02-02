import streamlit as st
import pickle
import pandas as pd
import requests

st.header('Movie Recommender')

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?'
                            'api_key=7b49ecf6a67514cd9d1571c68fede14c&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500"+ data['poster_path']

def fetch_overview(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?'
                            'api_key=7b49ecf6a67514cd9d1571c68fede14c&language=en-US'.format(movie_id))
    data = response.json()
    return data['overview']

def recommend_movies(movie):
    # index in new dataframe of selected movie
    movie_index = movies.index[movies['title'] == movie].tolist()[0]
    distances = similarity[movie_index]
    # create a numbered list of distances of selected movies and sort,
    # which returns next top 5 values(excluding first as it is the same movie)
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_5 = []
    recommended_movie_posters = []
    recommended_movie_overview = []

    for i in movies_list:
        recommend_5.append((movies.iloc[i[0]].title))
        # fetch the movie poster and overview
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_overview.append((fetch_overview(movie_id)))

    return recommend_5,recommended_movie_posters,recommended_movie_overview



similarity = pickle.load(open('similarity.pkl' ,'rb'))
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown and we will recommend you 5 similar movies",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions = recommend_movies(selected_movie)
    for i in range(len(recommended_movie_names)):
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.text(recommended_movie_names[i])
                st.caption(recommended_movie_descriptions[i])
            with col2:
                st.image(recommended_movie_posters[i])
