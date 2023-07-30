from tkinter import Tk, Canvas
from PIL import Image, ImageTk, ImageSequence

class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.attributes('-transparentcolor', '#f0f0f0')  # Set the transparent color to slightly dark gray

        # Load the image and create an iterator over its frames
        self._image_sequence = ImageSequence.Iterator(Image.open("./kurukuru.gif"))

        # Convert the frames to PIL Image objects and store them along with their durations
        self._frames = [(frame.convert('RGBA'), frame.info['duration']) for frame in self._image_sequence]
        self._zoomed_frames = self._frames.copy()
        self._frame_index = 0
        self._zoom_level = 1.0

        # Create a PhotoImage from the first frame and create an image item using it
        self.photo = ImageTk.PhotoImage(image=self._zoomed_frames[0][0])
        self.canvas = Canvas(self, width=self.photo.width(), height=self.photo.height())
        self.canvas.pack()
        self.image = self.canvas.create_image(self.photo.width()//2, self.photo.height()//2, image=self.photo)

        self.show_frame()

        # Bind the mouse scroll event to the zoom_image function
        self.bind("<MouseWheel>", self.zoom_image)

    def zoom_image(self, event):
        # Increase/Decrease the zoom level based on the scroll direction
        self._zoom_level *= 1.1 if event.delta > 0 else 0.9

        # Calculate the ratios of the mouse pointer to the left and top edges of the image
        x_ratio = event.x / self.winfo_width()
        y_ratio = event.y / self.winfo_height()

        # Resize all frames according to the new zoom level and update the image item
        self._zoomed_frames = [(frame.resize((int(frame.width * self._zoom_level), int(frame.height * self._zoom_level)), 
                                              Image.Resampling.LANCZOS), duration) for frame, duration in self._frames]
        self.photo = ImageTk.PhotoImage(image=self._zoomed_frames[self._frame_index][0])
        self.canvas.itemconfigure(self.image, image=self.photo)

        # Adjust the canvas size
        self.canvas.config(width=self.photo.width(), height=self.photo.height())

        # Move the window so that the mouse pointer remains at the same position on the image
        x = self.winfo_x() - int((self.winfo_width() - self.canvas.winfo_width()) * x_ratio)
        y = self.winfo_y() - int((self.winfo_height() - self.canvas.winfo_height()) * y_ratio)
        self.geometry(f'+{x}+{y}')

    def show_frame(self):
        # Update the image item to show the next frame
        self._frame_index = (self._frame_index + 1) % len(self._frames)
        self.photo = ImageTk.PhotoImage(image=self._zoomed_frames[self._frame_index][0])
        self.canvas.itemconfigure(self.image, image=self.photo)

        # Get the duration of the current frame
        duration = self._frames[self._frame_index][1]
        self.after(duration, self.show_frame)

app = Application()
app.mainloop()
