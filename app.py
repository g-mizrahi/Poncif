import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename
import cv2
import numpy as np
import logging
from copy import deepcopy
from pyaxidraw import axidraw  
logging.basicConfig(level=logging.INFO)

class Poncif_design_tool(tk.Tk):
    def __init__(self, *args, **kwargs):
        # Parent class __init__
        tk.Tk.__init__(self, *args, **kwargs)

        # General variables init
        # self.attributes("-fullscreen", True)
        self.bind('<Escape>', lambda event:self.close())
        self.attributes("-zoomed", True)

        # Define the closing method
        # The closing method must implement the robot closing method
        self.protocol("WM_DELETE_WINDOW", self.close)

        # Title of the window
        self.title("✏️ Poncif Design Tool")

        # Default picture
        # TODO : change the default picture to a more explicit one
        default_image_path = "Poncif_Design_Tool.png"

        # Define the general layout
        # A grid of 2 columns x 6 rows
        # content needs to be a class attribute to make it easier to update
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
        ctk.CTkButton(master=self.content, text="Choose an image", border_width=2, command=self.load_image).grid(column=1, row=0, sticky="nsew")

        # Define the widget to choose canny parameters
        canny_frame = ctk.CTkFrame(master=self.content)
        canny_frame.grid(column=1, row=1, sticky="nsew")
        canny_frame.rowconfigure(0, weight=1)
        canny_frame.rowconfigure(1, weight=2)
        canny_frame.rowconfigure(2, weight=2)
        canny_frame.columnconfigure(0, weight=1)
        canny_frame.columnconfigure(1, weight=2)
        canny_frame.columnconfigure(2, weight=1)
        # Define the title label for the canny widget
        ctk.CTkLabel(master=canny_frame, text="Select threshold values").grid(column=0, row=0, columnspan=3, sticky="ns")
        # Define the variables to hold the canny thresholds
        self.canny_low_threshold = tk.IntVar()
        self.canny_low_threshold.set(120)
        self.canny_high_threshold = tk.IntVar()
        self.canny_high_threshold.set(200)
        # Define the canny low threshold label
        ctk.CTkLabel(master=canny_frame, text="Low threshold").grid(column=0, row=1, sticky="nsew")
        # Canny low threshold slider
        # updates the low threshold variable
        ctk.CTkSlider(master=canny_frame, from_=0, to=300, number_of_steps=30, variable=self.canny_low_threshold, command=lambda x: self.compute_canny_contours()).grid(column=1, row=1, sticky="ew")
        # Canny low threshold display
        ctk.CTkEntry(master=canny_frame, placeholder_text=self.canny_low_threshold.get(), textvariable=self.canny_low_threshold).grid(column=2, row=1, sticky="ew")
        # Define the canny high threshold label
        ctk.CTkLabel(master=canny_frame, text="High threshold").grid(column=0, row=2, sticky="nsew")
        # Canny high threshold slider
        # updates the high threshold variable
        ctk.CTkSlider(master=canny_frame, from_=0, to=300, number_of_steps=30, variable=self.canny_high_threshold, command=lambda x: self.compute_canny_contours()).grid(column=1, row=2, sticky="ew")
        ctk.CTkEntry(master=canny_frame, placeholder_text=self.canny_high_threshold.get(), textvariable=self.canny_high_threshold).grid(column=2, row=2, sticky="ew")

        # Define the widget to select the tool (pen/eraser)
        self.clicked = False
        tool_frame = ctk.CTkFrame(master=self.content)
        tool_frame.grid(column=1, row=2, sticky="nsew")
        tool_frame.rowconfigure(0, weight=1)
        tool_frame.rowconfigure(1, weight=1)
        tool_frame.columnconfigure(0, weight=1)
        tool_frame.columnconfigure(1, weight=1)
        # Define the widget title
        ctk.CTkLabel(master=tool_frame, text="Select tool").grid(column=0, row=0, columnspan=2, sticky="nsew")
        # Define the tool variable
        self.tool_var = tk.IntVar()
        self.tool_var.set(0)
        # Include the images for the tools
        self.pen_img = tk.PhotoImage(file="pencil-svgrepo-com.png")
        self.eraser_img = tk.PhotoImage(file="eraser-svgrepo-com.png")
        # Define the radiobuttons to select the tool
        tk.Radiobutton(master=tool_frame, text="Draw", variable=self.tool_var, value=0, image=self.pen_img, command=self.select_tool).grid(column=0, row=1, sticky="nsew")
        tk.Radiobutton(master=tool_frame, text="Erase", variable=self.tool_var, value=1, image=self.eraser_img, command=self.select_tool).grid(column=1, row=1, sticky="nsew")

        # Define the widget to select the resolution
        resolution_frame = ctk.CTkFrame(master=self.content)
        resolution_frame.grid(column=1, row=3, sticky="nsew")
        resolution_frame.rowconfigure(0, weight=1)
        resolution_frame.rowconfigure(1, weight=1)
        resolution_frame.columnconfigure(0, weight=1)
        resolution_frame.columnconfigure(1, weight=1)
        resolution_frame.columnconfigure(2, weight=1)
        # Define the widget title
        ctk.CTkLabel(master=resolution_frame, text="Select resolution").grid(column=0, row=0, columnspan=3, sticky="nsew")
        # Define the resolution variable
        self.resolution = tk.IntVar()
        self.resolution.set(1)

        ctk.CTkLabel(master=resolution_frame, text="Space between holes").grid(column=0, row=1, sticky="nsew")
        ctk.CTkSlider(master=resolution_frame, from_=1, to=3, number_of_steps=2, variable=self.resolution, command=self.select_resolution).grid(column=1, row=1, sticky="ew")
        ctk.CTkEntry(master=resolution_frame, placeholder_text=self.resolution.get(), textvariable=self.resolution).grid(column=2, row=1, sticky="ew")

        # Define the widget to specify the tile dimensions
        tile_dimension_frame = ctk.CTkFrame(master=self.content)
        tile_dimension_frame.grid(column=1, row=4, sticky="nsew")
        tile_dimension_frame.rowconfigure(0, weight=1)
        tile_dimension_frame.rowconfigure(1, weight=1)
        tile_dimension_frame.rowconfigure(2, weight=1)
        tile_dimension_frame.columnconfigure(0, weight=1)
        tile_dimension_frame.columnconfigure(1, weight=1)
        # Define widget title
        ctk.CTkLabel(master=tile_dimension_frame, text="Select tile dimensions").grid(column=0, row=0, columnspan=2, sticky="nsew")
        ctk.CTkLabel(master=tile_dimension_frame, text="Width (mm)").grid(column=0, row=1, sticky="nsew")
        ctk.CTkLabel(master=tile_dimension_frame, text="Height (mm)").grid(column=0, row=2, sticky="nsew")
        # Define the dimension variables
        self.width = tk.IntVar()
        self.height = tk.IntVar()
        self.width.set(200)
        self.height.set(200)
        # Define the dimension entry fields
        ctk.CTkEntry(master=tile_dimension_frame, placeholder_text=self.width.get(), textvariable=self.width).grid(column=1, row=1, sticky="ew")
        ctk.CTkEntry(master=tile_dimension_frame, placeholder_text=self.height.get(), textvariable=self.height).grid(column=1, row=2, sticky="ew")

        # Define the start button widget
        ctk.CTkButton(master=self.content, text="Start", command=self.start).grid(column=1, row=5, sticky="nsew")

        # Define the image canvas to hold the image and the contours
        logging.info(f"Loading default image")
        self.image_canvas = tk.Canvas(self.content, bg="lightgrey")
        self.image_canvas.grid(column=0, row=0, rowspan=6, sticky="nsew")
        self.pil_poncif_image = Image.open(default_image_path)
        self.poncif_image = ImageTk.PhotoImage(self.pil_poncif_image)
        self.image_canvas.create_image(0, 0, image=self.poncif_image, anchor="nw", tags="image")

        self.drawing_coordinates = None
        self.image_canvas.bind('<Motion>', self.draw)
        self.image_canvas.bind('<ButtonPress-1>', self.click)
        self.image_canvas.bind('<ButtonRelease-1>', self.release)
    
    def draw(self, event):
        if self.clicked:
            if self.tool_var.get() == 0:
                # Pen mode
                # try:
                if self.drawing_coordinates:
                    self.drawing_distance += distance(self.drawing_coordinates, [event.x, event.y])
                    # coordinates exist
                    if self.drawing_distance > 10:
                        self.image_canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, width=2, tags="contours", outline="red", fill="red")
                        self.drawing_distance = 0
                    self.drawing_coordinates = [event.x, event.y]
                else:
                    logging.info(f"Failed drawing")
                    self.drawing_coordinates = [event.x, event.y]
            elif self.tool_var.get() == 1:
                # Eraser mode
                # if self.drawing_coordinates:
                    # coordinates exist
                    # print(self.image_canvas.find_overlapping(event.x - 5, event.y - 5, event.x + 5, event.y +5))
                for contour in self.image_canvas.find_overlapping(event.x - 5, event.y - 5, event.x + 5, event.y +5):
                    if "contours" in self.image_canvas.gettags(contour):
                        self.image_canvas.delete(contour)
                # else:
                #     logging.info(f"Failed erasing")
                #     self.drawing_coordinates = [event.x, event.y]
            else:
                logging.info(f"Invalid tool")
        else:
            pass

    def click(self, _):
        self.clicked = True
        self.drawing_distance = 0
    
    def release(self, _):
        self.clicked = False
        self.drawing_coordinates = None
        self.drawing_distance = 0

    def start(self):
        self.ad = axidraw.AxiDraw()
        self.ad.interactive()
        connected = self.ad.connect()
        self.ad.options.units = 2
        self.ad.update() 
        if not connected:
            print(f"Not connected")
        for i in self.image_canvas.find_withtag("contours"):
            coords = self.image_canvas.coords(i)
            # Find the coordinates in real mm values
            print(f"Target size {self.target_size}")
            point = ((coords[0]+2)*self.width.get()/self.target_size[0], (coords[1]+2)*self.height.get()/self.target_size[1])
            self.ad.goto(*point)
            self.ad.pendown()
            self.ad.penup()
            # Pierce hole
        logging.info(f"Start drilling the holes")

    def load_image(self):
        logging.info(f"Load image button pressed")
        image_path = askopenfilename(title="Select an image", filetypes=[('png files', '.png'), ('all files', '.*')])
        logging.info(f"Remove previous image and contours")
        self.image_canvas.delete("all")

        self.pil_poncif_image = Image.open(image_path)
        self.target_size = get_target_size(self.pil_poncif_image.size, (self.image_canvas.winfo_width(), self.image_canvas.winfo_height()))
        self.pil_poncif_image = self.pil_poncif_image.resize(self.target_size, Image.Resampling.LANCZOS)

        logging.info(f"Canvas dimensions : {self.image_canvas.winfo_width()}x{self.image_canvas.winfo_height()}")
        logging.info(f"Image dimensions : {self.pil_poncif_image.size[0]}x{self.pil_poncif_image.size[1]}")
        self.poncif_image = ImageTk.PhotoImage(self.pil_poncif_image)

        self.image_canvas.create_image(0, 0, image=self.poncif_image, anchor="nw", tags="image")
        self.compute_canny_contours()

    def select_resolution(self, value):
        logging.info(f"Resolution parameter : {value}")

    def compute_canny_contours(self):
        logging.info(f"Canny parameters : {self.canny_low_threshold.get()}, {self.canny_high_threshold.get()}")
        self.image_canvas.delete("contours")
        contours = get_contours_points(self.pil_poncif_image, self.canny_low_threshold.get(), self.canny_high_threshold.get(), sampling=20)
        contours = prune_contours(contours, min_dist=10)
        for path in contours:
            # For every path read the points coordinates
            # _ = input("Next contour ?")
            for point in path:
                # For every point draw a circl of size 4
                self.image_canvas.create_oval(point[0]-2, point[1]-2, point[0]+2, point[1]+2, fill="red", outline="red", tags="contours")

    def select_tool(self):
        logging.info(f"Selected tool : {self.tool_var.get()}")

    def close(self):
        try:
            self.ad.disconnect()
        except:
            pass
        logging.info(f"Closing")
        self.destroy()

