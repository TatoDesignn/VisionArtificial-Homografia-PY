## Homografia - Arucos👾
<p align="center">
  <img style="width: 500px; height: auto;" src="">
</p>
Este proyecto creado con python y sus librerias: numpy y cv2, tiene como proposito leer los diferentes codigos arucos para crear una matriz homgrafica y sobreponer un video, ademas si los codigos se acercan demasiado a la camara la escala del video se vera aumentada.

## ¿Como funciona?🤷‍♂️
- Primero debemos obtener los archivos necesarios para el programa, como el video que sobreponemos y importar las libreria `numpy, cv2 y cv2.aruco` 
- Creamos los diferentes **frames** con cv2 para mostrar los resultados.
- En el primer frame mostramos la lectura de los codigos aruco esto lo haremos con `.detectMarkers()`
- En el segundo frame mostraremos el rectangulo sobre puesto en los codigos, para esto debemos obtener las esquinas deseadas de los codigos arucos asi:
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

      #Almacenamos en p1, p2, p3 y p4 las respectivas esquinas´´´


