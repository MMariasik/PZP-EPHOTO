import customtkinter as ctk
from PIL import Image, ImageTk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ImageEditorApp(ctk.CTk):

    def init_buttons(self):
        self.load_button = ctk.CTkButton(self.sidebar_frame, text="⬆️ Wczytaj Obraz", command=self.load_image)
        self.load_button.grid(row=1, column=0, padx=20, pady=10)

        self.tool_label = ctk.CTkLabel(self.sidebar_frame, text="EDYCJA", fg_color="transparent", font=ctk.CTkFont(weight="bold"))
        self.tool_label.grid(row=2, column=0, padx=20, pady=(20, 0), sticky="w")

        self.crop_button = ctk.CTkButton(self.sidebar_frame, text="✂️ Przytnij & Obróć", command=lambda: self.apply_effect("Przycinanie"))
        self.crop_button.grid(row=3, column=0, padx=20, pady=5)
        
        self.exposure_button = ctk.CTkButton(self.sidebar_frame, text="💡 Ekspozycja/Kolory", command=lambda: self.apply_effect("Korekta Kolorów"))
        self.exposure_button.grid(row=4, column=0, padx=20, pady=5)
        
        self.filter_button = ctk.CTkButton(self.sidebar_frame, text="✨ Filtry", command=lambda: self.apply_effect("Filtry"))
        self.filter_button.grid(row=5, column=0, padx=20, pady=5)

        self.export_button = ctk.CTkButton(
            self.sidebar_frame, 
            text="⬇️ Eksportuj", 
            fg_color="#4CAF50", 
            hover_color="#45A049", 
            command=self.export_image,
            state="disabled" 
        )
        self.export_button.grid(row=7, column=0, padx=20, pady=(10, 20), sticky="s")


    def __init__(self):
        super().__init__()

        self.title("E-PHOTO - Prosta Edycja Zdjęć")
        self.geometry("1000x700")
        
        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)

        self.current_image = None
        self.photo_image = None
        
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="E-PHOTO 📸", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.init_buttons()

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.image_label = ctk.CTkLabel(self.main_frame, text="Wczytaj obraz, aby rozpocząć edycję", font=ctk.CTkFont(size=18))
        self.image_label.grid(row=0, column=0, sticky="nsew")


    def load_image(self):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        if file_path:
            try:
                self.current_image = Image.open(file_path)
                print(f"Wczytano: {file_path}")
                self.display_image(self.current_image)
            except Exception as e:
                print(f"Błąd podczas wczytywania obrazu: {e}")

    def display_image(self, img_data):
        main_width = self.main_frame.winfo_width() - 20
        main_height = self.main_frame.winfo_height() - 20
        
        if main_width <= 0 or main_height <= 0:
            self.update_idletasks()
            main_width = self.main_frame.winfo_width() - 20
            main_height = self.main_frame.winfo_height() - 20
        
        img_width, img_height = img_data.size
        ratio = min(main_width / img_width, main_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)

        resized_image = img_data.resize((new_width, new_height))
        self.photo_image = ImageTk.PhotoImage(resized_image)
        
        self.image_label.configure(image=self.photo_image, text="")
        self.image_label.image = self.photo_image

        self.export_button.configure(state="normal")


    def apply_effect(self, effect_name):
        if self.current_image:
            print(f"Aplikowanie efektu: {effect_name}")
            # TUTAJ BĘDZIE LOGIKA EDYCJI ZDJĘĆ Z UŻYCIEM PIL/OpenCV
            print("Funkcja niezaimplementowana.")
        else:
            print("Wczytaj najpierw obraz.")

    def export_image(self):
        from tkinter import filedialog
        if self.current_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG file", "*.png"), ("JPEG file", "*.jpg")]
            )
            if file_path:
                try:
                    self.current_image.save(file_path)
                    print(f"Obraz zapisany pomyślnie w: {file_path}")
                except Exception as e:
                    print(f"Błąd podczas zapisu obrazu: {e}")
        else:
            print("Brak obrazu do eksportu.")

if __name__ == "__main__":
    app = ImageEditorApp()
    app.mainloop()