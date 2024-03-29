# -*- coding: utf-8 -*-
"""Recommender System.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-dQYCBD6dXyz8-idn4i_jOf6SdEL8PK2
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

movies = pd.read_csv('/content/tmdb_5000_movies.csv')
credits = pd.read_csv('/content/tmdb_5000_credits.csv')

movies.head(2)

credits.head(2)

movies.shape

credits.shape

movies = movies.merge(credits, on='title')
movies.head(2)

movies.shape

# movies.iloc[0]

# movies['original_language'].value_counts()
movies.columns

movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.isnull().sum()

movies.dropna(inplace=True)

movies.shape

movies.duplicated().sum()

movies.head(2)

movies.iloc[0]['genres']

import ast

def convert(text):
  l = []
  for i in ast.literal_eval(text):
    l.append(i['name'])

  return l

movies['genres'] = movies['genres'].apply(convert)

movies['keywords'] = movies['keywords'].apply(convert)

def convert_cast(text):
  l = []
  counter = 0
  for i in ast.literal_eval(text):
    if counter < 3:
      l.append(i['name'])
    counter += 1
  return l

movies['cast'] = movies['cast'].apply(convert_cast)

# movies['genres'] = movies['genres'].apply(convert_cast)

def fetch_director(text):
  l = []
  for i in ast.literal_eval(text):
    if i['job'] == 'Director':
      l.append(i['name'])
      break

  return l

movies['crew'] = movies['crew'].apply(fetch_director)

movies.head(2)

movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies.head(2)

def remove_space(word):
  l = []
  for i in word:
    l.append(i.replace(' ',''))
  return l

movies['cast'] = movies['cast'].apply(remove_space)
movies['crew'] = movies['crew'].apply(remove_space)
movies['genres'] = movies['genres'].apply(remove_space)
movies['keywords'] = movies['keywords'].apply(remove_space)

movies.head(2)

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

movies.iloc[0]['tags']

new_df = movies[['movie_id','title','tags']]
new_df.head()

new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))
new_df.head()

new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())
new_df.head()

import nltk
from nltk.stem import PorterStemmer

ps = PorterStemmer()

def stems(text):
  l = []
  for i in text.split():
    l.append(ps.stem(i))
  return " ".join(l)

new_df['tags'] = new_df['tags'].apply(stems)

new_df.iloc[0]['tags']

from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(max_features=5000, stop_words='english')

vector = cv.fit_transform(new_df['tags']).toarray()

vector
vector.shape

from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vector)

similarity

new_df[new_df['title'] == 'Spider-Man'].index[0]

def recommend(movie):
  index = new_df[new_df['title'] == movie].index[0]
  distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
  for i in distances[1:6]:
    print(new_df.iloc[i[0]].title)

recommend('Avatar')

import pickle

pickle.dump(new_df, open('artifacts/movie_list.pkl','wb'))
pickle.dump(similarity, open('artifacts/similarity.pkl','wb'))