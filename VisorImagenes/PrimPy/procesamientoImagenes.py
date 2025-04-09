''' Paquete para procesamiento de imagenes '''

# Librerías: numpy para manejo de imágenes comoo arrays, cv2 para cambiar el tamaño de las imágenes y matplotlib para graficar los histogramas.

#---------------------------------------------------------------------- #
import numpy as np
import cv2
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------- #
def cargarImagen(imagen:str):
    '''
    Nombre: cargarImagen

    Descripción: Función que recibe una imagen y la carga en un array numpy

    Parámetro: 
        - imagen (str) - Ruta de la imagen a cargar

    Retorna: 
        - imagen (np.array) - Imagen cargada en un array numpy
    '''
    imagen = np.array(plt.imread(imagen))
    return imagen

# ---------------------------------------------------------------------- #
def mostrarImagen(imagen:np.array, nombre:str):
    '''
    Nombre: mostrarImagen

    Descripción: Función que recibe una imagen y la muestra en una ventana

    Parámetro: 
        - imagen (np.array) - Imagen a mostrar

    Retorna: 
        - None
    '''
    plt.figure(nombre, figsize=(10, 6))
    plt.imshow(imagen)
    plt.axis('off')
    plt.show()
# ---------------------------------------------------------------------- #
def colorearMatriz3X3(matriz:np.array):
    '''
    Nombre: colorearMatriz3X3
    
    Descripcion: Funcion que recibe una matriz 3x3 y la colorea segun la posicion de los elementos

    Parametros: 
        - matriz (np.array) - Matriz 3x3 a colorear

    Retorna: 
        - matriz (np.array) - Matriz 3x3 coloreada
    '''

    matriz[0,0] = [0,1,1] # Cyan
    matriz[0,1,:] = 1 # Blanco
    matriz[0,2] = [1,0,0] # Rojo
    matriz[1,0] = [1,0,1] # Magenta
    matriz[1,1,:] = 0.5 # Gris 
    matriz[1,2] = [0,1,0] # Verde
    matriz[2,0] = [1,1,0] # Amarillo
    matriz[2,1,:] = 0 # Negro
    matriz[2,2] = [0,0,1] # Azul

    return matriz

# ---------------------------------------------------------------------- #

def pintarPartesMatrizColores(matriz:np.array):
    '''
    Nombre: pintarPartesMatrizColores

    Descripción: Pinta una parte de la matriz con colores. Usa slicing.

    Parámetro: 
        - Recibe una matriz

    Retorna: 
        - La matriz con el brillo rebajado (*0.6)
    '''
    matriz[0:6,0] = [1,1,0] # Amarillo una columna
    matriz[0:6,1:3] = [0,1,1] # Cyan doble columna
    matriz[0:6,3:5] = [0,1,0] # Verde doble columna
    matriz[0:6,5:7] = [1,0,1] # Magenta doble columna
    matriz[0:6,7:9] = [1,0,0] # Rojo doble columna
    matriz[0:6,9:11] = [0,0,1] # Azul doble columna

    matriz = pintarMatrizGrises(matriz)

    return matriz * 0.6

def pintarMatrizGrises(matriz:np.array):
    '''
    Nombre: pintarMatrizGrises

    Descripción: Pinta una parte de la matriz con grises específicos. Usa slicing.

    Parámetro: 
        - Recibe una matriz

    Retorna: 
        - La matriz con sus grises
    '''
    for columna in range(8):
        matriz[6:8,columna] = (7-columna)/7

    return matriz

# ---------------------------------------------------------------------- #

def negativa(imagen:np.array):
    '''
    Nombre: negativa

    Descripción: Función que recibe una imagen y retorna la imagen con los colores invertidos

    Parámetro: 
        - imagen (np.array) - Imagen a invertir

    Retorna: 
        - imagen (np.array) - Imagen con los colores invertidos
    '''
    imagen = imagen/255
    return 1 - imagen

# ---------------------------------------------------------------------- #

