import face_recognition
import cv2
import numpy as np
import paho.mqtt.client as mqtt #comunicación mqtt
import time
import os
import sys
import random
import datetime
import telepot                #librería para comunicación telegram
import nextcloud_client       #para comunicación con servidor Nextcloud

global face2_names           #definimos un vector global para almacenar caras que nos será de utilidad más adelante
face2_names= []
global reiniciar             #variable para tratar de reiniciar el programa tras pararlo (sin éxito)
                       



def on_message(client, data, msg):  #funcion on_message para comunicación mqtt
    global apagar                   #usamos esta función para escuchar topics y mensajes especificos de nuestro interés
    if msg.topic == 'm1/lampara':
        if msg.payload==b'puertaabierta':
            client.publish('m1/delay', "delay") #enviamos el delay tras detectar que alguien ha entrado a casa
    if msg.topic == 'm1/alarma2':    #sale del programa poniendo apagar a 0
        if msg.payload==b'desactivar':
            apagar=0
    if msg.topic == 'm1/delay':      #respuesta (procesada en nodered al delay anterior
        if msg.payload==b'delay2':   #si nadie se ha identificado en la duración del delay, salta mensaje MQTT y mensaje a telegram
            print("22")
            if (face2_names != ['Javier Ruiz'] and face2_names != ['Unknown']):
                client.publish('m1/alarma', 'noidentificado')
                bot.sendMessage(id2, 'ALERTA Alguien ha entrado en casa sin identificarse')
                
                


correcto=1  #variable auxiliar que usaremos para dejar de actuar si hay intruso
nc = nextcloud_client.Client('http://172.30.161.252:8080') #inicializamos NC
nc.login('admin', 'n3mj4xSjWws9qp') #datos nextcloud

timer22 =5 #variables auxiliares en la identificación facial
timer21=5
apagar=1 #variable apagar encargada de la ejecución del programa





def handle(msg): #función para establecer comandos a bot telegram (interés especial inicializarlo)
    chat_id = msg['chat']['id']
    command = msg['text']
    global id2 #extraemos el chat_id en una variable global para usarlo a la hora de enviar mensajes a telegram
    id2=str(chat_id)

    if command == 'photo': #comando photo hace y envía foto a telegram
        path=os.getenv("HOME")
        cv2.imwrite(os.path.join('/home/pi', f'alarma100.jpg'), frame)
        bot.sendPhoto(id2, open(path + '/alarma100.jpg', 'rb'))
    if command == 'start': #inicializar nos da un valor de id2 y permite comunicación con telegram
        bot.sendMessage(id2, 'Bot correctamente inicializado')
        

bot = telepot.Bot('5049731123:AAEvLUPb77z8keB3z4PDUYZmNmh8cUAGhlA') #inicializamos el bot
bot.message_loop(handle)


timer=0
current_frame=0


broker_address="172.30.161.252" #broker MQTT

print("creating new instance") #Iniciamos toda la comunicación MQTT correctamente
client = mqtt.Client("P1")
client.on_message=on_message
print("connecting to broker")
client.username_pw_set(username="javierruiz", password="Javier14")
client.connect("172.30.161.252", 1883, 60)
client.subscribe("m1/lampara") #Nos suscribimos a topicos de nuestro interés para que on_message pueda escuchar adecuadamente
client.subscribe("m1/delay")
client.subscribe("m1/alarma2")
client.loop_start()



video_capture = cv2.VideoCapture(0) #Comenzamos la captura de video con OpenCV

javier_image = face_recognition.load_image_file("yo2.jpg") #Introducimos identificación facial a partir de foto previa
javier_face_encoding = face_recognition.face_encodings(javier_image)[0]

#se crea el array de codificaciones de caras conocidas y se les da un nombres
#en mi caso array de un solo elemento
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

while (apagar==1): #condicion apagar
  
    ret, frame = video_capture.read()

    #reducimos el tamaño de video para procesar con mayor rapidez
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
            
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown" #en principio name=desconocido

           
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]: #si hay alguna coincidencia, name=la mejor coincidencia
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame
    

        
    for(top, right, bottom, left), name in zip(face_locations, face_names): #funcion para procesado de imagen
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        date_string = time.strftime("%d-%m-%Y-%H:%M") #formato fecha de mi interes
        if(face_names==['Javier Ruiz']): #si me reconoce:
            face2_names=['Javier Ruiz'] #grabamos en un auxiliar para tratarlo por separado y poder identificar intruso con este vector
            client.loop_start() #reiniciamos com mqtt, puesto que a veces se para
            timer21=timer21-1 #se debe reconocer la cara 5 veces para evitar falsas detecciones
            if(timer<time.time() and timer21<=0):
                timer= float(time.time() + 10) #contador para no realizar detecciones que se "pisen"
                print("Soy yo")
                client.publish('m1/alarma', 'javier') #enviamos por mqtt que soy yo
                if video_capture.isOpened():
                    ret, frame = video_capture.read()
                    if ret:
                        global pathmio
                        pathmio = '/home/pi/envmqtt' #seleccionamos directorio
                        print(f"Creating file...")
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX #dibujamos rectangulo y ponemos el nombre del identificado
                        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                        cv2.imwrite(os.path.join(pathmio, f'CORRECTAalarma{current_frame}.jpg'), frame) #grabamos imagen del video
                        if(id2 !=0): #si se ha inicializado el bot... enviamos foto y mensaje
                            bot.sendPhoto(id2, open(pathmio + f'/CORRECTAalarma{current_frame}.jpg', 'rb'))
                            bot.sendMessage(id2, 'Bienvenido Javi!')
                        nc.put_file('controlalarma/ALARMACORRECTA' + date_string + '.jpg', f'CORRECTAalarma{current_frame}.jpg')
                    current_frame += 1 #avanzamos currentframe para no sobreescribir y reiniciamos timer21 para tener que detectar 5 veces la misma cara
                    timer21=5
        elif(face_names==['Unknown']): #proceso muy similar con "Unknown"
            client.loop_start()
            timer22 = timer22 - 1
            if(timer22==0 and correcto==1): #si se detecta desconocido, correcto=0, ya no salta más ahí, se entiende que el administrador debe invervenir pues le están robando en casa
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
