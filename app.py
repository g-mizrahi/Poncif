import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename
import cv2
import numpy as np
import logging
logging.basicConfig(level=logging.INFO)

class Poncif_design_tool(tk.Tk):
    def __init__(self, *args, **kwargs):
        # Parent class __init__
        tk.Tk.__init__(self, *args, **kwargs)

        # General variables init
        self.attributes("-fullscreen", True)
        self.bind('<Escape>', lambda event:self.close())
        # self.attributes("-zoomed", True)

        # Define the closing method
        # The closing method must implement the robot closing method
        self.protocol("WM_DELETE_WINDOW", self.close)

        # Title of the window
        self.title("✏️ Poncif Design Tool")

        # Default picture
        # TODO : change the default picture to a more explicit one
        self.default_image_path = "Poncif_Design_Tool.png"

        # Define the general layout
        # A grid of 2 columns x 6 rows
        self.content = ctk.CTkFrame(self)
        self.content.pack(side="top", fill="both", expand=True)
        self.content.columnconfigure(0, weight=8)
        self.content.columnconfigure(1, weight=1)
        self.content.rowconfigure(0, weight=1)
        self.content.rowconfigure(1, weight=1)
        self.content.rowconfigure(2, weight=1)
        self.content.rowconfigure(3, weight=1)
        self.content.rowconfigure(4, weight=1)
        self.content.rowconfigure(5, weight=1)

        # Define button to load an image
        load_image_button = ctk.CTkButton(master=self.content, text="Choose an image", border_width=2, command=self.load_image).grid(column=1, row=0, sticky="nsew")

        self.select_canny_frame = ctk.CTkFrame(master=self.content)
        self.select_canny_frame.grid(column=1, row=1, sticky="nsew")

        self.select_canny_frame.rowconfigure(0, weight=1)
        self.select_canny_frame.rowconfigure(1, weight=2)
        self.select_canny_frame.rowconfigure(2, weight=2)
        self.select_canny_frame.columnconfigure(0, weight=1)
        self.select_canny_frame.columnconfigure(1, weight=2)
        self.select_canny_frame.columnconfigure(2, weight=1)

        self.select_canny_frame_title = ctk.CTkLabel(master=self.select_canny_frame, text="Select threshold values")
        self.select_canny_frame_title.grid(column=0, row=0, columnspan=3, sticky="ns")

        self.canny_low_threshold = tk.IntVar()
        self.canny_low_threshold.set(120)
        self.canny_high_threshold = tk.IntVar()
        self.canny_high_threshold.set(200)

        self.select_canny_frame_low_threshold_label = ctk.CTkLabel(master=self.select_canny_frame, text="Low threshold")
        self.select_canny_frame_low_threshold_label.grid(column=0, row=1, sticky="nsew")

        self.select_canny_frame_low_threshold_slider = ctk.CTkSlider(master=self.select_canny_frame, from_=0, to=300, number_of_steps=30, variable=self.canny_low_threshold, command=self.compute_canny_contours)
        self.select_canny_frame_low_threshold_slider.grid(column=1, row=1, sticky="ew")

        self.select_canny_frame_low_threshold_display = ctk.CTkEntry(master=self.select_canny_frame, placeholder_text=self.canny_low_threshold.get(), textvariable=self.canny_low_threshold)
        self.select_canny_frame_low_threshold_display.grid(column=2, row=1, sticky="ew")

        self.select_canny_frame_high_threshold_label = ctk.CTkLabel(master=self.select_canny_frame, text="High threshold")
        self.select_canny_frame_high_threshold_label.grid(column=0, row=2, sticky="nsew")

        self.select_canny_frame_high_threshold_slider = ctk.CTkSlider(master=self.select_canny_frame, from_=0, to=300, number_of_steps=30, variable=self.canny_high_threshold, command=self.compute_canny_contours)
        self.select_canny_frame_high_threshold_slider.grid(column=1, row=2, sticky="ew")
        self.select_canny_frame_high_threshold_display = ctk.CTkEntry(master=self.select_canny_frame, placeholder_text=self.canny_high_threshold.get(), textvariable=self.canny_high_threshold)
        self.select_canny_frame_high_threshold_display.grid(column=2, row=2, sticky="ew")

        self.select_tool_frame = ctk.CTkFrame(master=self.content)
        self.select_tool_frame.grid(column=1, row=2, sticky="nsew")

        self.select_tool_frame.rowconfigure(0, weight=1)
        self.select_tool_frame.rowconfigure(1, weight=1)
        self.select_tool_frame.columnconfigure(0, weight=1)
        self.select_tool_frame.columnconfigure(1, weight=1)

        self.select_tool_title = ctk.CTkLabel(master=self.select_tool_frame, text="Select tool")
        self.select_tool_title.grid(column=0, row=0, columnspan=2, sticky="nsew")

        self.tool_var = tk.IntVar()
        self.tool_var.set(0)

        self.img1 = tk.PhotoImage(file="pencil-svgrepo-com.png")
        self.img2 = tk.PhotoImage(file="eraser-svgrepo-com.png")
        self.select_tool_radio_1 = tk.Radiobutton(master=self.select_tool_frame, text="Draw", variable=self.tool_var, value=0, image=self.img1, command=self.select_tool) 
        self.select_tool_radio_1.grid(column=0, row=1, sticky="nsew")
        self.select_tool_radio_2 = tk.Radiobutton(master=self.select_tool_frame, text="Erase", variable=self.tool_var, value=1, image=self.img2, command=self.select_tool)
        self.select_tool_radio_2.grid(column=1, row=1, sticky="nsew")

        self.select_resolution_frame = ctk.CTkFrame(master=self.content)
        self.select_resolution_frame.grid(column=1, row=3, sticky="nsew")
        self.select_resolution_frame.rowconfigure(0, weight=1)
        self.select_resolution_frame.rowconfigure(1, weight=1)
        self.select_resolution_frame.columnconfigure(0, weight=1)
        self.select_resolution_frame.columnconfigure(1, weight=1)
        self.select_resolution_frame.columnconfigure(2, weight=1)
        self.select_resolution_title = ctk.CTkLabel(master=self.select_resolution_frame, text="Select resolution")
        self.select_resolution_title.grid(column=0, row=0, columnspan=3, sticky="nsew")
        self.resolution = tk.IntVar()
        self.resolution.set(1)
        self.select_resolution_label = ctk.CTkLabel(master=self.select_resolution_frame, text="Space between holes")
        self.select_resolution_label.grid(column=0, row=1, sticky="nsew")
        self.select_resolution_slider = ctk.CTkSlider(master=self.select_resolution_frame, from_=1, to=3, number_of_steps=2, variable=self.resolution, command=self.select_resolution)
        self.select_resolution_slider.grid(column=1, row=1, sticky="ew")
        self.select_resolution_display = ctk.CTkEntry(master=self.select_resolution_frame, placeholder_text=self.resolution.get(), textvariable=self.resolution)
        self.select_resolution_display.grid(column=2, row=1, sticky="ew")

        self.select_tile_dimension_frame = ctk.CTkFrame(master=self.content)
        self.select_tile_dimension_frame.grid(column=1, row=4, sticky="nsew")
        self.select_tile_dimension_frame.rowconfigure(0, weight=1)
        self.select_tile_dimension_frame.rowconfigure(1, weight=1)
        self.select_tile_dimension_frame.rowconfigure(2, weight=1)
        self.select_tile_dimension_frame.columnconfigure(0, weight=1)
        self.select_tile_dimension_frame.columnconfigure(1, weight=1)

        self.select_tile_dimension_title = ctk.CTkLabel(master=self.select_tile_dimension_frame, text="Select tile dimensions")
        self.select_tile_dimension_title.grid(column=0, row=0, columnspan=2, sticky="nsew")
        self.select_tile_dimension_width_label = ctk.CTkLabel(master=self.select_tile_dimension_frame, text="Width (mm)")
        self.select_tile_dimension_width_label.grid(column=0, row=1, sticky="nsew")
        self.select_tile_dimension_height_label = ctk.CTkLabel(master=self.select_tile_dimension_frame, text="Height (mm)")
        self.select_tile_dimension_height_label.grid(column=0, row=2, sticky="nsew")
        self.width = tk.IntVar()
        self.height = tk.IntVar()
        self.width.set(200)
        self.height.set(200)
        self.select_tile_dimension_width_entry = ctk.CTkEntry(master=self.select_tile_dimension_frame, placeholder_text=self.width.get(), textvariable=self.width)
        self.select_tile_dimension_width_entry.grid(column=1, row=1, sticky="ew")
        self.select_tile_dimension_height_entry = ctk.CTkEntry(master=self.select_tile_dimension_frame, placeholder_text=self.height.get(), textvariable=self.height)
        self.select_tile_dimension_height_entry.grid(column=1, row=2, sticky="ew")

        self.start_button = ctk.CTkButton(master=self.content, text="Start", command=self.start)
        self.start_button.grid(column=1, row=5, sticky="nsew")

        self.image_canvas = tk.Canvas(self.content, bg="lightgrey")
        self.image_canvas.grid(column=0, row=0, rowspan=6, sticky="nsew")
        self.content.update()

        self.pil_poncif_image = Image.open(self.image_path)
        self.target_size = get_target_size(self.pil_poncif_image.size, (self.image_canvas.winfo_width(), self.image_canvas.winfo_height()))
        self.pil_poncif_image = self.pil_poncif_image.resize(self.target_size, Image.Resampling.LANCZOS)

        logging.info(f"Canvas dimensions : {self.image_canvas.winfo_width()}x{self.image_canvas.winfo_height()}")
        logging.info(f"Image dimensions : {self.pil_poncif_image.size[0]}x{self.pil_poncif_image.size[1]}")
        self.poncif_image = ImageTk.PhotoImage(self.pil_poncif_image)

        self.image_container = self.image_canvas.create_image(0, 0, image=self.poncif_image, anchor="nw")

    def start(self):
        logging.info(f"Start")

    def select_resolution(self, value):
        logging.info(f"Resolution parameter : {value}")

    def compute_canny_contours(self, value):
        logging.info(f"Canny parameters : {value}")
        self.image_canvas.delete("contours")
        self.contours = get_contours(self.pil_poncif_image, self.canny_low_threshold.get(), self.canny_high_threshold.get(), sampling=10)
        self.contours = prune_contours(self.contours, min_dist=10)
        for path in self.contours:
            _ = input("Next contour ?")
            for point in path:
                self.image_canvas.create_oval(point[0]-2, point[1]-2, point[0]+2, point[1]+2, fill="red", outline="red", tags="contours")

    def select_tool(self):
        logging.info(f"Selected tool : {self.tool_var.get()}")

    def close(self):
        logging.info(f"Closing")
        self.destroy()

    def load_image(self):
        logging.info(f"Loading image")
        self.image_path = askopenfilename(title="Choose a file", filetypes=[('png files', '.png'), ('all files', '.*')])
        self.image_canvas = tk.Canvas(self.content, bg="lightgrey")
        self.image_canvas.grid(column=0, row=0, rowspan=6, sticky="nsew")
        self.content.update()

        self.pil_poncif_image = Image.open(self.image_path)
        self.target_size = get_target_size(self.pil_poncif_image.size, (self.image_canvas.winfo_width(), self.image_canvas.winfo_height()))
        self.pil_poncif_image = self.pil_poncif_image.resize(self.target_size, Image.Resampling.LANCZOS)

        logging.info(f"Canvas dimensions : {self.image_canvas.winfo_width()}x{self.image_canvas.winfo_height()}")
        logging.info(f"Image dimensions : {self.pil_poncif_image.size[0]}x{self.pil_poncif_image.size[1]}")
        self.poncif_image = ImageTk.PhotoImage(self.pil_poncif_image)

        self.image_container = self.image_canvas.create_image(0, 0, image=self.poncif_image, anchor="nw")
        self.compute_canny_contours(0)

