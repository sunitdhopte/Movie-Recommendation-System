import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

movies = pd.read_csv('./dataset/tmdb_5000_movies.csv')
credits = pd.read_csv('./dataset/tmdb_5000_credits.csv')

movies.head(2)