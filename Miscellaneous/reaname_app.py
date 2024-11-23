import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Renamer")
        
        # Frame principal
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)
        
        # Botón para seleccionar carpeta
        self.select_button = tk.Button(self.main_frame, text="Select Folder", command=self.select_folder)
        self.select_button.pack()
        
        # Label para la imagen
        self.image_label = tk.Label(self.main_frame)
        self.image_label.pack()
        
        # Campo para renombrar
        self.rename_field = tk.Entry(self.main_frame, width=50)
        self.rename_field.pack(pady=5)
        
        # Botones para acción
        self.action_frame = tk.Frame(self.main_frame)
        self.action_frame.pack()
        
        self.save_button = tk.Button(self.action_frame, text="Rename & Next", command=self.rename_image)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.skip_button = tk.Button(self.action_frame, text="Skip", command=self.skip_image)
        self.skip_button.pack(side=tk.LEFT, padx=5)
        
        # Variables para imágenes y carpeta
        self.folder_path = None
        self.image_files = []
        self.current_image_index = -1
        self.current_image_path = None
        
    def select_folder(self):
        # Selección de carpeta
        self.folder_path = filedialog.askdirectory(title="Select Folder with Images")
        if not self.folder_path:
            return
        
        # Obtener archivos de imagen
        self.image_files = [f for f in os.listdir(self.folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        
        if not self.image_files:
            messagebox.showerror("Error", "No images found in the selected folder!")
            return
        
        # Reiniciar índice y mostrar primera imagen
        self.current_image_index = 0
        self.show_image()
    
    def show_image(self):
        if self.current_image_index < 0 or self.current_image_index >= len(self.image_files):
            messagebox.showinfo("Info", "No more images.")
            return
        
        # Obtener ruta de la imagen actual
        self.current_image_path = os.path.join(self.folder_path, self.image_files[self.current_image_index])
        
        # Cargar imagen
        img = Image.open(self.current_image_path)
        img.thumbnail((600, 400))  # Ajustar tamaño
        photo = ImageTk.PhotoImage(img)
        
        # Mostrar imagen
        self.image_label.config(image=photo)
        self.image_label.image = photo
        
        # Borrar campo de texto y sugerir nombre
        self.rename_field.delete(0, tk.END)
        self.rename_field.insert(0, os.path.splitext(self.image_files[self.current_image_index])[0])
    
    def rename_image(self):
        new_name = self.rename_field.get().strip()
        if not new_name:
            messagebox.showerror("Error", "New name cannot be empty!")
            return
        
        # Nueva ruta
        new_path = os.path.join(self.folder_path, new_name + os.path.splitext(self.current_image_path)[1])
        
        try:
            os.rename(self.current_image_path, new_path)
            self.image_files[self.current_image_index] = new_name + os.path.splitext(self.current_image_path)[1]
            self.current_image_index += 1
            self.show_image()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename image: {e}")
    
    def skip_image(self):   
        # Saltar a la siguiente imagen
        self.current_image_index += 1
        self.show_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRenamerApp(root)
    root.mainloop()
