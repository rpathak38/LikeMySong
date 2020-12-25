import pandas as pd
import sklearn.cluster as cluster
from sklearn.preprocessing import scale
import sklearn.decomposition as decomp
import matplotlib.pyplot as plt
import csv

# Data Cleaning and Organization
data = pd.read_csv("data_by_genres.csv")
data = data.sort_values(by='key')


print(data[['genres','key']].to_csv(path_or_buf='byKey.csv', index=False))
