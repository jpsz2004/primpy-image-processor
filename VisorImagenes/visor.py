from PrimPy import procesamientoImagenes as pi
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import tkinter.messagebox as mb

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ImageViewer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Visor de Imágenes - PrimPy")
        self.geometry("1000x600")

        self.image = None
        self.second_image = None
        self.current_image = None
        self.img_label = None
        self.image_original = None
        self.second_image_original = None
        self.typed_image = None
        self.channel_image = None       # Imagen con canales seleccionados

        # Frame superior para botones principales
        self.topbar = ctk.CTkFrame(self, height=50)
        self.topbar.pack(side="top", fill="x")

        # Botón para cargar imagen en el topbar
        self.load_btn = ctk.CTkButton(self.topbar, text="Cargar Imagen", command=self.load_image)
        self.load_btn.pack(side="left", padx=10)

        # Botón para guardar imagen en el topbar
        self.save_btn = ctk.CTkButton(self.topbar, text="Guardar Imagen", command=self.save_image)
        self.save_btn.pack(side="left", padx=10)

        # Botón para restaurar imagen original
        self.restore_btn = ctk.CTkButton(self.topbar, text="Restaurar", command=self.restore_image) 
        self.restore_btn.pack(side="left", padx=10)

        # Botón para eliminar imagen
        self.remove_btn = ctk.CTkButton(self.topbar, text="Eliminar Imagen", command=self.remove_image)
        self.remove_btn.pack(side="left", padx=10)

        # Sidebar izquierda
        self.sidebar = ctk.CTkScrollableFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        # Área principal
        self.main_area = ctk.CTkFrame(self)
        self.main_area.pack(side="left", fill="both", expand=True)

        # Creamos dos frames para las imágenes
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

        # Barra lateral derecha de transformaciones
        self.transformation_sidebar = ctk.CTkScrollableFrame(self, width=200)
        self.transformation_sidebar.pack(side="right", fill="y", padx=10, pady=10)

        # Inicializamos los elementos de la barra lateral izquierda
        self.init_sidebar()

        # Inicializamos los elementos de la barra de transformaciones (derecha)
        self.create_transform_sidebar()

    def init_sidebar(self):
        title = ctk.CTkLabel(self.sidebar, text="PrimPy Visor", font=ctk.CTkFont(size=18, weight="bold"), text_color="#00aaff")
        title.pack(pady=10)

        hist_btn = ctk.CTkButton(self.sidebar, text="Ver Histograma", command=self.see_histogram)
        hist_btn.pack(pady=5)

        # Brillo y Contraste
        self.brillo_slider, self.brillo_label = self.add_slider("Brillo", -100, 100)
        self.brillo_slider.configure(command=self.on_brillo_slider_change)
        self.contraste_slider, self.contraste_label = self.add_slider("Contraste", 0.01, 3)
        self.contraste_slider.configure(number_of_steps=299, command=self.on_contraste_slider_change)
        self.contraste_slider.set(0.1)

        # Zonas claras/oscuras
        zonas_frame = ctk.CTkFrame(self.sidebar)
        zonas_label = ctk.CTkLabel(zonas_frame, text="Zonas:")
        zonas_label.pack(anchor="w")
        self.zona_var = tk.StringVar(value="clara")
        ctk.CTkRadioButton(zonas_frame, text="Zonas Claras", variable=self.zona_var, value="clara", command=self.on_zone_change).pack(anchor="w")
        ctk.CTkRadioButton(zonas_frame, text="Zonas Oscuras", variable=self.zona_var, value="oscura", command=self.on_zone_change).pack(anchor="w")
        zonas_frame.pack(pady=5)

        # Tipo (agregamos "Binarizada" al listado)
        ctk.CTkLabel(self.sidebar, text="Tipo:").pack(anchor="w")
        self.tipo_combo = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Original", "Escala de Grises", "Negativo", "Binarizada"]
        )
        self.tipo_combo.configure(command=self.on_tipo_change)
        self.tipo_combo.pack(pady=5)

        # Canales RGB
        ctk.CTkLabel(self.sidebar, text="Canales RGB:").pack(anchor="w")
        self.rgb_checks = {}
        for color in ["Red", "Green", "Blue"]:
            var = tk.BooleanVar()
            cb = ctk.CTkCheckBox(self.sidebar, text=color, variable=var, command=self.on_channel_check)
            cb.pack(anchor="w")
            self.rgb_checks[color] = var

        # Canales CMY
        ctk.CTkLabel(self.sidebar, text="Canales CMY:").pack(anchor="w")
        self.cmy_checks = {}
        for color in ["Cyan", "Magenta", "Yellow"]:
            var = tk.BooleanVar()
            cb = ctk.CTkCheckBox(self.sidebar, text=color, variable=var, command=self.on_channel_check)
            cb.pack(anchor="w")
            self.cmy_checks[color] = var

        # Fusion panel moved here
        ctk.CTkLabel(self.sidebar, text="Fusionar Imágenes:").pack(pady=(10,0))
        ctk.CTkLabel(self.sidebar, text="Transparencia").pack(anchor="w")
        self.fusion_slider = ctk.CTkSlider(self.sidebar, from_=0, to=1)
        self.fusion_slider.set(0.5)
        self.fusion_slider.pack(pady=5)
        fusion_btn = ctk.CTkButton(self.sidebar, text="Fusionar", command=self.apply_fusion)
        fusion_btn.pack(pady=5)

    def create_transform_sidebar(self):
        # Etiqueta y slider para rotación
        ctk.CTkLabel(self.transformation_sidebar, text="Rotar (°):").pack()
        self.rot_slider = ctk.CTkSlider(self.transformation_sidebar, from_=-360, to=360, number_of_steps=720)
        self.rot_slider.pack(pady=5)

        # Traslación
        ctk.CTkLabel(self.transformation_sidebar, text="Trasladar dx, dy:").pack()
        self.dx_entry = ctk.CTkEntry(self.transformation_sidebar, placeholder_text="dx")
        self.dy_entry = ctk.CTkEntry(self.transformation_sidebar, placeholder_text="dy")
        self.dx_entry.pack()
        self.dy_entry.pack()

        translate_btn = ctk.CTkButton(self.transformation_sidebar, text="Trasladar", command=self.apply_translation)
        translate_btn.pack(pady=5)

        # Recortar
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

        # Sección para cambiar tamaño
        ctk.CTkLabel(self.transformation_sidebar, text="Cambiar Tamaño (ancho x alto):").pack(pady=(10,0))
        self.width_entry = ctk.CTkEntry(self.transformation_sidebar, placeholder_text="Ancho")
        self.height_entry = ctk.CTkEntry(self.transformation_sidebar, placeholder_text="Alto")
        self.width_entry.pack()
        self.height_entry.pack()

        resize_btn = ctk.CTkButton(self.transformation_sidebar, text="Cambiar tamaño", command=self.apply_resize)
        resize_btn.pack(pady=5)

        # Zoom panel
        ctk.CTkLabel(self.transformation_sidebar, text="Zoom:").pack()
        self.zoom_x_entry = ctk.CTkEntry(self.transformation_sidebar, placeholder_text="x")
        self.zoom_y_entry = ctk.CTkEntry(self.transformation_sidebar, placeholder_text="y")
        self.zoom_x_entry.pack()
        self.zoom_y_entry.pack()
        self.zoom_slider = ctk.CTkSlider(self.transformation_sidebar, from_=0, to=2)
        self.zoom_slider.pack(pady=5)
        zoom_btn = ctk.CTkButton(self.transformation_sidebar, text="Aplicar Zoom", command=self.apply_zoom)
        zoom_btn.pack(pady=5)

    def add_slider(self, label, minval, maxval):
        label_widget = ctk.CTkLabel(self.sidebar, text=f"{label}: 0.00")
        label_widget.pack(anchor="w")
        slider = ctk.CTkSlider(self.sidebar, from_=minval, to=maxval, number_of_steps=maxval - minval)
        slider.pack(pady=5)
        return slider, label_widget

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")])
        if not file_path:
            return

        if self.image is None:
            # Cargar la primera imagen
            self.reset_ui()
            self.image = cv2.imread(file_path)
            self.image_original = self.image.copy()

            self.tipo_combo.set("Original")  # Mostrar visualmente el tipo original
            self.on_tipo_change("Original")  # Aplica lógicamente el tipo seleccionado (actualiza typed_image y current_image)

        elif self.second_image is None:
            # Cargar la segunda imagen
            self.second_image = cv2.imread(file_path)
            self.second_image_original = self.second_image.copy()

        self.display_image()


    def save_image(self):
        """
        Guarda la imagen mostrada actualmente, usando un diálogo de archivo.
        """
        if self.current_image is None:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", '*.png'), ("JPEG Image", '*.jpg'), ("All Files", '*.*')]
        )
        if file_path:
            # Recuerda que self.current_image está en BGR si no lo hemos modificado
            cv2.imwrite(file_path, self.current_image)

    def display_image(self):
        if self.current_image is not None:
            # Display first image
            img_rgb = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_pil.thumbnail((400, 300))
            imgtk = ImageTk.PhotoImage(img_pil)
            self.image_panel.configure(image=imgtk, text="")
            self.image_panel.image = imgtk
            h, w = self.current_image.shape[:2]
            self.size_label.configure(text=f"Tamaño Primera: {w} x {h}")

        if self.second_image is not None:
            # Display second image
            second_rgb = cv2.cvtColor(self.second_image, cv2.COLOR_BGR2RGB)
            second_pil = Image.fromarray(second_rgb)
            second_pil.thumbnail((400, 300))
            imgtk2 = ImageTk.PhotoImage(second_pil)
            self.image_panel2.configure(image=imgtk2, text="")
            self.image_panel2.image = imgtk2
            h2, w2 = self.second_image.shape[:2]
            self.size_label2.configure(text=f"Tamaño Segunda: {w2} x {h2}")
        else:
            # Clear second panel if not present
            self.image_panel2.configure(image="", text="Aquí se mostrará la imagen 2")
            self.size_label2.configure(text="")

    def apply_changes(self):
        if self.image is None:
            return

        modified = self.image.copy()

        # Ajuste de brillo y contraste "simple" con convertScaleAbs
        brillo = self.brillo_slider.get()       # de -100 a 100
        contraste = self.contraste_slider.get() # de -100 a 100

        alpha = 1 + (contraste / 100.0)  # factor
        beta = brillo  # offset

        modified = cv2.convertScaleAbs(modified, alpha=alpha, beta=beta)
        self.current_image = modified
        self.display_image()

    def apply_translation(self):
        # Placeholder sin funcionalidad de traducción manual
        pass

    def recortar(self):
        # Placeholder sin funcionalidad de recorte manual
        pass

    def apply_resize(self):
        """
        Lee ancho y alto de los campos de texto y cambia el tamaño de la imagen.
        """
        if self.current_image is None:
            return
        
        # Obtenemos los valores de ancho y alto
        try:
            new_width = int(self.width_entry.get())
            new_height = int(self.height_entry.get())
        except ValueError:
            # Si no puso un número, no hacer nada
            return

        # Llamamos a la función de PrimPy para cambiar el tamaño
        resized = pi.cambiarTamaño(self.current_image, (new_width, new_height))
        self.current_image = resized
        self.display_image()

    def apply_zoom(self):
        # Placeholder for zoom functionality
        pass

    def apply_fusion(self):
        if self.image is not None and self.second_image is not None:
            alpha = self.fusion_slider.get()
            # Convert BGR to RGB for PrimPy usage if needed, or directly use:
            fused = pi.fusionarImagenesConEq(self.image, self.second_image, alpha)
            # Convert back to BGR
            fused_bgr = (fused*255).astype(np.uint8)
            self.current_image = fused_bgr
            self.second_image = None
            self.display_image()

    def reset_ui(self):
        """
        Restaura la interfaz de usuario a su estado inicial.
        """
        # 1. Restaurar los sliders (brillo y contraste en 0).
        self.brillo_slider.set(0)
        self.brillo_label.configure(text="Brillo: 0.00")
        self.contraste_slider.set(0.1)
        self.contraste_label.configure(text="Contraste: 0.10")

        # 2. Restaurar el menú de tipo de imagen (“Original”).
        self.tipo_combo.set("Original")

        # 3. Restaurar la selección de las zonas a “clara”.
        self.zona_var.set("clara")

        # 4. Desmarcar todos los checkboxes (RGB y CMY).
        for color_var in self.rgb_checks.values():
            color_var.set(False)
        for color_var in self.cmy_checks.values():
            color_var.set(False)

        # 5. Resetear otros elementos como sliders de rotación, entradas de recorte, etc.
        self.rot_slider.set(0)
        self.zoom_slider.set(1)
        self.fusion_slider.set(0.5)
        # Clear user typed text, but preserve placeholders
        for entry in [self.dx_entry, self.dy_entry, self.x1_entry, self.y1_entry, self.x2_entry, self.y2_entry, self.width_entry, self.height_entry, self.zoom_x_entry, self.zoom_y_entry]:
            if entry.get() not in ["", entry._placeholder_text]:
                entry.delete(0, 'end')
    
    def restore_image(self):
        """
        Restaura la imagen original y actualiza el panel.
        """

        #Siempre restaurar la interfaz
        self.reset_ui()
        if self.image_original is not None:
            self.image = self.image_original.copy()
            self.current_image = self.image.copy()
        if self.second_image_original is not None:
            self.second_image = self.second_image_original.copy()
        self.display_image()
        
    def remove_image(self):
        """
        Elimina la imagen actual y limpia el panel.
        """
        self.image = None
        self.second_image = None
        self.current_image = None
        self.image_panel.configure(image="", text="Aquí se mostrará la imagen 1")
        self.size_label.configure(text="")
        self.image_panel2.configure(image="", text="Aquí se mostrará la imagen 2")
        self.size_label2.configure(text="")
        # Restaurar la interfaz a su estado inicial
        self.reset_ui()

    def see_histogram(self):
        if self.image is None:
            mb.showwarning("Advertencia", "Debe cargar la imagen 1 para ver su histograma.")
            return
        img_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        pi.histograma(img_rgb) #Llamado al metodo de PrimPy para mostrar el histograma  


    def on_brillo_slider_change(self, value):
        if self.typed_image is None:
            return
        brillo_normalizado = float(value) / 100.0
        self.brillo_label.configure(text=f"Brillo: {brillo_normalizado:.2f}")

        temp = pi.ajustarBrillo(self.typed_image.copy(), brillo_normalizado)
        temp = (temp * 255).clip(0, 255).astype(np.uint8)
        self.current_image = temp
        self.display_image()


    def on_zone_change(self):
        if self.image_original is None:
            return
        self.on_contraste_slider_change(self.contraste_slider.get())

    def on_contraste_slider_change(self, value):
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
        all_checks = {**self.rgb_checks, **self.cmy_checks}
        # Ensure only one can be selected
        checked = [color for color, var in all_checks.items() if var.get()]
        if len(checked) > 1:
            newly_checked = checked[-1]
            for color in checked[:-1]:
                all_checks[color].set(False)
        if self.typed_image is None:
            return
        # If none is selected, revert to typed_image
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

if __name__ == '__main__':
    app = ImageViewer()
    app.mainloop()
