import face_recognition
import cv2
import numpy as np
import paho.mqtt.client as mqtt #import the client1
import time
import os
import sys
import random
import datetime
import telepot
import nextcloud_client
import paho.mqtt.client as mqtt

global face2_names
face2_names= []
global reiniciar
id2=0



def on_message(client, data, msg):
    global apagar
    if msg.topic == 'm1/lampara':
        if msg.payload==b'puertaabierta':
            client.publish('m1/delay', "delay")
    if msg.topic == 'm1/alarma2':
        if msg.payload==b'desactivar':
            apagar=0
    if msg.topic == 'm1/delay':
        if msg.payload==b'delay2':
            print("22")
            if (face2_names != ['Javier Ruiz'] and face2_names != ['Unknown']):
                client.publish('m1/alarma', 'noidentificado')
                bot.sendMessage(id2, 'ALERTA Alguien ha entrado en casa sin identificarse')
                
                


correcto=1
nc = nextcloud_client.Client('http://172.30.161.252:8080')
nc.login('admin', 'n3mj4xSjWws9qp')

timer22 =5
timer21=5
apagar=1





def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    global id2
    id2=str(chat_id)

    if command == 'photo':
        path=os.getenv("HOME")
        cv2.imwrite(os.path.join('/home/pi', f'alarma3.jpg'), frame)
        bot.sendPhoto(id2, open(path + '/alarma3.jpg', 'rb'))
    if command == 'start':
        bot.sendMessage(id2, 'Bot correctamente inicializado')
        

bot = telepot.Bot('5049731123:AAEvLUPb77z8keB3z4PDUYZmNmh8cUAGhlA')
bot.message_loop(handle)
nc = nextcloud_client.Client('http://172.30.161.252:8080')
nc.login('admin', 'n3mj4xSjWws9qp')

timer=0
current_frame=0
# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
broker_address="172.30.161.252"
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1")
client.on_message=on_message#create new instance
print("connecting to broker")
client.username_pw_set(username="javierruiz", password="Javier14")
client.connect("172.30.161.252", 1883, 60)
client.subscribe("m1/lampara")
client.subscribe("m1/delay")
client.subscribe("m1/alarma2")
client.loop_start()



video_capture = cv2.VideoCapture(0)

javier_image = face_recognition.load_image_file("yo2.jpg")
javier_face_encoding = face_recognition.face_encodings(javier_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    javier_face_encoding
]
known_face_names = [
    "Javier Ruiz"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while (apagar==1):
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame
    

        
    for(top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        date_string = time.strftime("%d-%m-%Y-%H:%M")
        if(face_names==['Javier Ruiz']):
            face2_names=['Javier Ruiz']
            client.loop_start()
            timer21=timer21-1
            if(timer<time.time() and timer21<=0):
                timer= float(time.time() + 10)
                print("Soy yo")
                client.publish('m1/alarma', 'javier')
                if video_capture.isOpened():
                    ret, frame = video_capture.read()
                    if ret:
                        global pathmio
                        pathmio = '/home/pi/envmqtt'
                        print(f"Creating file...")
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                        cv2.imwrite(os.path.join(pathmio, f'CORRECTAalarma{current_frame}.jpg'), frame)
                        if(id2 !=0):
                            bot.sendPhoto(id2, open(pathmio + f'/CORRECTAalarma{current_frame}.jpg', 'rb'))
                            bot.sendMessage(id2, 'Bienvenido Javi!')
                        nc.put_file('controlalarma/ALARMACORRECTA' + date_string + '.jpg', f'CORRECTAalarma{current_frame}.jpg')
                    current_frame += 1
                    timer21=5
        elif(face_names==['Unknown']):
            client.loop_start()
            timer22 = timer22 - 1
            if(timer22==0 and correcto==1):
                if(face_names==['Unknown']):
                    face2_names=['Unknown']
                    print("Intruso")
                    client.publish('m1/alarma', 'desconocido')
                    if video_capture.isOpened():
                        ret, frame = video_capture.read()
                        if ret:
                            pathmio = '/home/pi/envmqtt'
                            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                            font = cv2.FONT_HERSHEY_DUPLEX
                            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                            cv2.imwrite(os.path.join(pathmio, f'INTRUSOalarma{current_frame}.jpg'), frame)
                            if(id2 !=0):
                                bot.sendPhoto(id2, open(pathmio + f'/INTRUSOalarma{current_frame}.jpg', 'rb'))
                                bot.sendMessage(id2, 'ALERTA Alguien ha entrado en casa')
                            nc.put_file('controlalarma/ALARMAINTRUSO' + date_string + '.jpg', f'INTRUSOalarma{current_frame}.jpg')
                            timer22=5
                            correcto=0
                        
    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
