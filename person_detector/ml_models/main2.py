from mtcnn import MTCNN
import cv2
import os
from keras_facenet import FaceNet
import tensorflow as tf
import numpy as np
from PIL import Image
from numpy import asarray
from django.conf import settings
import pickle
from django.utils import timezone
import time
from person_detector.models import DetectedFace, IpCamera
from django.shortcuts import get_object_or_404

import paho.mqtt.client as mqtt
import json

# Konfigurasi MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
    else:
        print("Failed to connect, return code %d" % rc)

def on_publish(client, userdata, mid):
    print("Message successfully published")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT Broker")

def connect_mqtt():
    client = mqtt.Client()
    client.username_pw_set("87f91c55-b35f-46dc-b876-60606d526e4a", "M44o0Tz3DotSYbOQuIfOvwVlhVgVz0BDQcg4kTKeAQMUtAHzC4h6kdki7RkpeUBzWH5xjW7rmPYeDUCc")  # Ganti dengan nama pengguna dan kata sandi yang sesuai
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    # Ganti dengan alamat dan port broker MQTT yang sesuai
    broker_address = "telemetry.iotstadium.com"
    port = 1883

    try:
        client.connect(broker_address, port)
        client.loop_start()
        return client
    except Exception as e:
        print("Error connecting to MQTT Broker:", str(e))
        return None

def send_mqtt_message(client, topic, message):
    try:
        json_message = json.dumps(message)
        result, mid = client.publish(topic, json_message)
        if result == mqtt.MQTT_ERR_SUCCESS:
            print('Message successfully sent')
        else:
            print('Failed to send message, return code %d' % result)
    except Exception as e:
        print("Error sending MQTT message:", str(e))

def disconnect_mqtt(client):
    client.loop_stop()
    client.disconnect()

def send_message_to_mqtt(pesan):
    client = connect_mqtt()
    if client:
        topic = '87f91c55-b35f-46dc-b876-60606d526e4a'
        message = pesan
        send_mqtt_message(client, topic, message)
        disconnect_mqtt(client)
# Akhir Konfigurasi


my_facenet = FaceNet()

def make_database_should_crop(path):
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


def simpan_database(database):
    myfile = open("data.pkl", "wb")
    pickle.dump(database, myfile)
    myfile.close()

def cos_similarity(anchor, test):
    a = np.matmul(np.transpose(anchor), test)
    b = np.sum(np.multiply(anchor, test))
    c = np.sum(np.multiply(test, test))
    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))

database_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'person_detector')
database = make_database_should_crop(database_path)


def open_camera():
    database = make_database_should_crop(database_path)
    simpan_database(database)

    pickle_file = os.path.join(settings.BASE_DIR, 'person_detector', 'ml_models', 'data.pkl')
    with open(pickle_file, 'wb') as myfile:
        pickle.dump(database, myfile)

    haarscascade_path = os.path.join(settings.BASE_DIR, 'person_detector', 'ml_models', 'haarcascade.xml')
    detector = cv2.CascadeClassifier(haarscascade_path)

    last_print_time = time.time()

    camera = IpCamera.objects.latest()
    address = camera.ip_camera
    vid = cv2.VideoCapture(0)
    while(True):
        ret, frame = vid.read()
        wajah = detector.detectMultiScale(frame, scaleFactor = 1.2, minNeighbors = 5)
        if wajah is not None:
            for x1, y1, w, h in wajah:
                x2 = x1 + w
                y2 = y1 + h
                muka = frame[y1:y2, x1:x2]
                muka = cv2.cvtColor(muka, cv2.COLOR_BGR2RGB)
                muka = Image.fromarray(muka)
                muka = muka.resize((160,160)) 
                muka = asarray(muka)
                muka = np.expand_dims(muka, axis=0)
                test_embedder = my_facenet.embeddings(muka)[0]
                i = 100
                k = 'Unknown'
                
                for key in database:
                    distance = cos_similarity(database.get(key), test_embedder)
                    if (distance < i) & (distance < 0.5):
                        i = distance
                        k = key
                
                if k:
                    current_time = timezone.now()
                    if time.time() - last_print_time >= 1:
                        detected_face = DetectedFace.objects.create(name=k, detected_time=current_time)
                        detected_face.save()
                        last_print_time = time.time()  # Memperbarui waktu terakhir pesan dicetak dan data disimpan
                            
                        formatted_time = current_time.strftime('%d%m%Y')
                        pesan = {
                            'name': k,
                            'timestamp': formatted_time
                        }
                        send_message_to_mqtt(pesan)

                        print(f"Nama wajah terdeteksi: {k}; Waktu: {current_time}")
                    


                frame = cv2.rectangle(frame, (x1,y1), (x2,y2), (255,255,255), 1)
                frame = cv2.putText(frame, k, (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                cv2.imshow('frame', frame)
            
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break
    
    vid.release()
    cv2.destroyAllWindows()