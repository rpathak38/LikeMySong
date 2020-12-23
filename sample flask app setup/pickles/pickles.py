import pickle
import numpy

with open('pickles/model_save.pkl', 'rb') as model_file:
    model = pickle.load(model_file)
with open('pickles/pca_save.pkl', 'rb') as pca_file:
    pca = pickle.load(pca_file)
with open('pickles/scaler_save.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

def online_training(input_data):
    return model.predict(pca.transform(scaler.transform(input_data.reshape(1, -1))))