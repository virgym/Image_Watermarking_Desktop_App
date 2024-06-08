# Image Watermarking Desktop App

<p>A desktop application with a Tkinter Graphical User Interface (GUI) where you can upload an image and use Python to add a watermark logo, text or both.</p>

## Project Demonstration

<p align='center'>
  <img src='/demo/hello.png'/>
</p>


## Modules Used
### WatermarkApp Class:
- Manages the main application and UI setup.
- Handles events such as uploading an image and clearing the canvas.
- Contains a reference to ImageProcessor and ImageSaver to delegate specific tasks.

### ImageProcessor Class:
- Contains methods for processing images, such as adding logo and text watermarks.
- Interacts with the WatermarkApp instance to access the current state and update the displayed image.

### ImageSaver Class:
- Manages saving the watermarked images.
- Interacts with the WatermarkApp instance to access the current state of the watermarked images.


## Usage and Installation
1. Clone the repository.
2. Install the required packages from requirements.txt: pip install -r requirements.txt
3. Run "python watermark_app.py". This will display a GUI where you can upload, watermark, preview, and save the watermarked image. See demo on the demo/ folder.
<p align='center'>
  <img src='/demo/UI.png'/>
</p>

## Author
👩‍💻 Mutshinya Virginia Mudau

- GitHub: <a href='https://github.com/virgym' target='_blank'>@virgym</a>
- LinkedIn: <a href='https://www.linkedin.com/in/mutshinya-virginia-mudau-168a891b9/' target='_blank'>Mutshinya Virginia Mudau</a>

<br>
<p>Developed and tested in Python version 3.12.0 on a 64-bit Windows 10 Operating System.</p>

## License
<p>This project is published under the MIT license. Please refer to LICENSE <a href='LICENSE'> for more details.</a></p>
