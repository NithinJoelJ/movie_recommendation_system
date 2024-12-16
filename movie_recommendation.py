from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app=Flask(__name__)

movies = pd.read_csv('dataset.csv')
movies['tags'] = movies['genre']+movies['overview']
new_df = movies[['id','title','genre','overview','tags']]
new_df = new_df.drop(columns=['genre', 'overview'])
from sklearn.feature_extraction .text import CountVectorizer
cv = CountVectorizer(max_features=10000, stop_words='english')
vec = cv.fit_transform(new_df['tags'].values.astype('U')).toarray()
vec
vec.shape

sim = cosine_similarity(vec)
sim
new_df[new_df['title']=='The Godfather']
dist = sorted(list(enumerate(sim[0])),reverse=True,key=lambda vec:vec[1])
dist
for i in dist[0:5]:
    new_df.iloc[i[0]].title

def recommend(movies):
    try:
        index = new_df[new_df['title'] == movies].index[0]
        distance = sorted(list(enumerate(sim[index])), reverse=True, key=lambda vec: vec[1])
        recommended_movies = [new_df.iloc[i[0]].title for i in distance[1:6]]
        return recommended_movies
    except IndexError:
        return []

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data=request.get_json()
    movie_title = data.get('movie', '')
    recommendations=recommend(movie_title)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)