def get_target_size(size, container_size):
    ratio = min(container_size[0]/size[0], container_size[1]/size[1])
    target_size = [int(size[0] * ratio), int(size[1] * ratio)]
    return(target_size)

def get_contours(image, low_threshold=300, high_threshold=400, sampling=100):
    print(f"Computing contour with {low_threshold = } and {high_threshold = }")
    img_array = np.array(image)
    img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    canny = cv2.Canny(img, low_threshold, high_threshold, edges=True, L2gradient=True)
    contours, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    points = [[contour[i][0] for i in range(0, len(contour), sampling)] for contour in contours]
    print(len(contours))
    return(points)

def prune_contours(contours, min_dist=10):
    """
    remove points too close to other contours
    """
    mmc = []
    for contour in contours:
        min_coor_x = min([p[0] for p in contour])
        max_coor_x = max([p[0] for p in contour])
        min_coor_y = min([p[1] for p in contour])
        max_coor_y = max([p[1] for p in contour])
        mmc.append([min_coor_x, max_coor_x, min_coor_y, max_coor_y])
    for i in range(len(contours)):
        for j in range(i):
            if mmc[i][0]>=(mmc[j][1] - min_dist) or mmc[j][0]>=(mmc[i][1] - min_dist) or mmc[i][2]>=(mmc[j][3] - min_dist) or mmc[j][2]>=(mmc[i][3] - min_dist):
                continue
            else:
                new_contour = []
                for p in contours[i]:
                    try:
                        test = min([distance(*p, *q) for q in contours[j]])
                        if test > min_dist:
                            new_contour.append(p)
                        else:
                            print("too close")
                    except:
                        pass
                contours[i] = new_contour
    return(contours)

def get_contours_dict(image, low_threshold = 300, high_threshold = 400, scale=1, sampling=1):
    contours = get_contours(image, low_threshold, high_threshold)
    contours_dict = {i:[(contours[i][j][0]*scale).tolist() for j in range(0, len(contours[i]), sampling)] for i in range(len(contours))}
    return(contours_dict)

def distance(a, b, c, d):
    return(pow((a-c)**2 + (b-d)**2, 0.5))

app = Poncif_design_tool()

app.mainloop()