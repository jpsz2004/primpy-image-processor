# ImageViewer 📸✨

Bienvenido al **ImageViewer**, un visor interactivo de imágenes desarrollado en Python que utiliza **CustomTkinter** para una interfaz moderna y un toque de magia en el procesamiento de imágenes. Con este proyecto podrás:

- **Cargar y visualizar imágenes** (¡incluso dos al mismo tiempo para efectos de fusión!)
- **Aplicar transformaciones geométricas** como rotación, traslación, recorte, cambio de tamaño y zoom
- **Ajustar parámetros de procesamiento** como brillo y contraste
- **Fusionar imágenes** con un control deslizante de transparencia
- **Procesar imágenes** convirtiéndolas a escala de grises, negativo o binarizadas y extraer sus canales RGB/CMY

Este proyecto se apoya en la biblioteca [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) y en funciones personalizadas definidas en el módulo `procesamientoImagenes` (alias `pi`) para transformar las imágenes de forma súper cool. 😁

---

## Tabla de Contenidos

- [Características](#características)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Funcionalidades Clave y Fragmentos de Código](#funcionalidades-clave-y-fragmentos-de-código)
- [Requisitos e Instalación](#requisitos-e-instalación)
- [Uso](#uso)
- [Autores](#autores)
- [Licencia](#licencia)

---

## Características 🚀

- **Carga y Visualización:**  
  Permite seleccionar una o dos imágenes y visualizarlas en paneles separados.
  
- **Transformaciones Geométricas:**  
  Rotación, traslación, recorte, cambio de tamaño y zoom, todo en tiempo real.
  
- **Ajustes de Brillo y Contraste:**  
  Modifica parámetros para mejorar la visualización mediante sliders intuitivos.
  
- **Fusión de Imágenes:**  
  Combina dos imágenes usando un control de transparencia para obtener un efecto de fusión interesante.
  
- **Procesamiento de Canales:**  
  Selecciona y extrae capas específicas de canales RGB o CMY para análisis o efectos visuales.

---

## Estructura del Proyecto 📁

El proyecto está organizado en varias secciones que facilitan el mantenimiento y la extensión del código:

- **`visor.py`:**  
  Contiene la clase principal `ImageViewer` que extiende de `ctk.CTk` para crear la interfaz.
  
- **Módulo `procesamientoImagenes` (alias `pi`):**  
  Provee funciones especializadas para la manipulación y transformación de imágenes, como:  
  - `pi.trasladar`
  - `pi.recortar`
  - `pi.cambiarTamaño`
  - `pi.zoom`
  - `pi.rotar`
  - `pi.ajustarBrillo`
  - `pi.contrastarZonasClaras` y `pi.contrastarZonasOscuras`
  - Entre otras para procesamiento de canales y fusión.

- **Interfaz Gráfica:**  
  La interfaz se divide en tres áreas:
  - **Topbar:** Para botones de carga, guardado, restauración y eliminación de imágenes.
  - **Sidebar Izquierda:** Para controles de procesamiento, ajustes, selección de tipo de imagen y fusión.
  - **Sidebar Derecha:** Para transformaciones geométricas, como rotación, traslación, recorte, cambio de tamaño y zoom.
  - **Área Principal:** Donde se muestran las imágenes (imagen 1 y, opcionalmente, imagen 2).

---

## Funcionalidades Clave y Fragmentos de Código ⌨️

### 1. Inicialización y Configuración de la Ventana

La clase `ImageViewer` se inicializa estableciendo el modo de apariencia y el tamaño de la ventana, y creando las principales zonas de la interfaz:

```python
class ImageViewer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Visor de Imágenes - PrimPy")
        self.geometry("1000x600")
        # Configuración de frames: topbar, sidebars y área principal...
```

### 2. Carga y Visualización de Imágenes

El método `load_image()` permite seleccionar y cargar imágenes. Si es la primera imagen, se almacena en `self.image` y se guarda una copia original. Si ya hay una imagen cargada, la nueva se carga en `self.second_image`.

```python
def load_image(self):
    file_path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")])
    if not file_path:
        return
    if self.image is None:
        self.reset_ui()
        self.image = cv2.imread(file_path)
        self.image_original = self.image.copy()
        self.tipo_combo.set("Original")
        self.on_tipo_change("Original")
    elif self.second_image is None:
        self.second_image = cv2.imread(file_path)
        self.second_image_original = self.second_image.copy()
    self.display_image()
```

### 3. Transformaciones Geométricas y Ajuste de Parámetros

Se dispone de métodos para aplicar transformaciones en tiempo real, como:
- **Rotación:**  
  Actualiza el ángulo mediante un slider y rota la imagen con `pi.rotar`.
  
  ```python
  def on_rot_slider_change(self, value):
      if self.image is None:
          return
      angle = int(value)
      rotated = pi.rotar(self.image.copy(), angle)
      self.rot_label.configure(text=f"Rotación: {value:.2f}°")
      self.current_image = rotated
      self.display_image()
  ```
  
- **Ajuste de Brillo y Contraste:**  
  Se ajustan mediante sliders y se actualiza la imagen en tiempo real.
  
  ```python
  def on_brillo_slider_change(self, value):
      if self.typed_image is None:
          return
      brillo_normalizado = float(value) / 100.0
      self.brillo_label.configure(text=f"Brillo: {brillo_normalizado:.2f}")
      temp = pi.ajustarBrillo(self.typed_image.copy(), brillo_normalizado)
      temp = (temp * 255).clip(0, 255).astype(np.uint8)
      self.current_image = temp
      self.display_image()
  ```
  
### 4. Fusión de Imágenes

El método `apply_fusion()` valida la existencia de dos imágenes y las combina usando un factor de transparencia definido por un slider:

```python
def apply_fusion(self):
    if self.image is None or self.second_image is None:
        mb.showwarning("Advertencia", "Debe cargar la segunda imagen para realizar la fusión.")
        return
    if self.image.shape != self.second_image.shape:
        mb.showwarning("Advertencia", "Las imágenes deben tener el mismo tamaño para fusionarse.")
        return
    alpha = self.fusion_slider.get()
    fused = pi.fusionarImagenesConEq(self.image, self.second_image, alpha)
    if fused is not None:
        fused_bgr = (fused * 255).astype(np.uint8)
        self.current_image = fused_bgr
        self.second_image = None
        self.display_image()
```

---

## Requisitos e Instalación 🔧

### Requisitos
- **Python 3.x**
- **Tkinter y CustomTkinter:** Para la interfaz gráfica.
- **OpenCV (cv2), PIL (Pillow) y NumPy:** Para el procesamiento de imágenes.
- **Módulo `procesamientoImagenes`:** Incluido en el proyecto (ver instrucciones de uso).

### Instalación
1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu_usuario/ImageViewer.git
    ```
2. Instala las dependencias:
    ```bash
    pip install opencv-python pillow numpy customtkinter
    ```
3. Ejecuta el visor:
    ```bash
    python visor.py
    ```

---

## Uso 📂

Una vez lanzado el programa, podrás:
- **Cargar una imagen:** Usa el botón "Cargar Imagen" para seleccionar tu imagen favorita.
- **Aplicar transformaciones:** Usa los sliders y entradas de la barra lateral para modificar brillo, contraste, rotación, etc.
- **Fusionar imágenes:** Carga una segunda imagen y ajusta el slider de transparencia para ver el efecto de fusión.
- **Guardar cambios:** Guarda la imagen resultante con el botón "Guardar Imagen".

---

## Autores 👨‍💻👨‍💻

Este proyecto ha sido desarrollado con mucho entusiasmo por:
- **Juan Pablo Sánchez**
- **Kevin Esguerra**

¡Gracias por leer y esperamos que disfrutes usando ImageViewer! 🚀
