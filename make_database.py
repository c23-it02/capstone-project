from mtcnn import MTCNN
import cv2
import os
import numpy as np
import pickle
from keras_facenet import FaceNet

def make_database_should_crop(path):
    my_facenet = FaceNet()
    database = {}
    detector = MTCNN()
    for image in os.listdir(path):
        path_image = os.path.join(path, image)
        img = cv2.imread(path_image)
        posisi = detector.detect_faces(img)
        x1, y1, w, h = posisi[0]['box']
        x2, y2 = x1 + w, y1 + h
        img = img[y1:y2, x1:x2]
        img = Image.fromarray(img)
        img = img.resize((160, 160))
        img = asarray(img)
        img = np.expand_dims(img, axis=0)
        database[image.split('.')[0]] = my_facenet.embeddings(img)[0]
    return database

def make_database(path):
    my_facenet = FaceNet()
    database = {}
    for image in os.listdir(path):
        path_image = os.path.join(path, image)
        img = cv2.imread(path_image)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = img.resize((160, 160))
        img = asarray(img)
        img = np.expand_dims(img, axis=0)
        database[image.split('.')[0]] = my_facenet.embeddings(img)[0]
    return database

def simpan_database(database):
    myfile = open("data.pkl", "wb")
    pickle.dump(database, myfile)
    myfile.close()

#kalo fotonya belom dicrop
database = make_database_should_crop(os.path.join(os.getcwd(), 'Data'))
#kalo fotonya sudah dicrop
database = make_database(os.path.join(os.getcwd(), 'Data'))
#pilih salah satu yaa
simpan_database(database)