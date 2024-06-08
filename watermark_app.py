from PIL import Image, ImageTk
from tkinter import filedialog, Tk, Canvas, Label, Entry, StringVar, OptionMenu, IntVar, Scale, PhotoImage,  HORIZONTAL, END
import customtkinter as ctk
import os 
from image_processor import ImageProcessor
from image_saver import ImageSaver


# Main class for the application
class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermarking App")
        icon = PhotoImage(file='./images/icon.png')
        root.iconphoto(False, icon)
        self.root.geometry('950x600')
        self.root.config(padx=20, pady=20, bg="#4D869C")
        self.root.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform='a')
        self.root.columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')

        self.image_processor = ImageProcessor(self)
        self.image_saver = ImageSaver(self)

        # Load default image
        self.default_image_path = os.path.join(os.path.dirname(__file__), "images", "holder.jpg")

        self.setup_ui()

        # Set the background image
        self.set_background_image()
        self.root.bind('<Configure>', self.resize_background_image)


    # UI Setup function 
    def setup_ui(self):
        button_fg_color = "#7AB2B2"
        button_hover_color = "#5A9A9A"
        TEXT_COLOR = "white"
        TEXT_FONT = "Franklin Gothic Medium Italic"
        BUTTON_TEXT_SIZE = 12
        LABEL_TEXT_SIZE = 9

        self.canvas = Canvas(self.root, background="#C7C8CC", borderwidth=4, relief="groove")
        self.canvas.grid(row=0, column=2, columnspan=4, rowspan=6, sticky='nsew', padx=15, pady=15)
        self.canvas.bind('<Configure>', self.on_resize)

        upload_button = ctk.CTkButton(self.root, text="Upload a Picture", command=self.upload_image, font=(TEXT_FONT, BUTTON_TEXT_SIZE), corner_radius=15, fg_color=button_fg_color, hover_color=button_hover_color, text_color=TEXT_COLOR)
        upload_button.grid(row=0, column=0, sticky='ew', padx=5)

        choose_watermark_button = ctk.CTkButton(self.root, text="Upload a Logo", command=self.image_processor.add_logo_watermark, font=(TEXT_FONT, BUTTON_TEXT_SIZE), corner_radius=15, fg_color=button_fg_color, hover_color=button_hover_color, text_color=TEXT_COLOR)
        choose_watermark_button.grid(row=1, column=0, sticky='ew', padx=5)

        text_label = Label(text="Enter Text:", bg=button_fg_color ,fg=TEXT_COLOR, font=(TEXT_FONT, LABEL_TEXT_SIZE))
        text_label.grid(row=2, column=0, sticky='ew', padx=5)
        self.watermark_text_entry = Entry(width=30, bg=button_fg_color, fg=TEXT_COLOR, font=(TEXT_FONT, LABEL_TEXT_SIZE))
        self.watermark_text_entry.grid(row=2, column=1, padx=5, sticky='ew')
        self.watermark_text_entry.focus()
        self.watermark_text_entry.bind("<KeyRelease>", self.update_text_watermark)

        font_size_label = Label(text="Font Size:", bg=button_fg_color, fg=TEXT_COLOR, font=(TEXT_FONT, LABEL_TEXT_SIZE))
        font_size_label.grid(row=3, column=0, sticky='ew', padx=5)
        self.font_size_entry = Entry(width=6, bg=button_fg_color, fg=TEXT_COLOR, font=(TEXT_FONT, LABEL_TEXT_SIZE))
        self.font_size_entry.grid(row=3, column=1, padx=5, sticky='ew')
        self.font_size_entry.insert(0, "32")
        self.font_size_entry.bind("<KeyRelease>", self.update_text_watermark)

        font_type_label = Label(text="Font Type:", bg=button_fg_color, fg=TEXT_COLOR, font=(TEXT_FONT, LABEL_TEXT_SIZE))
        font_type_label.grid(row=4, column=0, sticky='ew', padx=5)
        self.font_type_var = StringVar(self.root)
        self.font_type_var.set("Arial")
        self.font_type_dropdown = OptionMenu(self.root, self.font_type_var, "Arial", "Times New Roman", "Verdana", "Georgia", "Courier New", "Comic Sans MS", "Calibri", "Tahoma", "Trebuchet MS", "Lucida Console", "Franklin Gothic Medium", "Franklin Gothic Medium Italic")
        self.font_type_dropdown.grid(row=4, column=1, padx=5, sticky='ew')
        self.font_type_dropdown.config(bg=button_fg_color, width=24, height=1, font=(TEXT_FONT, LABEL_TEXT_SIZE), fg=TEXT_COLOR)
        self.font_type_var.trace("w", self.update_text_watermark)

        info_label = Label(text="⭐⭐⭐⭐⭐  You can only rotate the watermark if it is text-only. Rotation is not supported for text combined with a logo.", font=(TEXT_FONT, 8), bg=self.root['bg'], fg=TEXT_COLOR)
        info_label.grid(row=6, column=0, columnspan=4, sticky='ew')

        rotation_angle_label = Label(text="Rotation Angle:", bg=button_fg_color, fg=TEXT_COLOR, width=1, font=(TEXT_FONT, LABEL_TEXT_SIZE))
        rotation_angle_label.grid(row=5, column=0, sticky='ew', padx=5)
        self.rotation_angle_var = IntVar(value=0)
        self.rotation_angle_slider = Scale(self.root, from_=-360, to=360, variable=self.rotation_angle_var, orient=HORIZONTAL, width=10, troughcolor='#CDE8E5', bg=button_fg_color, sliderlength=10)
        self.rotation_angle_slider.grid(row=5, column=1, padx=5, sticky='ew')
        self.rotation_angle_slider.bind("<ButtonRelease-1>", self.update_text_watermark)

        save_image_button = ctk.CTkButton(self.root, text="Save Image", font=(TEXT_FONT, BUTTON_TEXT_SIZE), command=self.image_saver.save_watermarked_image, corner_radius=15, fg_color=button_fg_color, hover_color=button_hover_color, text_color=TEXT_COLOR)
        save_image_button.grid(row=7, column=2, sticky='ew', padx=2)

        clear_button = ctk.CTkButton(self.root, text="Clear All", command=self.clear_canvas, font=(TEXT_FONT, BUTTON_TEXT_SIZE), corner_radius=15, fg_color=button_fg_color, hover_color=button_hover_color, text_color=TEXT_COLOR)
        clear_button.grid(row=7, column=3, sticky='ew', padx=2)



    # Function to set the background image
    def set_background_image(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        bg_image_path = os.path.join(current_path, "images", "wave_big.jpg")
        self.bg_image = Image.open(bg_image_path)
        self.bg_photo_image = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = Label(self.root, image=self.bg_photo_image)
        self.bg_label.image = self.bg_photo_image
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.lower()

    # Function to resize the background image to fill the window
    def resize_background_image(self, event):
        new_width = event.width
        new_height = event.height
        resized_image = self.bg_image.resize((new_width, new_height))
        self.bg_photo_image = ImageTk.PhotoImage(resized_image)
        # Update the label with the new image
        self.bg_label.config(image=self.bg_photo_image)
        self.bg_label.image = self.bg_photo_image

        
    # Function to upload an image 
    def upload_image(self):
        self.clear_canvas()
        self.rotation_angle_var.set(0)
        self.file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif"), ("All files", "*.*")])
        if self.file_path:
            pillow_image = Image.open(self.file_path).convert("RGB")
            resized_image = pillow_image.resize((self.canvas.winfo_width(), self.canvas.winfo_height()))
            photo_image = ImageTk.PhotoImage(resized_image)
            self.canvas.image = photo_image
            self.canvas.create_image(0, 0, image=photo_image, anchor="nw")
        else:
            # If no image is uploaded, display the default image
            self.display_default_image()


    # Function to get the font size from the entry
    def get_font_size(self):
        try:
            return int(self.font_size_entry.get())
        except ValueError:
            return 40  # Default to 40 if the input is invalid


    # Function to get the font type from the dropdown
    def get_font_type(self):
        font_type = self.font_type_var.get()
        font_file_paths = {
            "Arial": "C:/Windows/Fonts/arial.ttf",
            "Times New Roman": "C:/Windows/Fonts/times.ttf",
            "Verdana": "C:/Windows/Fonts/verdana.ttf",
            "Georgia": "C:/Windows/Fonts/georgia.ttf",
            "Courier New": "C:/Windows/Fonts/cour.ttf",
            "Comic Sans MS": "C:/Windows/Fonts/comic.ttf",
            "Calibri": "C:/Windows/Fonts/calibri.ttf",
            "Tahoma": "C:/Windows/Fonts/tahoma.ttf",
            "Trebuchet MS": "C:/Windows/Fonts/trebuc.ttf",
            "Lucida Console": "C:/Windows/Fonts/lucon.ttf",
            "Franklin Gothic Medium": "C:/Windows/Fonts/framd.ttf",
            "Franklin Gothic Medium Italic": "C:/Windows/Fonts/framdit.ttf"
        }
        return font_file_paths[font_type]
    

    # Function to get the rotation angle from the slider
    def get_rotation_angle(self):
        return self.rotation_angle_var.get()
    

    # Function to update the text watermark on the canvas. This function is called whenever the user types in the watermark text or changes the font size or font type
    def update_text_watermark(self, *args):
        watermarked_image = self.image_processor.add_text_or_both_watermarks()
        self.display_image(watermarked_image)


   # Display default image on the canvas. This function is called when no image is uploaded or when the canvas is cleared
    def display_default_image(self):
        try:
            default_image = Image.open(self.default_image_path)
            self.display_image(default_image)
        except Exception as e:
            print(f"Failed to load default image: {e}")


    # Function to isplay the uploaded image
    def display_image(self, image):
        # Ensure canvas dimensions are updated before resizing the image
        self.root.update_idletasks()
        resized_image = image.resize((self.canvas.winfo_width(), self.canvas.winfo_height())).convert("RGBA")
        tk_image = ImageTk.PhotoImage(resized_image)
        self.canvas.image = tk_image 
        self.canvas.create_image(0, 0, image=tk_image, anchor="nw")
        

    # Update canvas size on window resize
    def on_resize(self, event):
        if hasattr(self, 'canvas') and self.canvas.winfo_width() > 1:
            if hasattr(self, 'file_path') and self.file_path:
                image = Image.open(self.file_path)
            else:
                image = Image.open(self.default_image_path)
            self.display_image(image)


    # Clear the canvas
    def clear_canvas(self):
        self.canvas.delete("all")
        self.watermark_text_entry.delete(0, END)
        self.logo_watermarked_image = None
        self.text_watermarked_image = None
        self.logo_text_watermarked_image = None
        self.rotation_angle_var.set(0)
        self.display_default_image()


if __name__ == "__main__":
    root = Tk()
    # Create a new instance of the WatermarkApp class
    app = WatermarkApp(root)
    root.mainloop()