def extraerCapaRoja(imagen:np.array):
    '''
    Nombre: extraerCapaRoja

    Descripción: Función que recibe una imagen y retorna la capa roja de la imagen

    Parámetro: 
        - imagen (np.array) - Imagen a extraer la capa roja

    Retorna: 
        - imagen (np.array) - Imagen con la capa roja extraida
    '''

    imagen = imagen/255

    imagen[:,:,1] = imagen[:,:,2] = 0

    return imagen

# ---------------------------------------------------------------------- #

def extraerCapaVerde(imagen:np.array):
    '''
    Nombre: extraerCapaVerde

    Descripción: Función que recibe una imagen y retorna la capa verde de la imagen

    Parámetro: 
        - imagen (np.array) - Imagen a extraer la capa verde

    Retorna: 
        - imagen (np.array) - Imagen con la capa verde extraida
    '''

    imagen = imagen/255

    imagen[:,:,0] = imagen[:,:,2] = 0

    return imagen

# ---------------------------------------------------------------------- #

def extraerCapaAzul(imagen:np.array):
    '''
    Nombre: extraerCapaAzul

    Descripción: Función que recibe una imagen y retorna la capa azul de la imagen

    Parámetro: 
        - imagen (np.array) - Imagen a extraer la capa azul

    Retorna: 
        - imagen (np.array) - Imagen con la capa azul extraida
    '''

    imagen = imagen/255

    imagen[:,:,0] = imagen[:,:,1] = 0

    return imagen

# ---------------------------------------------------------------------- #

def extraerCapaMagenta(imagen:np.array):
    '''
    Nombre: extraerCapaMagenta

    Descripción: Función que recibe una imagen y retorna la capa magenta de la imagen

    Parámetro: 
        - imagen (np.array) - Imagen a extraer la capa magenta

    Retorna: 
        - imagen (np.array) - Imagen con la capa magenta extraida
    '''

    imagen = imagen/255
    imagen[:,:,0] = imagen[:,:,2] = 1 

    return imagen

# ---------------------------------------------------------------------- #

def extraerCapaCian(imagen:np.array):
    '''
    Nombre: extraerCapaCian

    Descripción: Función que recibe una imagen y retorna la capa cian de la imagen

    Parámetro: 
        - imagen (np.array) - Imagen a extraer la capa cian

    Retorna: 
        - imagen (np.array) - Imagen con la capa cian extraida
    '''

    imagen = imagen/255
    imagen[:,:,1] = imagen[:,:,2] = 1

    return imagen

# ---------------------------------------------------------------------- #

def extraerCapaAmarilla(imagen:np.array):
    '''
    Nombre: extraerCapaAmarilla

    Descripción: Función que recibe una imagen y retorna la capa amarilla de la imagen

    Parámetro: 
        - imagen (np.array) - Imagen a extraer la capa amarilla

    Retorna: 
        - imagen (np.array) - Imagen con la capa amarilla extraida
    '''

    imagen = imagen/255
    imagen[:,:,0] = imagen[:,:,1] = 1

    return imagen

# ---------------------------------------------------------------------- #
def extraerCapaRGB(imagen:np.array, capa:int):
    '''
    Nombre: extraerCapaRGB

    Descripción: Función que recibe una imagen y retorna la capa RGB de la imagen

    Parámetro: 
        - imagen (np.array) - Imagen a extraer la capa RGB
        - capa (int) - Capa a extraer (0: rojo, 1: verde, 2: azul)

    Retorna: 
        - imagen (np.array) - Imagen con la capa RGB extraida
    '''

    imagen = imagen/255

    if capa == 0:
        return extraerCapaRoja(imagen)
    elif capa == 1:
        return extraerCapaVerde(imagen)
    elif capa == 2:
        return extraerCapaAzul(imagen)
    else:
        raise ValueError("La capa debe ser 0, 1 o 2. Capa 0: Rojo, Capa 1: Verde, Capa 2: Azul")
