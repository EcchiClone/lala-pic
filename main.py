from tkinter import Tk, Canvas, NW, filedialog
from PIL import Image, ImageTk
from pynput import keyboard

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.*')])
    return file_path

def start_lala_display():
    root = Tk()

    root.overrideredirect(True)
    root.attributes('-transparentcolor', '#f0f0f0')  # Set the transparent color

    img_path = open_image()
    original_pil_img = Image.open(img_path).convert("RGBA")  # Convert image to RGBA for transparency

    img = ImageTk.PhotoImage(original_pil_img)

    global resized_photoimg
    resized_photoimg = img

    global zoom_level
    zoom_level = 1.0

    canvas = Canvas(root, width=img.width(), height=img.height(), bg="#f0f0f0")  # Set the canvas background to the same transparent color
    canvas.pack()

    image_id = canvas.create_image(0, 0, anchor=NW, image=img)

    def zoom_image(event):
        global zoom_level, resized_photoimg
        if event.delta > 0:
            zoom_level *= 1.1  # Increase the zoom level by 10%
        else:
            zoom_level *= 0.9  # Decrease the zoom level by 10%
        x, y = original_pil_img.size
        x, y = int(x * zoom_level), int(y * zoom_level)
        resized_img = original_pil_img.resize((x, y), Image.Resampling.NEAREST)
        resized_photoimg = ImageTk.PhotoImage(resized_img)
        canvas.itemconfig(image_id, image=resized_photoimg)
        canvas.config(width=x, height=y)

        # Calculate the ratios of the mouse pointer to the left and top edges of the image
        x_ratio = event.x / canvas.winfo_width()
        y_ratio = event.y / canvas.winfo_height()

        # Calculate the new position of the window
        new_x = root.winfo_x() + (event.x - x_ratio * x)
        new_y = root.winfo_y() + (event.y - y_ratio * y)

        # Move the window to the new position
        root.geometry(f"+{int(new_x)}+{int(new_y)}")

    root.bind("<MouseWheel>", zoom_image)

    drag_data = {"x": 0, "y": 0, "start_x": 0, "start_y": 0}

    def start_drag(event):
        drag_data["start_x"] = event.x_root
        drag_data["start_y"] = event.y_root

    def end_drag(event):
        drag_data["x"] = 0
        drag_data["y"] = 0
        drag_data["start_x"] = 0
        drag_data["start_y"] = 0

    def perform_drag(event):
        dx = event.x_root - drag_data["start_x"]
        dy = event.y_root - drag_data["start_y"]
        root.geometry(f"+{root.winfo_x() + dx}+{root.winfo_y() + dy}")
        drag_data["start_x"] = event.x_root
        drag_data["start_y"] = event.y_root

    root.bind("<ButtonPress-1>", start_drag)
    root.bind("<ButtonRelease-1>", end_drag)
    root.bind_all("<B1-Motion>", perform_drag)

    # Set the focus to the window
    root.focus_set()

    # Create a new keyboard listener
    listener = keyboard.Listener(on_release=lambda k: root.destroy() if k == keyboard.Key.esc else None)
    listener.start()

    root.mainloop()

start_lala_display()
