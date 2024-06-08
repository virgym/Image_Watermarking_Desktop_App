from PIL import Image, ImageDraw, ImageFont
from tkinter import filedialog


# Class to process images
class ImageProcessor:
    def __init__(self, app):
        self.app = app


    # A function to add logo watermark to an image
    def add_logo_watermark(self):
        if not self.app.file_path:
            print("Please upload an image first.")
            return
        logo_path = filedialog.askopenfilename(title="Select a File", filetypes=[("All files", "*.*")])
        if not logo_path:
            print("No logo selected.")
            return

        try:
            logo_image = Image.open(logo_path).convert("RGBA")
            background_image = Image.open(self.app.file_path).convert("RGBA")
            # Resize logo to fit in background. Use thumbnail() to keep the image aspect ratio
            logo_image.thumbnail((background_image.width, background_image.height))

            # Calculate the position to center the logo on the image
            logo_x = (background_image.width - logo_image.width) // 2
            logo_y = (background_image.height - logo_image.height) // 2
            # Create a transparent layer for the logo to merge properly
            overlay = Image.new('RGBA', background_image.size, (0, 0, 0, 0))
            overlay.paste(logo_image, (logo_x, logo_y))

            # Add the logo to the background image
            self.app.logo_watermarked_image = Image.alpha_composite(background_image, overlay)
            self.app.display_image(self.app.logo_watermarked_image)
            return self.app.logo_watermarked_image
        except Exception as e:
            print(f"Error adding logo watermark: {e}")
            return None


    # A function to add text watermark to an image or both text and logo watermarks
    def add_text_or_both_watermarks(self):
        text_to_add = self.app.watermark_text_entry.get()
        font_size = self.app.get_font_size()
        font_type = self.app.get_font_type()
        text_font = ImageFont.truetype(font_type, font_size)
        rotation_angle = self.app.get_rotation_angle()

        if self.app.logo_watermarked_image:
            image = self.app.logo_watermarked_image.copy()
            overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(overlay)
            draw.text((10, 10), text_to_add, font=text_font, fill=(255, 255, 255, 200))
            self.app.logo_text_watermarked_image = Image.alpha_composite(self.app.logo_watermarked_image, overlay)
            return self.app.logo_text_watermarked_image
        else:
            try:
                background_image = Image.open(self.app.file_path).convert("RGBA")
                overlay = Image.new("RGBA", background_image.size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(overlay)
                text_width, text_height = draw.textbbox((0, 0), text_to_add, font=text_font)[2:]
                text_x = (background_image.width - text_width) // 2
                text_y = (background_image.height - text_height) // 2            

                # Rotate the text before adding it to the overlay
                rotated_text = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
                rotated_draw = ImageDraw.Draw(rotated_text)
                rotated_draw.text((0, 0), text_to_add, font=text_font, fill=(255, 255, 255, 230))
                rotated_text = rotated_text.rotate(rotation_angle, expand=True)

                # Add the rotated text to the overlay
                overlay.paste(rotated_text, (int(text_x), int(text_y)), rotated_text)
                self.app.text_watermarked_image = Image.alpha_composite(background_image, overlay)
                return self.app.text_watermarked_image
            except (OSError, Exception) as e:
                print(f"Error adding text watermark: {e}")
            return None
        