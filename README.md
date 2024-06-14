## Homografia - Arucos👾
<p align="center">
  <img style="width: 500px; height: auto;" src="">
</p>
Este proyecto creado con python y sus librerias: numpy y cv2, tiene como proposito leer los diferentes codigos arucos para crear una matriz homgrafica y sobreponer un video, ademas si los codigos se acercan demasiado a la camara la escala del video se vera aumentada.

## ¿Como funciona?🤷‍♂️
- Primero debemos obtener los archivos necesarios para el programa, como el video que sobreponemos y importar las libreria `numpy, cv2 y cv2.aruco`.
- Creamos los diferentes **frames** con cv2 para mostrar los resultados.
- En el primer frame mostramos la lectura de los codigos aruco esto lo haremos con `.detectMarkers()`.
- En el segundo frame mostraremos el poligono sobre puesto en los codigos, para esto debemos obtener las esquinas deseadas de los codigos arucos asi:
```python
  p1 = None 
  p2 = None
  p3 = None
  p4 = None
  #Declaramos los 4 puntos donde guardaremos las esquinas, para mostrar el video

  if np.all(ids != None):
      for i in range(len(ids)):
          if ids[i] == 6:
              p1 = (corners[i][0][0][0], corners[i][0][0][1])
          elif ids[i] == 7:
              p2 = (corners[i][0][1][0], corners[i][0][1][1])
          elif ids[i] == 11:
              p3 = (corners[i][0][2][0], corners[i][0][2][1])
          elif ids[i] == 10:
              p4 = (corners[i][0][3][0], corners[i][0][3][1])

    #Almacenamos en p1, p2, p3 y p4 las respectivas esquinas
  ```
- Para terminar el frame 2 debemos de crear un arreglo de numpy y con `.fillPoly()` creamos el poligono.
- En el tercer frame mostramos el video sobrepuesto para esto debemos de crear la matriz homografica con `.findHomography()` ademas debemos de transformar el video para aplicarle la matriz y que este en el espacio del frame esto con `.warpPerspective()` y por ultimo creamos una mascara para luego superponer en el frame, quedaria de esta manera:
```python
ret, frame_mostrar = mostrar.read() #frame del video
    if ret:
        h, status = cv2.findHomography(np.array([(0, 0), (frame_mostrar.shape[1], 0), (frame_mostrar.shape[1], frame_mostrar.shape[0]), (0, frame_mostrar.shape[0])], dtype=np.float32), puntos_aruco)
        #creamos la matriz homografica
        frame_mostrar_transformado = cv2.warpPerspective(frame_mostrar, h, (frame.shape[1], frame.shape[0]))
        #tranformamos el video para aplicarle la matriz y que este en el espacio del frame

        mascara = np.zeros_like(frame3, dtype=np.uint8)
        cv2.fillPoly(mascara, [puntos_aruco.astype(int)], (1, 1, 1))
        
        frame3 = frame3 * (1 - mascara) + frame_mostrar_transformado * mascara # Superponer el resultado de frame_mostrar en el frame 3
``` 
- Por ultimo en el cuarto frame si el poligono se acerca demasiado a la camara el video tendra una escala por 5 desde su esquina inferior derecha, primero debemos obtener el valor de cercania para hacer esto calculamos el area del poligono y el area del frame para luego dividir su valor y obtener el resultado de relacion de areas: 
```python
    area_frame = frame.shape[0] * frame.shape[1] #area del frame
    area_rectangulo = 0.5 * abs(np.cross(puntos_aruco[1] - puntos_aruco[0], puntos_aruco[2] - puntos_aruco[0])) #area de los puntos

    relacion_areas = area_frame / area_rectangulo #resultado
```
- Para aumentar la escala * 5 desde la esquina inferior derecha, debemos multiplicar los puntos respectivos
<p align="center">
  <img style="width: 500px; height: auto;" src="">
</p>

Con esta imagen entendemos el procedimiento, en `p2` (punto 2) modificamos en el eje `x` en `p3` modicamos el eje `x` y el eje `y` y en `p4` modificamos el eje `y`, ahora debemos de programar esto: 
```python
    if relacion_areas <= 7:    
        p1 = (p1[0], p1[1])
        p2 = (p2[0] * 5, p2[1])
        p3 = (p3[0] *  5, p3[1] * 5)
        p4 = (p4[0], p4[1] * 5)
```
## ¿Como puedo probarlo?👌
Debes tener python instalado en tu equipo y ademas tener las librerias necesarias para que funciones, es bastante sencillo abre el buscador de windows y busca "CMD", en tu terminal escribe estos dos comandos uno por uno:
- `py -m pip install numpy`
- `py -m pip install opencv-python`