# ---------------------------------------------------------------------- #
def reconstruirImagenRGB(capaRoja:np.array, capaVerde:np.array, capaAzul:np.array):
    '''
    Nombre: reconstruirImagenRGB

    Descripción: Función que recibe las capas de una imagen y las reconstruye en una imagen RGB

    Parámetros:
        - capaRoja (np.array) - Capa roja de la imagen
        - capaVerde (np.array) - Capa verde de la imagen
        - capaAzul (np.array) - Capa azul de la imagen

    Retorna:
        - imagen (np.array) - Imagen reconstruida
    '''

    imagen = capaRoja + capaVerde + capaAzul

    return imagen*255

# ---------------------------------------------------------------------- #
def cambiarTamaño(imagen:np.array, nuevoTamaño:tuple):
    '''
    Nombre: cambiarTamaño

    Descripción: Función que recibe una imagen y un nuevo tamaño y cambia el tamaño de la imagen

    Parámetros:
        - imagen (np.array) - Imagen a cambiar de tamaño
        - nuevoTamaño (tuple) - Nuevo tamaño de la imagen

    Retorna:
        - imagen (np.array) - Imagen con el nuevo tamaño
    '''

    imagen = cv2.resize(imagen, nuevoTamaño)

    return imagen

# ---------------------------------------------------------------------- #
def fusionarImagenesSinEq(imagen1:np.array, imagen2:np.array):
    '''
    Nombre: fusionarImagenes

    Descripción: Función que recibe dos imagenes y las fusiona en una sola imagen sin factor de ecualización, teniendo en cuenta que las imagenes deben ser del mismo tamaño

    Parámetros:
        - imagen1 (np.array) - Imagen 1 a fusionar
        - imagen2 (np.array) - Imagen 2 a fusionar
    
    Retorna:
        - imagen (np.array) - Imagen fusionada
    '''

    imagen1 = imagen1/255
    imagen2 = imagen2/255

    if imagen1.shape != imagen2.shape:
        raise ValueError("Las imagenes deben tener el mismo tamaño")
    else:
        return imagen1 + imagen2

# ---------------------------------------------------------------------- #
def fusionarImagenesConEq(imagen1:np.array, imagen2:np.array, factorEq:float):
    '''
    Nombre: fusionarImagenesConEq

    Descripción: Función que recibe dos imagenes y las fusiona en una sola imagen con un factor de ecualización, teniendo en cuenta que las imagenes deben ser del mismo tamaño

    Parámetros:
        - imagen1 (np.array) - Imagen 1 a fusionar 
        - imagen2 (np.array) - Imagen 2 a fusionar
        - factorEq (float) - Factor de ecualización entre 0 y 1
    
    Retorna:
        - imagen (np.array) - Imagen fusionada
    '''

    imagen1 = imagen1/255
    imagen2 = imagen2/255

    if imagen1.shape != imagen2.shape:
        raise ValueError("Las imagenes deben tener el mismo tamaño")
    else:
        if factorEq < 0:
            raise ValueError("El factor de ecualización debe ser mayor que 0")
        else:
            return (imagen1*factorEq) + (1 - factorEq)*imagen2

# ---------------------------------------------------------------------- #
def ecualizarImg(imagen:np.array, factor:float):
    '''
    Nombre: ecualizarImg
    
    Descripción: Función que recibe una imagen y un factor y ecualiza la imagen por el factor

    Parámetros:
        - imagen (np.array) - Imagen a ecualizar
        - factor (float) - Factor de ecualización entre 0 y 1
    
    Retorna:
        - imagen (np.array) - Imagen ecualizada
    '''
    
    imagen = imagen/255

    if factor < 0:
        raise ValueError("El factor de ecualización debe ser mayor que 0")
    else:
        return imagen * factor