def get_target_size(size, container_size):
    ratio = min(container_size[0]/size[0], container_size[1]/size[1])
    target_size = [int(size[0] * ratio), int(size[1] * ratio)]
    return(target_size)

def get_contours_points(image, low_threshold=300, high_threshold=400, sampling=100):
    canny = cv2.Canny(cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR), low_threshold, high_threshold, edges=True, L2gradient=True)
    contours, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # TODO : make a better sampling using the distance
    # IDEA : The sampling using distance will be made during the piercing (better time control)
    # sampled_contours = []
    # for contour in contours:
    #     sampled_contour = [contour[0][0]]
    #     local_distance = 0
    #     for i in range(1, len(contour) - 1):
    #         local_distance += distance(contour[i][0], contour[i-1][0])
    #         if local_distance < sampling :
    #             continue
    #         else:
    #             sampled_contour.append(contour[i][0])
    #             local_distance = 0
    #     sampled_contours.append(sampled_contour)
    # return(sampled_contours)
    return([[contour[i][0] for i in range(0, len(contour), sampling)] for contour in contours])

def prune_contours(contours, min_dist=10):
    """
    remove points too close to other contours
    """
    # Compute the general location of each path
    mmc = [[min([p[0] for p in path]), max([p[0] for p in path]), min([p[1] for p in path]), max([p[1] for p in path])] for path in contours]

    for i in range(len(contours)):
        # for each path the goal is to find the points too close to points of previous paths
        # print(f"{i}")
        for j in range(i):
            # print(f"  {j}")
            # for all previous paths
            # check if the paths collide
            if not too_close(mmc[i], mmc[j], min_dist):
                # print(f"Don't collide {i}, {j}")
                continue
            else:
                # print(f"Collide {i}, {j}")
                # find the points that collide
                temp = deepcopy(contours[i])
                for k in range(len(contours[i])-1, -1, -1):
                    # for every point check if there is a colliding point
                    # the list has to be traversed in the oppsite direction to not mess with the indices when pop
                    for p in contours[j]:
                        # print(f"checking points {contours[i][len(contours[i])-1-k]} and {p}")
                        # print(f"{distance(contours[i][len(contours[i])-1-k], p)}")
                        if distance(contours[i][k], p)<=min_dist:
                            # print(f"Found colliding point at index {k} of {len(contours[i])}")
                            temp.pop(k)
                            break
                contours[i] = temp
    return(contours)

def distance(p1, p2):
    return(pow((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2, 0.5))

def too_close(a, b, min_dist=10):
    if b[0] - a[1] > min_dist:
        return(False)
    elif a[0] - b[1] > min_dist:
        return(False)
    elif a[2] - b[3] > min_dist:
        return(False)
    elif b[2] - a[3] > min_dist:
        return(False)
    else:
        return(True)

app = Poncif_design_tool()

app.mainloop()