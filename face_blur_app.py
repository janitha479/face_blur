import customtkinter as ctk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import os

class FaceBlurApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Face Detection and Blurring Tool")
        self.root.geometry("1200x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables
        self.images = []  # List to store multiple images
        self.current_index = -1
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        container = ctk.CTkFrame(self.root)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel for image list
        left_panel = ctk.CTkFrame(container, width=250)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        
        # Image list frame
        list_frame = ctk.CTkFrame(left_panel)
        list_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        list_label = ctk.CTkLabel(list_frame, text="Image List")
        list_label.pack(pady=5)
        
        self.image_listbox = ctk.CTkTextbox(list_frame, width=230, height=400)
        self.image_listbox.pack(padx=10, pady=5)
        
        # Buttons for left panel
        btn_frame = ctk.CTkFrame(left_panel)
        btn_frame.pack(fill="x", padx=10)
        
        self.add_btn = ctk.CTkButton(btn_frame, text="Add Images", command=self.add_images)
        self.add_btn.pack(fill="x", pady=5)
        
        self.remove_btn = ctk.CTkButton(btn_frame, text="Remove Selected", command=self.remove_image, state="disabled")
        self.remove_btn.pack(fill="x", pady=5)
        
        self.process_all_btn = ctk.CTkButton(btn_frame, text="Process All", command=self.process_all_images, state="disabled")
        self.process_all_btn.pack(fill="x", pady=5)
        
        self.save_all_btn = ctk.CTkButton(btn_frame, text="Save All", command=self.save_all_images, state="disabled")
        self.save_all_btn.pack(fill="x", pady=5)
        
        # Right panel for image display
        right_panel = ctk.CTkFrame(container)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Navigation frame
        nav_frame = ctk.CTkFrame(right_panel)
        nav_frame.pack(fill="x", pady=5)
        
        self.prev_btn = ctk.CTkButton(nav_frame, text="Previous", command=self.show_previous, state="disabled", width=100)
        self.prev_btn.pack(side="left", padx=5)
        
        self.next_btn = ctk.CTkButton(nav_frame, text="Next", command=self.show_next, state="disabled", width=100)
        self.next_btn.pack(side="left", padx=5)
        
        self.blur_btn = ctk.CTkButton(nav_frame, text="Blur Current", command=self.blur_current, state="disabled", width=100)
        self.blur_btn.pack(side="left", padx=5)
        
        self.save_btn = ctk.CTkButton(nav_frame, text="Save Current", command=self.save_current, state="disabled", width=100)
        self.save_btn.pack(side="left", padx=5)
        
        # Images display frame
        self.display_frame = ctk.CTkFrame(right_panel)
        self.display_frame.pack(fill="both", expand=True, pady=10)
        
        # Original image
        original_frame = ctk.CTkFrame(self.display_frame)
        original_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        self.original_label = ctk.CTkLabel(original_frame, text="Original Image")
        self.original_label.pack(pady=5)
        
        self.original_canvas = ctk.CTkCanvas(original_frame, width=450, height=450, bg="#2b2b2b")
        self.original_canvas.pack(expand=True)
        
        # Processed image
        processed_frame = ctk.CTkFrame(self.display_frame)
        processed_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        self.processed_label = ctk.CTkLabel(processed_frame, text="Processed Image")
        self.processed_label.pack(pady=5)
        
        self.processed_canvas = ctk.CTkCanvas(processed_frame, width=450, height=450, bg="#2b2b2b")
        self.processed_canvas.pack(expand=True)
    
    def add_images(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if file_paths:
            for path in file_paths:
                img = cv2.imread(path)
                if img is not None:
                    self.images.append({
                        'path': path,
                        'original': img,
                        'processed': None
                    })
                    self.image_listbox.insert("end", f"{os.path.basename(path)}\n")
            
            if len(self.images) > 0:
                self.current_index = 0 if self.current_index == -1 else self.current_index
                self.update_buttons()
                self.show_current_image()
    
    def remove_image(self):
        if self.current_index >= 0:
            self.images.pop(self.current_index)
            self.image_listbox.delete("1.0", "end")
            for img in self.images:
                self.image_listbox.insert("end", f"{os.path.basename(img['path'])}\n")
            
            if len(self.images) == 0:
                self.current_index = -1
                self.clear_canvases()
            elif self.current_index >= len(self.images):
                self.current_index = len(self.images) - 1
                self.show_current_image()
            else:
                self.show_current_image()
            self.update_buttons()
    
    def show_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_current_image()
            self.update_buttons()
    
    def show_next(self):
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.show_current_image()
            self.update_buttons()
    
    def show_current_image(self):
        if 0 <= self.current_index < len(self.images):
            current = self.images[self.current_index]
            self.display_image(current['original'], self.original_canvas)
            if current['processed'] is not None:
                self.display_image(current['processed'], self.processed_canvas)
            else:
                self.processed_canvas.delete("all")
    
    def blur_current(self):
        if 0 <= self.current_index < len(self.images):
            current = self.images[self.current_index]
            gray = cv2.cvtColor(current['original'], cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            processed = current['original'].copy()
            for (x, y, w, h) in faces:
                face_roi = processed[y:y+h, x:x+w]
                blurred_face = cv2.GaussianBlur(face_roi, (99, 99), 30)
                processed[y:y+h, x:x+w] = blurred_face
            
            current['processed'] = processed
            self.display_image(processed, self.processed_canvas)
            self.save_btn.configure(state="normal")
            messagebox.showinfo("Detection Complete", f"Found {len(faces)} face(s) in the image!")
    
    def process_all_images(self):
        for i, img_data in enumerate(self.images):
            if img_data['processed'] is None:
                gray = cv2.cvtColor(img_data['original'], cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                
                processed = img_data['original'].copy()
                for (x, y, w, h) in faces:
                    face_roi = processed[y:y+h, x:x+w]
                    blurred_face = cv2.GaussianBlur(face_roi, (99, 99), 30)
                    processed[y:y+h, x:x+w] = blurred_face
                
                img_data['processed'] = processed
        
        self.show_current_image()
        self.save_all_btn.configure(state="normal")
        messagebox.showinfo("Batch Processing", "All images have been processed!")
    
    def save_current(self):
        if 0 <= self.current_index < len(self.images) and self.images[self.current_index]['processed'] is not None:
            original_path = self.images[self.current_index]['path']
            directory = os.path.dirname(original_path)
            filename = os.path.basename(original_path)
            name, ext = os.path.splitext(filename)
            
            save_path = filedialog.asksaveasfilename(
                initialdir=directory,
                initialfile=f"{name}_blurred{ext}",
                defaultextension=ext,
                filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
            )
            
            if save_path:
                try:
                    cv2.imwrite(save_path, self.images[self.current_index]['processed'])
                    messagebox.showinfo("Success", "Image saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def save_all_images(self):
        if len(self.images) == 0:
            return
        
        save_dir = filedialog.askdirectory(title="Select Directory to Save All Images")
        if save_dir:
            success_count = 0
            for img_data in self.images:
                if img_data['processed'] is not None:
                    filename = os.path.basename(img_data['path'])
                    name, ext = os.path.splitext(filename)
                    save_path = os.path.join(save_dir, f"{name}_blurred{ext}")
                    
                    try:
                        cv2.imwrite(save_path, img_data['processed'])
                        success_count += 1
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to save {filename}: {str(e)}")
            
            messagebox.showinfo("Batch Save Complete", f"Successfully saved {success_count} out of {len(self.images)} images!")
    
    def display_image(self, cv_image, canvas):
        height, width = cv_image.shape[:2]
        max_size = 450
        scale = min(max_size/width, max_size/height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        resized = cv2.resize(cv_image, (new_width, new_height))
        image = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image)
        
        canvas.image = photo
        canvas.delete("all")
        canvas.create_image(max_size//2, max_size//2, image=photo)
    
    def clear_canvases(self):
        self.original_canvas.delete("all")
        self.processed_canvas.delete("all")
    
    def update_buttons(self):
        has_images = len(self.images) > 0
        self.remove_btn.configure(state="normal" if has_images else "disabled")
        self.process_all_btn.configure(state="normal" if has_images else "disabled")
        self.blur_btn.configure(state="normal" if has_images else "disabled")
        self.prev_btn.configure(state="normal" if self.current_index > 0 else "disabled")
        self.next_btn.configure(state="normal" if self.current_index < len(self.images) - 1 else "disabled")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FaceBlurApp()
    app.run()