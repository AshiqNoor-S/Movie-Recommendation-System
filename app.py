import streamlit as st
import pickle
import pandas as pd
import requests

# Load movies data
movies_list = pickle.load(open("movies.pkl", "rb"))
movies = pd.DataFrame(movies_list)

# Load similarity data
similarity = pickle.load(open("similarity.pkl", "rb"))

# Function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=021bc4902479d5576cb2e30c5b8f3930&language=en-US'.format(movie_id))
    data = response.json()
    return "http://image.tmdb.org/t/p/w500" + data['poster_path']

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    similar_movies = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in similar_movies:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Streamlit UI
st.title("Movies Recommendation System")

st.sidebar.subheader("Instructions:")
st.sidebar.markdown("1. **Select a movie** from the dropdown or type the name of a movie.")
st.sidebar.markdown("2. Click the **'Get Recommendations'** button to see top 5 recommendations.")

# Sidebar for user input
selected_movie_name = st.sidebar.selectbox("Select a movie", movies['title'].values)


# Display selected movie with reduced size
st.subheader("Selected Movie:")
selected_movie_id = movies.loc[movies['title'] == selected_movie_name, 'movie_id'].values[0]
selected_movie_poster = fetch_poster(selected_movie_id)
st.image(selected_movie_poster, caption=selected_movie_name, width=200)

# Recommendation section
if st.button('Get Recommendations'):
    st.subheader("Top 5 Recommendations:")

    # Get recommendations
    names, posters = recommend(selected_movie_name)

    # Display recommendations in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    for name, poster, col in zip(names, posters, [col1, col2, col3, col4, col5]):
        with col:
            st.text(name)
            st.image(poster, use_column_width=True, caption=name)
