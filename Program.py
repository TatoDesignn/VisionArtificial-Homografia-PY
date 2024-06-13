import numpy as np
import cv2
import cv2.aruco as aruco

video = cv2.VideoCapture(0, cv2.CAP_DSHOW) #Apertura de la camara 

cv2.namedWindow("Trabajo2", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Trabajo2", 1280, 720) #Redimensionar el tamaño de la ventana 

dictionary = aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250) #inicializar el diccionario, en este caso es 6x6
parameters = cv2.aruco.DetectorParameters() #Inicializar los parametros

detector = cv2.aruco.ArucoDetector(dictionary,parameters) 

mostrar = cv2.VideoCapture("Video.mp4")#Apertura del video 

while True:
    disponible, frame = video.read()#frame donde se muestra los ids

    if not disponible:
        break
    
    frame2 = frame.copy()#frame donde se muestra el rectangulo verde
    frame3 = frame.copy()#frame donde se muestra el video
    frame4 = frame.copy()#frame donde se muestra la ampliacion por un factor de 5
    
    corners, ids, rejected = detector.detectMarkers(frame) #Detectamos los arucos y almacenamos sus ids y sus esquinas 
    cv2.aruco.drawDetectedMarkers(frame, corners, ids) #Mostramos en nuestro frame los cornes y los ids

    p1 = None 
    p2 = None
    p3 = None
    p4 = None #Declaramos los 4 puntos donde guardaremos las esquinas, para mostrar el video

    if np.all(ids != None):
        for i in range(len(ids)):
            if ids[i] == 6:
                p1 = (corners[i][0][0][0], corners[i][0][0][1])
            elif ids[i] == 7:
                p2 = (corners[i][0][1][0], corners[i][0][1][1])
            elif ids[i] == 11:
                p3 = (corners[i][0][2][0], corners[i][0][2][1])
            elif ids[i] == 10:
                p4 = (corners[i][0][3][0], corners[i][0][3][1]) #Almacenamos en p1, p2, p3 y p4 las respectivas esquinas

    if p1 is not None and p2 is not None and p3 is not None and p4 is not None:

        puntos_aruco = np.array([p1, p2, p3, p4], dtype=np.float32) #almacenamos los puntos en un array de numpy

        cv2.fillPoly(frame2, [puntos_aruco.astype(int)], (0, 255, 0)) #Dibujamos el rectangulo verde 
        

        ret, frame_mostrar = mostrar.read() #frame del video

        if ret:
            h, status = cv2.findHomography(np.array([(0, 0), (frame_mostrar.shape[1], 0), (frame_mostrar.shape[1], frame_mostrar.shape[0]), (0, frame_mostrar.shape[0])], dtype=np.float32), puntos_aruco)
            #creamos la matriz homografica
            frame_mostrar_transformado = cv2.warpPerspective(frame_mostrar, h, (frame.shape[1], frame.shape[0]))
            #tranformamos el video para aplicarle la matriz y que este en el espacio del frame

            mascara = np.zeros_like(frame3, dtype=np.uint8)
            cv2.fillPoly(mascara, [puntos_aruco.astype(int)], (1, 1, 1))
             #se crea una mascar en el mismo espacio para luego superponer
            
            frame3 = frame3 * (1 - mascara) + frame_mostrar_transformado * mascara # Superponer el resultado de frame_mostrar en el frame 3
        
        area_frame = frame.shape[0] * frame.shape[1] #area del frame
        area_rectangulo = 0.5 * abs(np.cross(puntos_aruco[1] - puntos_aruco[0], puntos_aruco[2] - puntos_aruco[0])) #area de los puntos

        relacion_areas = area_frame / area_rectangulo #resultado

        if relacion_areas <= 7:    
            p1 = (p1[0], p1[1])
            p2 = (p2[0] * 5, p2[1])
            p3 = (p3[0] *  5, p3[1] * 5)
            p4 = (p4[0], p4[1] * 5)

        if ret:
            h2, status = cv2.findHomography(np.array([(0, 0), (frame_mostrar.shape[1], 0), (frame_mostrar.shape[1], frame_mostrar.shape[0]), (0, frame_mostrar.shape[0])], dtype=np.float32), np.array([p1, p2, p3, p4], dtype=np.float32))
            #creamos la matriz homografica
            frame_mostrar_transformado2 = cv2.warpPerspective(frame_mostrar, h2, (frame.shape[1], frame.shape[0]))
            #tranformamos el video para aplicarle la matriz y que este en el espacio del frame

            mascara2 = np.zeros_like(frame4, dtype=np.uint8)
            cv2.fillPoly(mascara2, [np.array([p1, p2, p3, p4], dtype=np.int32)], (1, 1, 1))
             #se crea una mascar en el mismo espacio para luego superponer
            
            frame4 = frame4 * (1 - mascara2) + frame_mostrar_transformado2 * mascara2 # Superponer el resultado de frame_mostrar en el frame 3

    ventana1 = np.hstack((frame, frame2)) 
    ventana2 = np.hstack((frame3, frame4))

    ventana_final = np.vstack((ventana1, ventana2))

    cv2.imshow("Trabajo2", ventana_final)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()