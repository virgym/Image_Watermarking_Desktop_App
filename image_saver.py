from tkinter import filedialog, END


# Saves the watermarked image
class ImageSaver:
    def __init__(self, app):
        self.app = app


    def save_watermarked_image(self):
        if self.app.logo_text_watermarked_image:
            self.save_image(self.app.logo_text_watermarked_image)
        elif self.app.logo_watermarked_image:
            self.save_image(self.app.logo_watermarked_image)
        elif self.app.text_watermarked_image:
            self.save_image(self.app.text_watermarked_image)


    def save_image(self, image):
        save_path = filedialog.asksaveasfilename(initialdir="Downloads", defaultextension=".png", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif"), ("All files", "*.*")])
        if save_path:
            image.save(save_path)
            self.app.watermark_text_entry.delete(0, END)
            self.app.rotation_angle_var.set(0)
