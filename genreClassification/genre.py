import pandas as pd
import sklearn.cluster as cluster
from sklearn.preprocessing import scale
import sklearn.decomposition as decomp
import matplotlib.pyplot as plt
import csv

# Data Cleaning and Organization
data = pd.read_csv("data_by_genres.csv")
genres = data[['genres']]
data = data.drop('genres', 1)
data = data.drop("duration_ms", 1)
data = data.drop("popularity", 1)
data = data.drop("key", 1)
data = data.drop("mode", 1)

# Normalization (Scaling)
X = data.to_numpy()
X = scale(X)

# Dimensionality Reduction (PCA)
#pca = decomp.KernelPCA(n_components=2, kernel='rbf')
#X = pca.fit_transform(X)
#print(X.shape)

#2900 genres,
# Agglomerative Clustering
agglomerative = cluster.AgglomerativeClustering(n_clusters=297, linkage='ward')
print(agglomerative.fit_predict(X))

# plt.scatter(X[:,0], X[:,1], c = agglomerative.labels_, cmap= 'rainbow')
# plt.show()

with open("genres_classified_without_mode.csv", "w") as fout:
    csv_writer = csv.writer(fout)
    temp = list(zip(genres.values.flatten(), agglomerative.labels_))
    temp.sort(key = lambda x: x[1])
    for genre, label in temp:
        csv_writer.writerow([genre, label])