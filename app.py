import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename

import logging
logging.basicConfig(level=logging.INFO)

class Poncif_design_tool(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.attributes("-zoomed", True)
        self.protocol("WM_DELETE_WINDOW", self.close)

    def close(self):
        logging.info(f"Closing")
        self.destroy()

def load_image():
    logging.info(f"Loading image")

def get_target_size(size, container_size):
    ratio = min(container_size[0]/size[0], container_size[1]/size[1])
    target_size = [int(size[0] * ratio), int(size[1] * ratio)]
    return(target_size)

app = Poncif_design_tool()
app.title("✏️ Poncif Design Tool")

content = tk.ttk.Frame(app)
content.pack(side="top", fill="both", expand=True)
content.columnconfigure(0, weight=8)
content.columnconfigure(1, weight=1)
content.rowconfigure(0, weight=1)
content.rowconfigure(1, weight=1)
content.rowconfigure(2, weight=1)
content.rowconfigure(3, weight=1)
content.rowconfigure(4, weight=1)
content.rowconfigure(5, weight=1)

# CHOOSE IMAGE AREA

load_image_button = ctk.CTkButton(master=content, text="Choose an image", border_width=5, corner_radius=1, command=load_image)
load_image_button.grid(column=1, row=0, sticky="nsew", padx=(10, 10))

# SELECT CANNY PARAMETERS AREA

select_canny_frame = ctk.CTkFrame(master=content)
select_canny_frame.grid(column=1, row=1, sticky="nsew")

select_canny_frame.rowconfigure(0, weight=1)
select_canny_frame.rowconfigure(1, weight=2)
select_canny_frame.rowconfigure(2, weight=2)
select_canny_frame.columnconfigure(0, weight=1)
select_canny_frame.columnconfigure(1, weight=2)
select_canny_frame.columnconfigure(2, weight=1)

select_canny_frame_title = ctk.CTkLabel(master=select_canny_frame, text="Select threshold values")
select_canny_frame_title.grid(column=0, row=0, columnspan=3, sticky="ns")

canny_low_threshold = tk.IntVar()
canny_low_threshold.set(120)
canny_high_threshold = tk.IntVar()
canny_high_threshold.set(200)

select_canny_frame_low_threshold_label = ctk.CTkLabel(master=select_canny_frame, text="Low threshold")
select_canny_frame_low_threshold_label.grid(column=0, row=1, sticky="nsew")

select_canny_frame_low_threshold_slider = ctk.CTkSlider(master=select_canny_frame, from_=0, to=300, number_of_steps=30, variable=canny_low_threshold, command=None)
select_canny_frame_low_threshold_slider.grid(column=1, row=1, sticky="ew")

select_canny_frame_low_threshold_display = ctk.CTkEntry(master=select_canny_frame, placeholder_text=canny_low_threshold.get(), textvariable=canny_low_threshold)
select_canny_frame_low_threshold_display.grid(column=2, row=1, sticky="ew")

select_canny_frame_high_threshold_label = ctk.CTkLabel(master=select_canny_frame, text="High threshold")
select_canny_frame_high_threshold_label.grid(column=0, row=2, sticky="nsew")

select_canny_frame_high_threshold_slider = ctk.CTkSlider(master=select_canny_frame, from_=0, to=300, number_of_steps=30, variable=canny_high_threshold, command=None)
select_canny_frame_high_threshold_slider.grid(column=1, row=2, sticky="ew")
select_canny_frame_high_threshold_display = ctk.CTkEntry(master=select_canny_frame, placeholder_text=canny_high_threshold.get(), textvariable=canny_high_threshold)
select_canny_frame_high_threshold_display.grid(column=2, row=2, sticky="ew")

# SELECT TOOL AREA

select_tool_frame = ctk.CTkFrame(master=content)
select_tool_frame.grid(column=1, row=2, sticky="nsew")

select_tool_frame.rowconfigure(0, weight=1)
select_tool_frame.rowconfigure(1, weight=1)
select_tool_frame.columnconfigure(0, weight=1)
select_tool_frame.columnconfigure(1, weight=1)

select_tool_title = ctk.CTkLabel(master=select_tool_frame, text="Select tool")
select_tool_title.grid(column=0, row=0, columnspan=2, sticky="nsew")

tool_var = tk.IntVar()
tool_var.set(0)

img1 = tk.PhotoImage(file="pencil-svgrepo-com.png")
img2 = tk.PhotoImage(file="eraser-svgrepo-com.png")
select_tool_radio_1 = tk.Radiobutton(master=select_tool_frame, text="Draw", variable=tool_var, value=0, image=img1) 
select_tool_radio_1.grid(column=0, row=1, sticky="nsew")
select_tool_radio_2 = tk.Radiobutton(master=select_tool_frame, text="Erase", variable=tool_var, value=1, image=img2)
select_tool_radio_2.grid(column=1, row=1, sticky="nsew")

# SELECT RESOLUTION AREA

select_resolution_frame = ctk.CTkFrame(master=content)
select_resolution_frame.grid(column=1, row=3, sticky="nsew")
select_resolution_frame.rowconfigure(0, weight=1)
select_resolution_frame.rowconfigure(1, weight=1)
select_resolution_frame.columnconfigure(0, weight=1)
select_resolution_frame.columnconfigure(1, weight=1)
select_resolution_frame.columnconfigure(2, weight=1)
select_resolution_title = ctk.CTkLabel(master=select_resolution_frame, text="Select resolution")
select_resolution_title.grid(column=0, row=0, columnspan=3, sticky="nsew")
resolution = tk.IntVar()
resolution.set(1)
select_resolution_label = ctk.CTkLabel(master=select_resolution_frame, text="Space between holes")
select_resolution_label.grid(column=0, row=1, sticky="nsew")
select_resolution_slider = ctk.CTkSlider(master=select_resolution_frame, from_=1, to=3, number_of_steps=2, variable=resolution, command=None)
select_resolution_slider.grid(column=1, row=1, sticky="ew")
select_resolution_display = ctk.CTkEntry(master=select_resolution_frame, placeholder_text=resolution.get(), textvariable=resolution)
select_resolution_display.grid(column=2, row=1, sticky="ew")

# SELECT TILE DIMENSIONS AREA

select_tile_dimension_frame = ctk.CTkFrame(master=content)
select_tile_dimension_frame.grid(column=1, row=4, sticky="nsew")
select_tile_dimension_frame.rowconfigure(0, weight=1)
select_tile_dimension_frame.rowconfigure(1, weight=1)
select_tile_dimension_frame.rowconfigure(2, weight=1)
select_tile_dimension_frame.columnconfigure(0, weight=1)
select_tile_dimension_frame.columnconfigure(1, weight=1)

select_tile_dimension_title = ctk.CTkLabel(master=select_tile_dimension_frame, text="Select tile dimensions")
select_tile_dimension_title.grid(column=0, row=0, columnspan=2, sticky="nsew")
select_tile_dimension_width_label = ctk.CTkLabel(master=select_tile_dimension_frame, text="Width (mm)")
select_tile_dimension_width_label.grid(column=0, row=1, sticky="nsew")
select_tile_dimension_height_label = ctk.CTkLabel(master=select_tile_dimension_frame, text="Height (mm)")
select_tile_dimension_height_label.grid(column=0, row=2, sticky="nsew")
width = tk.IntVar()
height = tk.IntVar()
width.set(200)
height.set(200)
select_tile_dimension_width_entry = ctk.CTkEntry(master=select_tile_dimension_frame, placeholder_text=width.get(), textvariable=width)
select_tile_dimension_width_entry.grid(column=1, row=1, sticky="ew")
select_tile_dimension_height_entry = ctk.CTkEntry(master=select_tile_dimension_frame, placeholder_text=height.get(), textvariable=height)
select_tile_dimension_height_entry.grid(column=1, row=2, sticky="ew")

# START BUTTON

def start():
    logging.info(f"Start")

start_button = ctk.CTkButton(master=content, text="Start", command=start)
start_button.grid(column=1, row=5, sticky="nsew")

# CANVAS AREA

image_canvas = tk.Canvas(content, bg="red")
image_canvas.grid(column=0, row=0, rowspan=6, sticky="nsew")
content.update()

# CREATE BACKGROUND IMAGE

poncif_image = Image.open("/home/user/Documents/Poncif/poncif/Poncif_Design_Tool.png")
target_size = get_target_size(poncif_image.size, (image_canvas.winfo_width(), image_canvas.winfo_height()))
poncif_image = poncif_image.resize(target_size, Image.Resampling.LANCZOS)

logging.info(f"Canvas dimensions : {image_canvas.winfo_width()}x{image_canvas.winfo_height()}")
logging.info(f"Image dimensions : {poncif_image.size[0]}x{poncif_image.size[1]}")
poncif_image = ImageTk.PhotoImage(poncif_image)

image_canvas.create_image(image_canvas.winfo_width()/2, image_canvas.winfo_height()/2,image=poncif_image, anchor="center")

app.mainloop()