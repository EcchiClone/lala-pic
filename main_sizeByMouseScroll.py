from tkinter import Tk, Canvas, PhotoImage, NW
from PIL import Image, ImageTk

root = Tk()

# Hide the title bar
root.overrideredirect(True)

root.attributes('-transparentcolor','#f0f0f0')

# Check if Resampling is not in PIL.Image and if not, assign PIL.Image to it
if not hasattr(Image, 'Resampling'):
    Image.Resampling = Image

# Load the image with PIL
original_pil_img = Image.open("./kurukuru.gif")

# Convert PIL image object to PhotoImage object
img = ImageTk.PhotoImage(original_pil_img)

# Create a global variable for the resized photo image
resized_photoimg = img

# Keep track of the zoom level
zoom_level = 1.0

# Canvas
canvas = Canvas(root, width=img.width(), height=img.height())
canvas.pack()

# Positioning the Image inside the canvas
image_id = canvas.create_image(0, 0, anchor=NW, image=img)

def zoom_image(event):
    global resized_photoimg, zoom_level
    # Increase/Decrease the zoom level based on the scroll direction
    if event.delta > 0:
        zoom_level *= 1.1  # Increase the zoom level by 10%
    else:
        zoom_level *= 0.9  # Decrease the zoom level by 10%
    # Get the original image size
    x, y = original_pil_img.size
    # Apply the zoom level to the original image size
    x, y = int(x * zoom_level), int(y * zoom_level)
    # Resize the original image with NEAREST algorithm
    resized_img = original_pil_img.resize((x, y), Image.Resampling.NEAREST)
    # Convert PIL image object to PhotoImage object
    resized_photoimg = ImageTk.PhotoImage(resized_img)
    # Calculate the ratio of mouse pointer in the image
    ratio_x = event.x / canvas.winfo_width()
    ratio_y = event.y / canvas.winfo_height()
    # Calculate the new position of the window
    new_x = root.winfo_x() + (event.x - ratio_x * x)
    new_y = root.winfo_y() + (event.y - ratio_y * y)
    # Stop the screen update
    root.update_idletasks()
    # Update the image on the canvas
    canvas.itemconfig(image_id, image=resized_photoimg)
    # Update the canvas size
    canvas.config(width=x, height=y)
    # Move the window to the new position
    root.geometry(f"+{int(new_x)}+{int(new_y)}")
    # Restart the screen update
    root.update_idletasks()

# Bind the mouse scroll event to the zoom_image function
root.bind("<MouseWheel>", zoom_image)

# Bind the escape key to exit the program
root.bind("<Escape>", lambda event: root.destroy())

# Variables to keep track of the drag
drag_data = {"x": 0, "y": 0, "start_x": 0, "start_y": 0}

def start_drag(event):
    # Store the initial position of the mouse when the button is pressed
    drag_data["start_x"] = event.x_root
    drag_data["start_y"] = event.y_root

def end_drag(event):
    # Reset the drag data when the mouse button is released
    drag_data["x"] = 0
    drag_data["y"] = 0
    drag_data["start_x"] = 0
    drag_data["start_y"] = 0

def perform_drag(event):
    # Calculate the distance moved by the mouse
    dx = event.x_root - drag_data["start_x"]
    dy = event.y_root - drag_data["start_y"]
    # Move the window by the distance the mouse moved
    root.geometry(f"+{root.winfo_x() + dx}+{root.winfo_y() + dy}")
    # Update the start position with the new position
    drag_data["start_x"] = event.x_root
    drag_data["start_y"] = event.y_root

# Bind the mouse drag events to the handler functions
root.bind("<ButtonPress-1>", start_drag)
root.bind("<ButtonRelease-1>", end_drag)
root.bind_all("<B1-Motion>", perform_drag)

# Starts the GUI
root.mainloop()
