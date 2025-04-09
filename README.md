# 🖼️ PrimPy Visor - Procesamiento de Imágenes con Interfaz Gráfica

**PrimPy Visor** es una herramienta interactiva desarrollada con Python y `CustomTkinter`, que permite cargar, modificar, analizar y transformar imágenes digitales mediante diversas operaciones de procesamiento.

Este proyecto combina el uso de una interfaz intuitiva con técnicas avanzadas de manipulación de imágenes a través del paquete personalizado `PrimPy`.

---

## 📂 Estructura del Proyecto

```
📁 PrimPy/
 └── procesamientoImagenes.py    # Módulo con funciones de procesamiento vectorial
📄 visor.py                      # Interfaz gráfica principal en CustomTkinter
📄 README.md                     # Documentación del proyecto
```

---

## 🚀 Funcionalidades Principales

### ✅ Carga y visualización de imágenes

Permite al usuario cargar hasta **dos imágenes** para visualización, fusión o comparación.

```python
file_path = filedialog.askopenfilename(...)
self.image = cv2.imread(file_path)
self.image_original = self.image.copy()
self.current_image = self.image.copy()
```

La imagen es redimensionada con `thumbnail()` solo para mostrarla en el panel sin afectar la original.

---

### 🌈 Ajustes básicos: Brillo y Contraste

Controlados por sliders que modifican la imagen con `cv2.convertScaleAbs`.

```python
alpha = 1 + (contraste / 100.0)  # Factor de contraste
beta = brillo                    # Desplazamiento de brillo
modified = cv2.convertScaleAbs(imagen, alpha=alpha, beta=beta)
```

---

### 🧪 Tipos y canales de imagen

Opciones para visualizar:
- Imagen original
- Escala de grises (Average, Luminosity, Midgray)
- Imagen negativa
- Imagen binarizada

También se puede mostrar solo un canal RGB o CMY, por ejemplo:

```python
def extraerCapaRoja(imagen):
    imagen[:,:,1] = imagen[:,:,2] = 0
    return imagen
```

---

### 📊 Histograma

Muestra un histograma interactivo para cada canal RGB usando `matplotlib`.

```python
plt.bar(range(256), histogram, color=color)
plt.title(f'Histograma Canal {channels[i-1]}')
```

---

## 🔄 Transformaciones geométricas

Se accede desde la barra lateral derecha. Incluye:

### 🔃 Rotación

Rotación libre de cualquier ángulo usando geometría vectorial.

```python
angulo_rad = np.deg2rad(angulo)
# Cálculo inverso de coordenadas para rotar cada pixel
```

### 🧽 Traslación

Mueve la imagen según una coordenada `(dx, dy)`.

```python
nueva_imagen[i + y, j + x] = imagen[i, j]
```

### ✂️ Recorte

Extrae una región rectangular de la imagen.

```python
recorte = imagen[y1:y2, x1:x2]
```

### 🔍 Zoom sobre coordenada

Permite ampliar una zona específica a partir de una coordenada `(x, y)` y un factor `α`.

```python
new_w = int(col / alpha)
recortada = imagen[y1:y2, x1:x2]
```

### 📊 Redimensionamiento

Escala la imagen a un nuevo tamaño con OpenCV.

```python
cv2.resize(imagen, (nuevo_ancho, nuevo_alto))
```

---

## 🧬 Fusión de Imágenes

Permite mezclar dos imágenes con un **slider de transparencia**, usando un factor `α`.

```python
fused = imagen1 * alpha + (1 - alpha) * imagen2
```

También incluye ecualización de niveles si es necesario.

---

## 📀 Guardar / Restaurar

- Guarda la imagen procesada en formato PNG o JPG.
- Restaura la imagen original cargada.
- Elimina imágenes y limpia la interfaz.

```python
cv2.imwrite(file_path, self.current_image)
```

---

## 🧠 Fundamento Teórico

Basado en los conceptos de procesamiento de imágenes enseñados en la clase:

- Representación matricial de imágenes
- Modelos de color RGB y CMY
- Ecualización de imágenes
- Técnicas de escala de grises
- Zoom, rotación, recorte, y traslación

🗞 Apoyado por la presentación:  
`Presentación Procesamiento Imagenes.pdf`

---

## 📷 Tecnologías Usadas

- `Python`
- `NumPy` para procesamiento vectorial
- `OpenCV` para manejo de imágenes
- `Matplotlib` para histogramas
- `Pillow` para compatibilidad con Tkinter
- `CustomTkinter` para interfaz moderna

---

## 🛠️ Cómo ejecutar el visor

```bash
pip install customtkinter numpy opencv-python matplotlib pillow
python visor.py
```

---


## 🤪 Autores

**Juan Pablo Sánchez y Kevin Esguerra**  
📘 Basado en el curso de **Computación gráfica** de la Universidad Tecnológica de Pereira para el docente Francisco Medina
🗓️ 2025
