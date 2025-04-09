from PrimPy import procesamientoImagenes as pi
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import tkinter.messagebox as mb

# Configuración global de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ImageViewer(ctk.CTk):
    """
    Clase principal para el visor de imágenes utilizando CustomTkinter.
    
    Esta clase implementa funcionalidades de:
      - Cargar y mostrar imágenes (hasta dos)
      - Guardar, restaurar y eliminar imágenes
      - Aplicar transformaciones básicas (rotación, traslación, recorte, cambiar tamaño, zoom)
      - Ajustar parámetros de procesamiento (brillo, contraste, tipo de visualización, canales)
      - Fusionar dos imágenes mediante un factor de transparencia

    Se hace uso de funciones definidas en el módulo "procesamientoImagenes" (pi).
    """
    def __init__(self):
        """
        Inicializa la ventana principal y todos los widgets (botones, entradas, sliders, etc.).
        Configura la estructura de la interfaz en topbar, sidebars y área principal.
        """
        super().__init__()
        self.title("Visor de Imágenes - PrimPy")
        self.geometry("1000x600")

        # Variables para almacenar imágenes:
        self.image = None                # Imagen principal cargada
        self.second_image = None         # Segunda imagen cargada para fusión
        self.current_image = None        # Imagen actualmente mostrada (resultado de transformaciones)
        self.img_label = None
        self.image_original = None       # Copia original de la primera imagen
        self.second_image_original = None  # Copia original de la segunda imagen
        self.typed_image = None          # Imagen procesada según tipo seleccionado (original, gris, negativo, binaria)
        self.channel_image = None        # Imagen obtenida tras aplicar la selección de canales

        # FRAME: Topbar para botones principales (cargar, guardar, restaurar, eliminar)
        self.topbar = ctk.CTkFrame(self, height=50)
        self.topbar.pack(side="top", fill="x")

        self.load_btn = ctk.CTkButton(self.topbar, text="Cargar Imagen", command=self.load_image)
        self.load_btn.pack(side="left", padx=10)

        self.save_btn = ctk.CTkButton(self.topbar, text="Guardar Imagen", command=self.save_image)
        self.save_btn.pack(side="left", padx=10)

        self.restore_btn = ctk.CTkButton(self.topbar, text="Restaurar", command=self.restore_image)
        self.restore_btn.pack(side="left", padx=10)

        self.remove_btn = ctk.CTkButton(self.topbar, text="Eliminar Imagen", command=self.remove_image)
        self.remove_btn.pack(side="left", padx=10)

        # SIDEBAR IZQUIERDA: Contiene controles de procesamiento y fusión de imágenes
        self.sidebar = ctk.CTkScrollableFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        # ÁREA PRINCIPAL: Se divide en dos frames para mostrar la imagen 1 y la imagen 2 (si es que hay)
        self.main_area = ctk.CTkFrame(self)
        self.main_area.pack(side="left", fill="both", expand=True)

        self.left_image_frame = ctk.CTkFrame(self.main_area)
        self.left_image_frame.pack(side="left", expand=True, fill="both")

        self.right_image_frame = ctk.CTkFrame(self.main_area)
        self.right_image_frame.pack(side="left", expand=True, fill="both")

        self.image_panel = ctk.CTkLabel(self.left_image_frame, text="Aquí se mostrará la imagen 1")
        self.image_panel.pack(side="top", anchor="center", expand=True)
        self.size_label = ctk.CTkLabel(self.left_image_frame, text="")
        self.size_label.pack(side="top", anchor="center")

        self.image_panel2 = ctk.CTkLabel(self.right_image_frame, text="Aquí se mostrará la imagen 2")
        self.image_panel2.pack(side="top", anchor="center", expand=True)
        self.size_label2 = ctk.CTkLabel(self.right_image_frame, text="")
        self.size_label2.pack(side="top", anchor="center")

        # SIDEBAR DERECHA: Barra lateral de transformaciones (rotación, traslación, recorte, cambiar tamaño, zoom)
        self.transformation_sidebar = ctk.CTkScrollableFrame(self, width=200)
        self.transformation_sidebar.pack(side="right", fill="y", padx=10, pady=10)

        # Inicializamos elementos en la sidebar izquierda (controles de imagen, fusión y ajustes)
        self.init_sidebar()

        # Inicializamos elementos en la barra de transformaciones (derecha)
        self.create_transform_sidebar()

    def init_sidebar(self):
        """
        Inicializa la barra lateral izquierda con controles generales y de fusión:
          - Visualización del histograma
          - Ajuste de brillo y contraste
          - Selección de zonas (claras u oscuras)
          - Selección del tipo de imagen (Original, Escala de Grises, Negativo, Binarizada)
          - Checkboxes de canales RGB y CMY (solo uno puede estar activo a la vez)
          - Controles de fusión (slider de transparencia y botón de fusionar)
        """
        title = ctk.CTkLabel(self.sidebar, text="PrimPy Visor", font=ctk.CTkFont(size=18, weight="bold"), text_color="#00aaff")
        title.pack(pady=10)

        hist_btn = ctk.CTkButton(self.sidebar, text="Ver Histograma", command=self.see_histogram)
        hist_btn.pack(pady=5)

        # Sliders de brillo y contraste
        self.brillo_slider, self.brillo_label = self.add_slider("Brillo", -100, 100)
        self.brillo_slider.configure(command=self.on_brillo_slider_change)
        self.contraste_slider, self.contraste_label = self.add_slider("Contraste", 0.01, 3)
        self.contraste_slider.configure(number_of_steps=299, command=self.on_contraste_slider_change)
        self.contraste_slider.set(0.1)

        # Opciones de zonas claras/oscuras
        zonas_frame = ctk.CTkFrame(self.sidebar)
        zonas_label = ctk.CTkLabel(zonas_frame, text="Zonas:")
        zonas_label.pack(anchor="w")
        self.zona_var = tk.StringVar(value="clara")
        ctk.CTkRadioButton(zonas_frame, text="Zonas Claras", variable=self.zona_var, value="clara", command=self.on_zone_change).pack(anchor="w")
        ctk.CTkRadioButton(zonas_frame, text="Zonas Oscuras", variable=self.zona_var, value="oscura", command=self.on_zone_change).pack(anchor="w")
        zonas_frame.pack(pady=5)

        # Selección del tipo de imagen
        ctk.CTkLabel(self.sidebar, text="Tipo:").pack(anchor="w")
        self.tipo_combo = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Original", "Escala de Grises", "Negativo", "Binarizada"]
        )
        self.tipo_combo.configure(command=self.on_tipo_change)
        self.tipo_combo.pack(pady=5)

        # Checkboxes para canales RGB (mutuamente exclusivos)
        ctk.CTkLabel(self.sidebar, text="Canales RGB:").pack(anchor="w")
        self.rgb_checks = {}
        for color in ["Red", "Green", "Blue"]:
            var = tk.BooleanVar()
            cb = ctk.CTkCheckBox(self.sidebar, text=color, variable=var, command=self.on_channel_check)
            cb.pack(anchor="w")
            self.rgb_checks[color] = var

        # Checkboxes para canales CMY (mutuamente exclusivos)
        ctk.CTkLabel(self.sidebar, text="Canales CMY:").pack(anchor="w")
        self.cmy_checks = {}
        for color in ["Cyan", "Magenta", "Yellow"]:
            var = tk.BooleanVar()
            cb = ctk.CTkCheckBox(self.sidebar, text=color, variable=var, command=self.on_channel_check)
            cb.pack(anchor="w")
            self.cmy_checks[color] = var

        # Panel de fusión de imágenes
        ctk.CTkLabel(self.sidebar, text="Fusionar Imágenes:").pack(pady=(10, 0))
        ctk.CTkLabel(self.sidebar, text="Transparencia").pack(anchor="w")
        self.fusion_slider = ctk.CTkSlider(self.sidebar, from_=0, to=1)
        self.fusion_slider.set(0.5)
        self.fusion_slider.pack(pady=5)
        fusion_btn = ctk.CTkButton(self.sidebar, text="Fusionar", command=self.apply_fusion)
        fusion_btn.pack(pady=5)

    def create_transform_sidebar(self):
        """
        Inicializa la barra lateral derecha con controles para transformaciones:
          - Rotación: slider de -360° a 360° con etiqueta que muestra el valor actual.
          - Traslación: entradas para dx y dy y botón "Trasladar".
          - Recorte: entradas para coordenadas de recorte y botón "Recortar".
          - Cambio de tamaño: entradas para ancho y alto y botón "Cambiar tamaño".
          - Zoom: entradas para coordenadas del centro y slider (con etiqueta) para el factor de zoom,
                   y botón "Aplicar Zoom".
        """
        # Rotación
        self.rot_label = ctk.CTkLabel(self.transformation_sidebar, text="Rotación: 0.00°")
        self.rot_label.pack()
        self.rot_slider = ctk.CTkSlider(self.transformation_sidebar, from_=-360, to=360, number_of_steps=720)
        self.rot_slider.pack(pady=5)
        self.rot_slider.configure(command=self.on_rot_slider_change)
        
        # Traslación
        ctk.CTkLabel(self.transformation_sidebar, text="Trasladar dx, dy:").pack()
        self.dx_entry = ctk.CTkEntry(self.transformation_sidebar, placeholder_text="dx")
        self.dy_entry = ctk.CTkEntry(self.transformation_sidebar, placeholder_text="dy")
        self.dx_entry.pack()
        self.dy_entry.pack()
        translate_btn = ctk.CTkButton(self.transformation_sidebar, text="Trasladar", command=self.apply_translation)
        translate_btn.pack(pady=5)
        
        # Recorte
        ctk.CTkLabel(self.transformation_sidebar, text="Recortar (x1,y1)-(x2,y2):").pack()
        self.x1_entry = ctk.CTkEntry(self.transformation_sidebar, placeholder_text="x1")
        self.y1_entry = ctk.CTkEntry(self.transformation_sidebar, placeholder_text="y1")
        self.x2_entry = ctk.CTkEntry(self.transformation_sidebar, placeholder_text="x2")
        self.y2_entry = ctk.CTkEntry(self.transformation_sidebar, placeholder_text="y2")
        self.x1_entry.pack()
        self.y1_entry.pack()
        self.x2_entry.pack()
        self.y2_entry.pack()
        recortar_btn = ctk.CTkButton(self.transformation_sidebar, text="Recortar", command=self.recortar)
        recortar_btn.pack(pady=5)
        
        # Cambio de tamaño
        ctk.CTkLabel(self.transformation_sidebar, text="Cambiar Tamaño (ancho x alto):").pack(pady=(10, 0))
        self.width_entry = ctk.CTkEntry(self.transformation_sidebar, placeholder_text="Ancho")
        self.height_entry = ctk.CTkEntry(self.transformation_sidebar, placeholder_text="Alto")
        self.width_entry.pack()
        self.height_entry.pack()
        resize_btn = ctk.CTkButton(self.transformation_sidebar, text="Cambiar tamaño", command=self.apply_resize)
        resize_btn.pack(pady=5)
        
        # Zoom
        ctk.CTkLabel(self.transformation_sidebar, text="Zoom:").pack()
        self.zoom_x_entry = ctk.CTkEntry(self.transformation_sidebar, placeholder_text="x")
        self.zoom_y_entry = ctk.CTkEntry(self.transformation_sidebar, placeholder_text="y")
        self.zoom_x_entry.pack()
        self.zoom_y_entry.pack()
        self.zoom_label = ctk.CTkLabel(self.transformation_sidebar, text="Factor de Zoom: 1.00")
        self.zoom_label.pack()
        # El slider de zoom va de 0.1 a 5, y se actualiza en tiempo real con su valor
        self.zoom_slider = ctk.CTkSlider(self.transformation_sidebar, from_=0.1, to=5, number_of_steps=200, command=self.update_zoom_label)
        self.zoom_slider.set(1.0)
        self.zoom_slider.pack(pady=5)
        zoom_btn = ctk.CTkButton(self.transformation_sidebar, text="Aplicar Zoom", command=self.apply_zoom)
        zoom_btn.pack(pady=5)

    def add_slider(self, label, minval, maxval):
        """
        Crea un slider con una etiqueta asociada.

        Parámetros:
            label (str): Texto para la etiqueta.
            minval (float): Valor mínimo del slider.
            maxval (float): Valor máximo del slider.
        Retorna:
            (slider, label_widget): Tupla con el widget slider y su etiqueta.
        """
        label_widget = ctk.CTkLabel(self.sidebar, text=f"{label}: 0.00")
        label_widget.pack(anchor="w")
        slider = ctk.CTkSlider(self.sidebar, from_=minval, to=maxval, number_of_steps=maxval - minval)
        slider.pack(pady=5)
        return slider, label_widget

    def load_image(self):
        """
        Abre un diálogo para seleccionar una imagen y la carga.
        Si no hay imagen cargada, se establece como imagen principal;
        de lo contrario, se carga como segunda imagen para tareas de fusión.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")])
        if not file_path:
            return

        if self.image is None:
            # Cargar la primera imagen
            self.reset_ui()
            self.image = cv2.imread(file_path)
            self.image_original = self.image.copy()
            self.tipo_combo.set("Original")  # Selección visual del tipo original
            self.on_tipo_change("Original")   # Aplica la conversión a typed_image
        elif self.second_image is None:
            # Cargar la segunda imagen
            self.second_image = cv2.imread(file_path)
            self.second_image_original = self.second_image.copy()

        self.display_image()

    def save_image(self):
        """
        Muestra un diálogo para guardar la imagen actualmente mostrada.
        """
        if self.current_image is None:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", '*.png'), ("JPEG Image", '*.jpg'), ("All Files", '*.*')]
        )
        if file_path:
            cv2.imwrite(file_path, self.current_image)

    def display_image(self):
        """
        Actualiza y muestra la imagen en los paneles correspondientes.
        Muestra la imagen principal en el panel izquierdo y, si existe,
        la segunda imagen en el panel derecho.
        """
        if self.current_image is not None:
            img_rgb = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_pil.thumbnail((400, 300))
            imgtk = ImageTk.PhotoImage(img_pil)
            self.image_panel.configure(image=imgtk, text="")
            self.image_panel.image = imgtk
            h, w = self.current_image.shape[:2]
            self.size_label.configure(text=f"Tamaño Primera: {w} x {h}")

        if self.second_image is not None:
            second_rgb = cv2.cvtColor(self.second_image, cv2.COLOR_BGR2RGB)
            second_pil = Image.fromarray(second_rgb)
            second_pil.thumbnail((400, 300))
            imgtk2 = ImageTk.PhotoImage(second_pil)
            self.image_panel2.configure(image=imgtk2, text="")
            self.image_panel2.image = imgtk2
            h2, w2 = self.second_image.shape[:2]
            self.size_label2.configure(text=f"Tamaño Segunda: {w2} x {h2}")
        else:
            # Si no existe la segunda imagen, se muestra un mensaje predeterminado.
            self.image_panel2.configure(image="", text="Aquí se mostrará la imagen 2")
            self.size_label2.configure(text="")

    def apply_changes(self):
        """
        Aplica los cambios globales de brillo y contraste usando cv2.convertScaleAbs
        sobre la imagen original (sin tipo) y actualiza la visualización.
        """
        if self.image is None:
            return

        modified = self.image.copy()

        brillo = self.brillo_slider.get()       # Valor en el rango -100 a 100
        contraste = self.contraste_slider.get()   # Valor en el rango definido

        alpha = 1 + (contraste / 100.0)  # Factor para el contraste
        beta = brillo                  # Valor de desplazamiento para el brillo

        modified = cv2.convertScaleAbs(modified, alpha=alpha, beta=beta)
        self.current_image = modified
        self.display_image()

    def apply_translation(self):
        """
        Lee las coordenadas ingresadas (dx, dy) y traslada la imagen
        usando la función 'trasladar' de procesamientoImagenes.
        """
        if self.image is None:
            return
        try:
            x = int(self.dx_entry.get())
            y = int(self.dy_entry.get())
        except ValueError:
            mb.showerror("Error", "Las coordenadas deben ser valores enteros.")
            return
        translated = pi.trasladar(self.image, (x, y))
        self.current_image = translated
        self.display_image()

    def recortar(self):
        """
        Recorta la imagen según las coordenadas ingresadas (x1, x2, y1, y2)
        utilizando la función 'recortar' de procesamientoImagenes.
        """
        if self.image is None:
            return
        try:
            x1 = int(self.x1_entry.get())
            x2 = int(self.x2_entry.get())
            y1 = int(self.y1_entry.get())
            y2 = int(self.y2_entry.get())
        except ValueError:
            mb.showerror("Error", "Todas las coordenadas deben ser enteros.")
            return
        cropped = pi.recortar(self.image, (x1, x2), (y1, y2))
        self.current_image = cropped
        self.display_image()

    def apply_resize(self):
        """
        Lee el ancho y alto ingresados y cambia el tamaño de la imagen
        utilizando la función 'cambiarTamaño' de procesamientoImagenes.
        Se actualiza tanto 'image' como 'current_image' para mantener consistencia.
        """
        if self.current_image is None:
            return

        try:
            new_width = int(self.width_entry.get())
            new_height = int(self.height_entry.get())
        except ValueError:
            mb.showerror("Error", "Debe ingresar números válidos para el tamaño.")
            return

        resized = pi.cambiarTamaño(self.image, (new_width, new_height))
        self.image = resized
        self.current_image = resized
        self.display_image()

    def apply_zoom(self):
        """
        Aplica zoom a la imagen usando las coordenadas y el factor seleccionado.
        El factor de zoom se obtiene del slider y las coordenadas (x, y) se leen
        de las entradas correspondientes. Se utiliza la función 'zoom' de procesamientoImagenes.
        """
        if self.image is None:
            mb.showerror("Error", "Debe cargar una imagen antes de aplicar zoom.")
            return

        try:
            x = int(self.zoom_x_entry.get())
            y = int(self.zoom_y_entry.get())
            alpha = float(self.zoom_slider.get())
        except ValueError:
            mb.showerror("Error", "Ingrese coordenadas válidas y asegúrese de mover el slider de zoom.")
            return

        if alpha <= 0 or alpha > 100:
            mb.showerror("Error", "El factor de zoom debe estar entre 0 y 100.")
            return

        try:
            zoomed = pi.zoom(self.image.copy(), alpha, (x, y))
            zoomed_bgr = (zoomed * 255).astype(np.uint8)
            self.current_image = zoomed_bgr
            self.display_image()
        except Exception as e:
            mb.showerror("Error", f"Ocurrió un error al aplicar zoom:\n{str(e)}")

    def update_zoom_label(self, value):
        """
        Actualiza la etiqueta que muestra el valor actual del factor de zoom.
        
        Parámetro:
            value (float): Valor actual del slider de zoom.
        """
        self.zoom_label.configure(text=f"Factor de Zoom: {float(value):.2f}")

    def apply_fusion(self):
        """
        Fusiona la imagen principal con la segunda imagen usando un factor de transparencia.
        Se validan los casos en que no hay segunda imagen o las imágenes tienen tamaños distintos.
        Utiliza la función 'fusionarImagenesConEq' de procesamientoImagenes.
        """
        if self.image is None:
            return
        if self.second_image is None:
            mb.showwarning("Advertencia", "Debe cargar una segunda imagen para realizar la fusión.")
            return
        if self.image.shape != self.second_image.shape:
            mb.showwarning("Advertencia", "Las imágenes deben tener el mismo tamaño para fusionarse.")
            return
        alpha = self.fusion_slider.get()
        if alpha <= 0:
            mb.showwarning("Advertencia", "El valor de transparencia debe ser mayor que 0.")
            return
        fused = pi.fusionarImagenesConEq(self.image, self.second_image, alpha)
        if fused is not None:
            fused_bgr = (fused * 255).astype(np.uint8)
            self.current_image = fused_bgr
            self.second_image = None
            self.display_image()

    def reset_ui(self):
        """
        Restaura la interfaz de usuario a su estado inicial:
          - Reinicia los sliders de brillo, contraste, rotación y zoom.
          - Restaura la opción de tipo de imagen a "Original".
          - Desmarca todas las selecciones de canales.
          - Limpia las entradas de texto.
        """
        self.brillo_slider.set(0)
        self.brillo_label.configure(text="Brillo: 0.00")
        self.contraste_slider.set(0.1)
        self.contraste_label.configure(text="Contraste: 0.10")
        self.tipo_combo.set("Original")
        self.zona_var.set("clara")
        for color_var in self.rgb_checks.values():
            color_var.set(False)
        for color_var in self.cmy_checks.values():
            color_var.set(False)
        self.rot_slider.set(0)
        self.zoom_slider.set(1)
        self.fusion_slider.set(0.5)
        # Limpia las entradas de texto, preservando los placeholders
        for entry in [self.dx_entry, self.dy_entry, self.x1_entry, self.y1_entry, self.x2_entry, self.y2_entry, self.width_entry, self.height_entry, self.zoom_x_entry, self.zoom_y_entry]:
            entry.delete(0, 'end')

    def restore_image(self):
        """
        Restaura la imagen original (y la segunda imagen si corresponde) y actualiza la visualización.
        También se reinicia la interfaz a su estado inicial.
        """
        self.reset_ui()
        if self.image_original is not None:
            self.image = self.image_original.copy()
            self.current_image = self.image.copy()
        if self.second_image_original is not None:
            self.second_image = self.second_image_original.copy()
        self.display_image()

    def remove_image(self):
        """
        Elimina la imagen actual y limpia el panel de visualización.
        Reinicia la interfaz a su estado inicial.
        """
        self.image = None
        self.second_image = None
        self.current_image = None
        self.image_panel.configure(image="", text="Aquí se mostrará la imagen 1")
        self.size_label.configure(text="")
        self.image_panel2.configure(image="", text="Aquí se mostrará la imagen 2")
        self.size_label2.configure(text="")
        self.reset_ui()

    def see_histogram(self):
        """
        Muestra el histograma de la imagen principal utilizando la función 'histograma'
        del módulo procesamientoImagenes. Se valida que la imagen esté cargada.
        """
        if self.image is None:
            mb.showwarning("Advertencia", "Debe cargar la imagen 1 para ver su histograma.")
            return
        img_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        pi.histograma(img_rgb)

    def on_brillo_slider_change(self, value):
        """
        Ajusta el brillo en tiempo real de 'typed_image' usando el valor del slider.
        Se utiliza la función 'ajustarBrillo' de procesamientoImagenes y actualiza 'current_image'.
        
        Parámetro:
            value (float): Valor del slider de brillo.
        """
        if self.typed_image is None:
            return
        brillo_normalizado = float(value) / 100.0
        self.brillo_label.configure(text=f"Brillo: {brillo_normalizado:.2f}")
        temp = pi.ajustarBrillo(self.typed_image.copy(), brillo_normalizado)
        temp = (temp * 255).clip(0, 255).astype(np.uint8)
        self.current_image = temp
        self.display_image()

    def on_zone_change(self):
        """
        Se ejecuta al cambiar la selección de zona (claras u oscuras),
        y se vuelve a aplicar el contraste usando el valor actual del slider.
        """
        if self.image_original is None:
            return
        self.on_contraste_slider_change(self.contraste_slider.get())

    def on_contraste_slider_change(self, value):
        """
        Ajusta el contraste en tiempo real de 'typed_image' usando el valor del slider.
        Se utiliza la función 'contrastarZonasOscuras' o 'contrastarZonasClaras'
        de procesamientoImagenes, dependiendo de la zona seleccionada.
        
        Parámetro:
            value (float): Valor del slider de contraste.
        """
        if self.typed_image is None:
            return
        factor = float(value)
        self.contraste_label.configure(text=f"Contraste: {factor:.2f}")
        zona = self.zona_var.get()
        if zona == "oscura":
            temp = pi.contrastarZonasOscuras(self.typed_image.copy(), factor)
        else:
            temp = pi.contrastarZonasClaras(self.typed_image.copy(), factor)
        temp = (temp * 255).clip(0, 255).astype(np.uint8)
        self.current_image = temp
        self.display_image()

    def on_tipo_change(self, choice):
        """
        Cambia el tipo de visualización de la imagen (Original, Escala de Grises, Negativo o Binarizada).
        Restablece el brillo y contraste a sus valores iniciales y actualiza 'typed_image' y 'current_image'.

        Parámetro:
            choice (str): Tipo seleccionado en el menú.
        """
        self.brillo_slider.set(0)
        self.brillo_label.configure(text="Brillo: 0.00")
        self.contraste_slider.set(0.1)
        self.contraste_label.configure(text="Contraste: 0.10")
        if self.image_original is None:
            return
        typed_image = self.image_original.copy()
        if choice == "Escala de Grises":
            temp = pi.grisesConAverage(typed_image)
            temp = (temp * 255).clip(0, 255).astype(np.uint8)
            typed_image = cv2.cvtColor(temp, cv2.COLOR_GRAY2BGR)
        elif choice == "Negativo":
            temp = pi.negativa(typed_image)
            typed_image = (temp * 255).clip(0, 255).astype(np.uint8)
        elif choice == "Binarizada":
            temp = pi.binarizar(typed_image, 0.5)
            temp = (temp * 255).astype(np.uint8)
            typed_image = cv2.cvtColor(temp, cv2.COLOR_GRAY2BGR)
        self.typed_image = typed_image
        if choice == "Original":
            self.typed_image = self.image_original.copy()
        self.current_image = self.typed_image
        self.display_image()

    def on_channel_check(self):
        """
        Permite la selección exclusiva de canales RGB o CMY.
        Si se selecciona más de un canal, solo se mantiene el más reciente.
        Actualiza 'current_image' mostrando únicamente la(s) capa(s) seleccionada(s).
        Si no hay ninguna seleccionada, se restaura 'typed_image'.
        """
        all_checks = {**self.rgb_checks, **self.cmy_checks}
        checked = [color for color, var in all_checks.items() if var.get()]
        if len(checked) > 1:
            # Mantiene solo el último chequeado, desmarcando los anteriores.
            newly_checked = checked[-1]
            for color in checked[:-1]:
                all_checks[color].set(False)
        if self.typed_image is None:
            return
        if not any(var.get() for var in all_checks.values()):
            self.current_image = self.typed_image.copy()
            self.display_image()
            return
        float_img = self.typed_image.astype(np.float32)
        combined = np.zeros_like(float_img)
        if self.rgb_checks["Red"].get():
            combined += pi.extraerCapaRoja(float_img.copy())
        if self.rgb_checks["Green"].get():
            combined += pi.extraerCapaVerde(float_img.copy())
        if self.rgb_checks["Blue"].get():
            combined += pi.extraerCapaAzul(float_img.copy())
        if self.cmy_checks["Cyan"].get():
            combined += pi.extraerCapaCian(float_img.copy())
        if self.cmy_checks["Magenta"].get():
            combined += pi.extraerCapaMagenta(float_img.copy())
        if self.cmy_checks["Yellow"].get():
            combined += pi.extraerCapaAmarilla(float_img.copy())
        combined = np.clip(combined, 0, 1)
        self.current_image = (combined * 255).astype(np.uint8)
        self.display_image()

    def on_rot_slider_change(self, value):
        """
        Aplica rotación a la imagen principal usando el valor del slider de rotación.
        Actualiza la etiqueta de rotación y muestra la imagen rotada.
        
        Parámetro:
            value (float): Ángulo en grados obtenido del slider.
        """
        if self.image is None:
            return
        angle = int(value)
        rotated = pi.rotar(self.image.copy(), angle)
        self.rot_label.configure(text=f"Rotación: {value:.2f}°")
        self.current_image = rotated
        self.display_image()

if __name__ == '__main__':
    app = ImageViewer()
    app.mainloop()
