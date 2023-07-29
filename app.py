import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwMmUwYjhiMmI5MzVjMzQzODg5NGEyYTQ4MzM2NGRjZSIsInN1YiI6IjY0YmZhNTkxNmQ0Yzk3MDBmZjQ5NTkwMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zPojDrc_PDgX8C8OzRtFhPNLw4AWLNk9TWWO-xOyZC4"
    }
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}", headers=headers)
    data = response.json()

    return "http://image.tmdb.org/t/p/w185" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters



st.title('Movie Recommender System')
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox('select your movie', (movies['title'].values))
if st.button('Recommend'):
    names,poster = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(poster[0])
        st.text(names[0])
    with col2:
        st.image(poster[1])
        st.text(names[1])
    with col3:
        st.image(poster[2])
        st.text(names[2])
    with col4:
        st.image(poster[3])
        st.text(names[3])
    with col5:
        st.image(poster[4])
        st.text(names[4])


