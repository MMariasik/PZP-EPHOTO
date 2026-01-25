import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
from tkinter import filedialog

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ImageEditorApp(ctk.CTk):
    def __init__(self): 
        super().__init__()

        self.title("E-PHOTO - Rozbudowane Filtry")
        self.geometry("1100x800")
        
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)

        self.current_image = None
        self.original_image = None # Przechowuje oryginał do resetu
        self.photo_image = None

        self.imagesSaves = []
        
        # --- SIDEBAR ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="E-PHOTO 📸", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=(20, 10))
        
        self.load_button = ctk.CTkButton(self.sidebar_frame, text="⬆️ Wczytaj Obraz", command=self.load_image)
        self.load_button.pack(padx=20, pady=10)

        self.tool_label = ctk.CTkLabel(self.sidebar_frame, text="FILTRY I EFEKTY", font=ctk.CTkFont(weight="bold"))
        self.tool_label.pack(pady=(10, 5))

        self.scroll_frame = ctk.CTkScrollableFrame(self.sidebar_frame, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.init_filter_buttons()

        self.reset_button = ctk.CTkButton(self.sidebar_frame, text="🔄 Resetuj Obraz", fg_color="#D32F2F", hover_color="#B71C1C", command=self.reset_image)
        self.reset_button.pack(padx=20, pady=5)

        self.reset_button = ctk.CTkButton(self.sidebar_frame, text="🔄 Cofnij efekt", fg_color="#D32F2F", hover_color="#B76A1C", command=self.undo)
        self.reset_button.pack(padx=20, pady=5)

        self.export_button = ctk.CTkButton(self.sidebar_frame, text="⬇️ Eksportuj", fg_color="#4CAF50", hover_color="#45A049", command=self.export_image, state="disabled")
        self.export_button.pack(padx=20, pady=(10, 20))

        # --- MAIN CANVAS ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.image_label = ctk.CTkLabel(self.main_frame, text="Wczytaj obraz, aby rozpocząć", font=ctk.CTkFont(size=18))
        self.image_label.grid(row=0, column=0, sticky="nsew")

    def init_filter_buttons(self):
        filters = [
            ("Obróć 90°", "Obrót"),
            ("Czarno-Białe", "B&W"),
            ("Sepia (Retro)", "Sepia"),
            ("Negatyw", "Invert"),
            ("Rozmycie", "Blur"),
            ("Szkic (Edges)", "Sketch"),
            ("Żywe Kolory", "Vibrant"),
            ("Wyostrzenie", "Sharpen"),
            ("Kontury", "Contour"),
            ("Auto Kontrast", "Contrast")
        ]

        for text, mode in filters:
            btn = ctk.CTkButton(self.scroll_frame, text=text, command=lambda m=mode: self.apply_effect(m))
            btn.pack(fill="x", padx=10, pady=3)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.original_image = ImageOps.exif_transpose(self.original_image)
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)
            self.export_button.configure(state="normal")
            self.imagesSaves = []

    def reset_image(self):
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.imagesSaves = []
            self.display_image(self.current_image)
        
    def undo(self):
        if self.original_image and self.imagesSaves:
            self.current_image = self.imagesSaves.pop()
            self.display_image(self.current_image)

    def display_image(self, img_data):
        self.update_idletasks()

        w_frame, h_frame = self.main_frame.winfo_width()-40, self.main_frame.winfo_height()-40
        if w_frame <= 0 or h_frame <= 0: w_frame, h_frame = 800, 600

        img_w, img_h = img_data.size
        ratio = min(w_frame/img_w, h_frame/img_h)
        new_w = int(img_w * ratio)
        new_h = int(img_h * ratio)
        
        self.photo_image = ctk.CTkImage(
            light_image=img_data, 
            dark_image=img_data, 
            size=(new_w, new_h)  
        )
        
        self.image_label.configure(image=self.photo_image, text="")

    def apply_effect(self, mode):
        if not self.current_image: return

        self.imagesSaves.append(self.current_image.copy())
        
        if self.current_image.mode != "RGB":
            self.current_image = self.current_image.convert("RGB")

        if mode == "Obrót":
            self.current_image = self.current_image.rotate(-90, expand=True)
        elif mode == "B&W":
            self.current_image = ImageOps.grayscale(self.current_image).convert("RGB")
        elif mode == "Invert":
            self.current_image = ImageOps.invert(self.current_image)
        elif mode == "Blur":
            self.current_image = self.current_image.filter(ImageFilter.GaussianBlur(radius=2))
        elif mode == "Sharpen":
            self.current_image = self.current_image.filter(ImageFilter.SHARPEN)
        elif mode == "Sketch":
            self.current_image = self.current_image.filter(ImageFilter.CONTOUR)
        elif mode == "Contour":
            self.current_image = self.current_image.filter(ImageFilter.FIND_EDGES)
        elif mode == "Contrast":
            self.current_image = ImageOps.autocontrast(self.current_image)
        elif mode == "Vibrant":
            enhancer = ImageEnhance.Color(self.current_image)
            self.current_image = enhancer.enhance(1.8)
        elif mode == "Sepia":
            sepia_img = ImageOps.grayscale(self.current_image)
            sepia_img = ImageOps.colorize(sepia_img, "#704214", "#C0A080")
            self.current_image = sepia_img

        self.display_image(self.current_image)

    def export_image(self):
        if self.current_image:
            path = filedialog.asksaveasfilename(defaultextension=".png")
            if path: self.current_image.save(path)

if __name__ == "__main__":
    app = ImageEditorApp()
    app.mainloop()