# ---------------------------------------------------------------------- #
def grisesConAverage(imagen:np.array):
    '''
    Nombre: grisesConAverage

    Descripción: Función que recibe una imagen y la convierte a escala de grises usando el método de average

    Parámetro:
        - imagen (np.array) - Imagen a convertir a escala de grises

    Retorna:
        - imagen (np.array) - Imagen en escala de grises
    '''

    imagen = imagen/255

    imagen = (imagen[:,:,0] + imagen[:,:,1] + imagen[:,:,2]) / 3

    return imagen
# ---------------------------------------------------------------------- #
def grisesConLuminosity(imagen:np.array):
    '''
    Nombre: grisesConLuminosity

    Descripción: Función que recibe una imagen y la convierte a escala de grises usando el método de luminosity

    Parámetro:
        - imagen (np.array) - Imagen a convertir a escala de grises

    Retorna:
        - imagen (np.array) - Imagen en escala de grises
    '''

    imagen = imagen/255

    imagenGris = imagen[:,:,0]*0.299 + imagen[:,:,1]*0.587 + imagen[:,:,2]*0.114

    return imagenGris
# ---------------------------------------------------------------------- #
def grisesConMidgray(imagen:np.array):
    '''
    Nombre: grisesConMidgray

    Descripción: Función que recibe una imagen y la convierte a escala de grises usando el método de midgray

    Parámetro:
        - imagen (np.array) - Imagen a convertir a escala de grises

    Retorna:
        - imagen (np.array) - Imagen en escala de grises
    '''

    imagen = imagen/255

    # Obtener el valor mínimo y máximo de la imagen
    min_val = np.minimum(imagen[:,:,0], np.minimum(imagen[:,:,1], imagen[:,:,2]))
    max_val = np.maximum(imagen[:,:,0], np.maximum(imagen[:,:,1], imagen[:,:,2]))

    # Calcular el tono medio
    imagenGris = (max_val + min_val) / 2  

    return imagenGris
# ---------------------------------------------------------------------- #
def ajustarBrillo(imagen:np.array, brillo:float):
    '''
    Nombre: ajustarBrillo

    Descripción: Función que recibe una imagen y un brillo y ajusta el brillo de la imagen

    Parámetros:
        - imagen (np.array) - Imagen a ajustar el brillo
        - brillo (float) - Brillo a ajustar entre -1 y 1
    
    Retorna:
        - imagen (np.array) - Imagen con el brillo ajustado
    '''

    imagen = imagen/255

    if brillo < -1 or brillo > 1:
        raise ValueError("El brillo debe estar entre -1 y 1")
    else:
        return imagen + brillo
# ---------------------------------------------------------------------- #
def ajustarBrilloCapa(imagen:np.array, brillo:float, capa:int):
    '''
    Nombre: ajustarBrilloCapa

    Descripción: Función que recibe una imagen y un brillo y ajusta el brillo de la imagen en la capa especificada

    Parámetros:
        - imagen (np.array) - Imagen a ajustar el brillo
        - brillo (float) - Brillo a ajustar entre -1 y 1
        - capa (int) - Capa a ajustar el brillo (0: rojo, 1: verde, 2: azul)
    
    Retorna:
        - imagen (np.array) - Imagen con el brillo ajustado
    '''

    imagen = imagen/255

    if brillo < -1 or brillo > 1:
        raise ValueError("El brillo debe estar entre -1 y 1")
    else:
        imagen[:,:,capa] = imagen[:,:,capa] + brillo

    return imagen
# ---------------------------------------------------------------------- #
def contrastarZonasOscuras(imagen:np.array, factor:float):
    '''
    Nombre: contrastarZonasOscuras

    Descripción: Función que recibe una imagen y un factor y contrasta las zonas oscuras de la imagen por el factor

    Parámetros:
        - imagen (np.array) - Imagen a contrastar
        - factor (float) - Factor de contraste mayor que 0
    
    Retorna:
        - imagen (np.array) - Imagen con el contraste ajustado
    '''

    imagen = imagen/255

    if factor < 0:
        raise ValueError("El factor de contraste debe ser mayor que 0")
    else:
        imagen_contraste = factor*np.log10(imagen + 1) 
        return imagen_contraste
