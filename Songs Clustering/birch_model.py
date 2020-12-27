
import pandas as pd
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import StandardScaler
import sklearn.decomposition as decomp
import csv
import pickle

def dataclean(filePath):
    '''
    Cleans the data to be feeded into the KMeans model.
    Assigns variables to be stored in the output csv. 
    '''
    data = pd.read_csv(filePath)
    names = data[['name']]
    artist = data[['artists']]
    ids = data[['id']]

    dropThis = ['year', 'artists', 'explicit', 'duration_ms', 'popularity', 'id', 'release_date', 'name', 'liveness', 'mode']
    for name in dropThis:
        data = data.drop(name, 1);
    return (data, names, artist, ids)

def normalize(data):
    '''
    Uses a Standard Scaler to perform feature scaling on the cleansed data.
    '''
    X = data.to_numpy()
    sc = StandardScaler()
    sc.fit(X)
    X = sc.transform(X)
    return X, sc
 
def pca(data, components):
  pca = PCA(n_components = components)
  pca.fit(data)
  data = pca.transform(data)
  return data, pca

def clustering(data, clusters):
    '''
    Fits a birch model with the data and returns the model.
    '''
    model = Birch(n_clusters = clusters)
    model.fit(data)
    return model

def csvWrite(data, names, artists, ids, model):
    ''' 
    Writes the data with the assigned clusters to a csv file.
    '''
    with open("/home/cluster.csv", "w") as fout:
        csv_writer = csv.writer(fout)
        temp = list(zip(names.values.flatten(), artists.values, ids.values.flatten(), model.labels_))
        temp.sort(key = lambda x: x[3])
        for name, artist, ids, label in temp:
            csv_writer.writerow([name, artist, ids, label])

def migrate(model, scaler, pca):
  '''
  Serializes the model and scaler to pickle files for deployment in Flask.
  '''
  pickle.dump(model, open("model_save.pkl", "wb"))
  pickle.dump(scaler, open("scaler_save.pkl", "wb"))
  pickle.dump(pca, open("pca_save.pkl", "wb"))

def main():
    dataPath = input("Enter the file path for the song data csv file:")
    data, names, artist, ids = dataclean(dataPath)
    X, scaler = normalize(data)
    X, pca = pca(X, 5)
    model = clustering(X, 10000)
    csvWrite(data, names, artist, ids, model)
    migrate(model, scaler, pca)

if __name__ == '__main__':
    main()
© 2020 GitHub, Inc.
