import tensorflow as tf
from tensorflow.keras.models import load_model
import os
from tensorflow.keras.utils import img_to_array, load_img
import numpy as np

def buat_model(path_model):
    return load_model(path_model)

def predict(tes_path, model):
    img = load_img(tes_path, target_size=(600, 600))
    x = img_to_array(img)
    x /= 255
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    yhat = model.predict(images)
    yhat = np.argmax(yhat, axis=1)[0]
    return yhat

model = buat_model(os.path.join(os.getcwd(),'implementasi_HDD','model_HDD.h5'))
print(predict(os.path.join(os.getcwd(),'implementasi_HDD','1_HDD.jpg'), model))