# ---------------------------------------------------------------------- #
def contrastarZonasClaras(imagen:np.array, factor:float):
    '''
    Nombre: contrastarZonasClaras

    Descripción: Función que recibe una imagen y un factor y contrasta las zonas claras de la imagen por el factor

    Parámetros:
        - imagen (np.array) - Imagen a contrastar
        - factor (float) - Factor de contraste mayor que 0
    
    Retorna:
        - imagen (np.array) - Imagen con el contraste ajustado
    '''

    imagen = imagen/255

    if factor < 0:
        raise ValueError("El factor de contraste debe ser mayor que 0")
    else:
        imagen_contraste = factor*np.exp(imagen - 1) 
        return imagen_contraste
# ---------------------------------------------------------------------- #
def zoom(imagen: np.array, alpha: float, coord: tuple):
    '''
    Nombre: zoom

    Descripción: Realiza un zoom en la imagen centrado en la coordenada especificada.

    Parámetros:
        - imagen: np.array -> Imagen de entrada en formato numpy array.
        - alpha: float -> Factor de zoom (>1 amplía, <1 reduce).
        - coord: tuple -> Coordenada (x, y) que se mantendrá en el centro del zoom.

    Retorna:
        - nueva_imagen np.array con la imagen redimensionada.
    '''
    imagen = imagen / 255  
    fil, col, _ = imagen.shape
    x, y = coord

    # Definir el tamaño del recorte basado en el factor de zoom
    if alpha <= 0 or alpha > 100:
        raise ValueError("El factor de zoom debe estar en el rango (0, 100) sin ser cero.")
    else:
        new_w = int(col / alpha)
        new_h = int(fil / alpha)

    # Calcular los límites de la región de zoom
    x1 = max(x - new_w // 2, 0)
    x2 = min(x + new_w // 2, col)
    y1 = max(y - new_h // 2, 0)
    y2 = min(y + new_h // 2, fil)

    # Extraer la región de interés
    imagen_recortada = imagen[y1:y2, x1:x2]

    # Crear una nueva imagen con el tamaño original
    nueva_imagen = np.zeros_like(imagen)

    # Escalar manualmente con interpolación simple (repetición de píxeles)
    for i in range(fil):
        for j in range(col):
            orig_x = int((j / col) * imagen_recortada.shape[1])
            orig_y = int((i / fil) * imagen_recortada.shape[0])
            nueva_imagen[i, j] = imagen_recortada[orig_y, orig_x]

    return nueva_imagen
# ---------------------------------------------------------------------- #
def binarizar(imagen: np.array, umbral: float):
    '''
    Nombre: binarizar

    Descripción: Binariza una imagen en escala de grises.

    Parámetros:
        - imagen: np.array -> Imagen en escala de grises con valores en el rango [0,1].'
        - umbral: float -> Umbral de binarización.'
    Retorna:
        - Imagen binarizada.''
    '''
    imagen = imagen / 255  

    if len(imagen.shape) == 3:  # Si tiene 3 dimensiones, se convierte a escala de grises
        grises = (imagen[:,:,0] + imagen[:,:,1] + imagen[:,:,2]) / 3  # Promedio de los canales para escala de grises

    return (grises >= umbral)  # Convierte la imagen en binaria (0 o 1)
# ---------------------------------------------------------------------- #
def rotar(imagen: np.array, angulo: float):
    '''
    Nombre: rotar

    Descripción: Rota una imagen en cualquier ángulo usando solo NumPy.

    Parámetros:
        - imagen: np.array -> Imagen en formato NumPy con forma (alto, ancho, canales).
        - angulo: float -> Ángulo de rotación en grados (puede ser cualquier número real).

    Retorna:
        - np.array -> Imagen rotada.
    '''

    # Convertir ángulo a radianes
    angulo_rad = np.deg2rad(angulo)

    # Dimensiones originales de la imagen
    alto, ancho = imagen.shape[:2]

    # Calcular la matriz de rotación
    cos_a, sin_a = np.cos(angulo_rad), np.sin(angulo_rad)

    # Nuevas dimensiones de la imagen rotada
    nuevo_ancho = int(abs(ancho * cos_a) + abs(alto * sin_a))
    nuevo_alto = int(abs(ancho * sin_a) + abs(alto * cos_a))

    # Crear la imagen de salida vacía
    imagen_rotada = np.zeros((nuevo_alto, nuevo_ancho, imagen.shape[2]), dtype=imagen.dtype)

    # Centro de la imagen original y la rotada
    centro_x, centro_y = ancho / 2, alto / 2
    nuevo_centro_x, nuevo_centro_y = nuevo_ancho / 2, nuevo_alto / 2

    # Aplicar la transformación inversa para cada píxel en la imagen rotada
    for i in range(nuevo_alto):
        for j in range(nuevo_ancho):
            # Coordenadas en la imagen original
            x = (j - nuevo_centro_x) * cos_a + (i - nuevo_centro_y) * sin_a + centro_x
            y = -(j - nuevo_centro_x) * sin_a + (i - nuevo_centro_y) * cos_a + centro_y

            # Verificar si las coordenadas están dentro de la imagen original
            if 0 <= int(y) < alto and 0 <= int(x) < ancho:
                imagen_rotada[i, j] = imagen[int(y), int(x)]

    return imagen_rotada
# ---------------------------------------------------------------------- #
def trasladar(imagen:np.array, coordenadas:tuple):
    """
    Nombre: trasladar

    Descripción: Traslada una imagen a las coordenadas indicadas

    Parametros:
        - imagen: np.array: imagen a trasladar
        - coordenadas: tuple: coordenadas a las que se trasladará la imagen

    Retorna:
        - np.array: imagen trasladada
    """

    x, y = coordenadas
    nueva_imagen = np.zeros_like(imagen)
    for i in range(imagen.shape[0]):
        for j in range(imagen.shape[1]):
            if i + y < imagen.shape[0] and j + x < imagen.shape[1]:
                nueva_imagen[i + y, j + x] = imagen[i, j]
    return nueva_imagen
# ---------------------------------------------------------------------- #
def recortar(imagen:np.array, coordX:tuple, coordY:tuple):
    """
    Nombre: recortar

    Descripción: Recorta una imagen a las coordenadas indicadas

    Parameters:
        - imagen: np.array: imagen a recortar
        - coordX: tuple: x inicial y final
        - coordY: tuple: y inicial y final

    Returns:
        - np.array: imagen recortada
    """
    x1, x2 = coordX
    y1, y2 = coordY
    
    nueva_imagen = imagen[x1:x2, y1:y2]
    return nueva_imagen
# ---------------------------------------------------------------------- #
def histograma(image_array:np.array):
    '''
    Nombre: histograma

    Descripción: Función que recibe una imagen y muestra su histograma por canal RGB.

    Parametros:	
        - image_array: np.array -> Imagen a mostrar el histograma.
    '''
    channels = ['Rojo', 'Verde', 'Azul']
    colors = ['r', 'g', 'b']
    
    plt.figure("Histograma de la Imagen", figsize=(10, 6))
    
    for i, (channel, color) in enumerate(zip(range(3), colors), 1):
        plt.subplot(4, 1, i+1)
        histogram, bins = np.histogram(image_array[:, :, channel], bins=256, range=(0, 256))
        plt.bar(range(256), histogram, color=color)
        plt.title(f'Histograma Canal {channels[i-1]}')
        plt.xlabel('Intensidad')
        plt.ylabel('Frecuencia')
    
    plt.subplot(4, 1, 1)
    plt.imshow(image_array/255)
    plt.axis('off')
    plt.title('Imagen Original')
    
    plt.tight_layout()
    plt.show()