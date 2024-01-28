# from tkinter import *
# #widgets=button.textbox,label,images
# #windows=container to hold objects
# print("None")
# window=Tk()
# photo=PhotoImage(file='ICM.png')
# window.geometry("800x600")
# window.title("ImaGini")
# label=Label(window,
#             text="Imagini",
#             font=('Arial',40,'bold'),
#             fg='green',
#             bg='black',
#             relief=RAISED,
#             bd=10,
#             padx=20,
#             pady=20,
#             image=photo,
#             compound='bottom')

# label.place(x=0,y=0)
# label.pack()
# #icon=PhotoImage(file='logo.png')
# #window.iconphoto(True,icon)
# window.config(background="#c38cd4")
# window.mainloop()

import tkinter as tk
from tkinter import filedialog,simpledialog, PhotoImage,ttk
from PIL import Image, ImageFilter, ImageTk,ImageEnhance,ImageOps,ImageDraw
import sys
# Define global variables
edited_image = None
edited_images = []
current_image_index = -1
canvas=None

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp *.ppm *.pgm")])
    if file_path:
        # Load and display the image
        global edited_image, edited_images, current_image_index
        edited_image = Image.open(file_path)
        edited_images = [edited_image.copy()]
        current_image_index = 0
        display_image(edited_image)
        print(f"Opened image: {file_path}")

def save_image():
    # Ask the user to select a file location to save the image
    if edited_image:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])

        # Check if the user canceled the file dialog
        if not file_path:
            return

        try:
            # Save the edited image to the selected file location
            edited_image.save(file_path)
            print("Image saved")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No image to save")
# Implement a simple login popup
def login_popup():
    
    username = simpledialog.askstring("Login", "Enter your username:")
    password = simpledialog.askstring("Login", "Enter your password:")

    # Check the username and password
    if username == "IITG" and password == "12345":
        # Continue with the application
        print("Login successful")
    else:
        # Close the application or show an error message
        print("Login failed")
        sys.exit(1)

def undo():
    global edited_image, edited_images, current_image_index

    if current_image_index > 0:
        current_image_index -= 1
        edited_image = edited_images[current_image_index]
        display_image(edited_image)
        print("Undo")
    else:
        print("No more actions to undo")

def redo():
    global edited_image, edited_images, current_image_index

    if current_image_index < len(edited_images) - 1:
        current_image_index += 1
        edited_image = edited_images[current_image_index]
        display_image(edited_image)
        print("Redo")
    else:
        print("No more actions to redo")

def display_image(image):
    global canvas
    #need to define a canvas as a global variable so you can update
    # it within the display_image function.
    if image:
        # Convert the PIL image to a Tkinter PhotoImage
        photo_image = ImageTk.PhotoImage(image)

        if canvas is not None:
            # Clear the previous canvas
            canvas.delete("all")

            # Display the new image on the canvas
            canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)
            canvas.image = photo_image  # Keep a reference to avoid garbage collection
    else:
        # Handle the case when there's no image
        print("No image to display")

###################################################
#######################################filters############
##################################
def apply_filter(filter_type):
    global edited_image, edited_images, current_image_index

    if edited_image:
        if filter_type == "Blur":
            edited_image = edited_image.filter(ImageFilter.BLUR)
        elif filter_type == "Contour":
            edited_image = edited_image.filter(ImageFilter.CONTOUR)
        elif filter_type == "Edge enhance":
            edited_image = edited_image.filter(ImageFilter.EDGE_ENHANCE)
        elif filter_type == "Edge enhance more":
            edited_image = edited_image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        elif filter_type == "Emboss":
            edited_image = edited_image.filter(ImageFilter.EMBOSS)
        elif filter_type == "Find edges":
            edited_image = edited_image.filter(ImageFilter.FIND_EDGES)
        elif filter_type == "Smooth":
            edited_image = edited_image.filter(ImageFilter.SMOOTH)
        elif filter_type == "Smooth more":
            edited_image = edited_image.filter(ImageFilter.SMOOTH_MORE)
        elif filter_type == "Sharpen":
            edited_image = edited_image.filter(ImageFilter.SHARPEN)
        elif filter_type == "Remove noise":
            edited_image = edited_image.filter(ImageFilter.SMOOTH_MORE)
        else:
            print("Unknown filter type")

        # Append the edited image to the list of edited images
        edited_images.append(edited_image.copy())
        current_image_index = len(edited_images) - 1

        # Display the edited image in the user interface
        display_image(edited_image)
        print(f"Applied {filter_type} filter")
    else:
        print("No image to apply filter to")



#####transform********#####################Function to rotate        
def rotate():
    global edited_image,edited_images,current_image_index
    if edited_image:
        edited_image=edited_image.transpose(Image.ROTATE_90)
        edited_images.append(edited_image.copy())
        current_image_index=len(edited_images)-1
        display_image(edited_image)
        print("Rotated 90 degrees clockwise")
    else:
        print('No image to rotate')    

def mirror():
    global edited_image,edited_images,current_image_index

    if edited_image:
        edited_image=edited_image.transpose(Image.FLIP_LEFT_RIGHT)
        edited_images.append(edited_image.copy())
        current_image_index=len(edited_images)-1
        display_image(edited_image)
        print("Mirrored horizontally")
    else:
        print("No image to mirror")   

def crop():
    global edited_image, edited_images, current_image_index
    if edited_image:
        # Create a temporary image for cropping
        cropped_image = edited_image.copy()

        # Create a cropping rectangle using the canvas
        cropping_rect = canvas.create_rectangle(0, 0, 0, 0, outline="red")
        cropping_rect_started = False
        x1, y1, x2, y2 = 0, 0, 0, 0  # Initialize these variables

        def start_crop(event):
            nonlocal cropping_rect_started, x1, y1
            cropping_rect_started = True
            x1, y1 = event.x, event.y
            canvas.coords(cropping_rect, x1, y1, x1, y1)

        def update_crop(event):
            nonlocal x2, y2
            if cropping_rect_started:
                x2, y2 = event.x, event.y
                canvas.coords(cropping_rect, x1, y1, x2, y2)

        def end_crop(event):
            nonlocal cropping_rect_started, x2, y2, cropped_image

            if cropping_rect_started:
                # Calculate the cropping region
                cropped_region = (x1, y1, x2, y2)
                
                # Crop the image based on the coordinates
                cropped_image = cropped_image.crop(cropped_region)

                # Append the edited image to the list of edited images
                # Increment the current_image_index and append the edited image
                
                edited_images.append(cropped_image.copy())
                

                # Display the cropped image
                display_image(cropped_image)
                print("Image cropped")
        current_image_index = len(edited_images)
        canvas.bind("<ButtonPress-1>", start_crop)
        canvas.bind("<B1-Motion>", update_crop)
        canvas.bind("<ButtonRelease-1>", end_crop)
    else:
        print("No image to crop")

# Function to perform the image resizing
index_of_image=current_image_index
def perform_resize():
    global edited_image, edited_images, current_image_index

    if edited_image:
        print("Resizing function called")
        # Create a popup window to get user input for new width and height
        popup = tk.Toplevel(app)
        popup.title("Resize Image")

        # Create Entry widgets for width and height input
        width_label = tk.Label(popup, text="Width (pixels):")
        width_entry = tk.Entry(popup)
        height_label = tk.Label(popup, text="Height (pixels):")
        height_entry = tk.Entry(popup)

        index_of_image = current_image_index  # Initialize index_of_image here

        def resize_action():
            nonlocal index_of_image  # Declare index_of_image as nonlocal
            edited_image = edited_images[index_of_image]  # Use the correct index
            new_width = int(width_entry.get())
            new_height = int(height_entry.get())
            # Resize the image
            edited_image = edited_image.resize((new_width, new_height))
            # Append the edited image to the list of edited images
            edited_images.append(edited_image.copy())
            index_of_image = len(edited_images) - 1
            # Display the resized image
            display_image(edited_image)
            print(f"Resized image to {new_width}x{new_height}")
            popup.destroy()

        # Create a button to trigger the resize action
        resize_button = tk.Button(popup, text="Resize", command=resize_action)

        # Place widgets on the popup window
        width_label.grid(row=0, column=0)
        width_entry.grid(row=0, column=1)
        height_label.grid(row=1, column=0)
        height_entry.grid(row=1, column=1)
        resize_button.grid(row=2, columnspan=2)
    else:
        print("No image to resize")

    current_image_index += 1
    
##################################################
########Functions for  sliders##################
##################################################
# Function to apply sharpness adjustment with a user input popup
def sharpen():
    global edited_image, edited_images, current_image_index
    if edited_image:
        try:
            # Ask the user for the sharpness value using a popup
            sharpness = simpledialog.askfloat("Sharpness", "Enter sharpness value (0.1 to 3.0):", minvalue=0.1, maxvalue=3.0)
            if sharpness is not None:
                edited_image = edited_image.filter(ImageFilter.SHARPEN)
                edited_images.append(edited_image.copy())
                current_image_index = len(edited_images) - 1
                display_image(edited_image)
                print(f"Applied sharpness adjustment with value {sharpness}")
        except ValueError:
            print("Invalid sharpness value entered.")
# Function to apply brightness adjustment with a user input popup
def brighten():
    global edited_image, edited_images, current_image_index
    if edited_image:
        try:
            # Ask the user for the brightness value using a popup
            brightness = simpledialog.askfloat("Brightness", "Enter brightness value (0.1 to 3.0):", minvalue=0.1, maxvalue=3.0)
            if brightness is not None:
                edited_image = ImageEnhance.Brightness(edited_image).enhance(brightness)
                edited_images.append(edited_image.copy())
                current_image_index = len(edited_images) - 1
                display_image(edited_image)
                print(f"Applied brightness adjustment with value {brightness}")
        except ValueError:
            print("Invalid brightness value entered.")
# Function to apply contrast adjustment with a user input popup
def contrast():
    global edited_image, edited_images, current_image_index
    if edited_image:
        try:
            # Ask the user for the contrast value using a popup
            contrast = simpledialog.askfloat("Contrast", "Enter contrast value (0.1 to 3.0):", minvalue=0.1, maxvalue=3.0)
            if contrast is not None:
                edited_image = ImageEnhance.Contrast(edited_image).enhance(contrast)
                edited_images.append(edited_image.copy())
                current_image_index = len(edited_images) - 1
                display_image(edited_image)
                print(f"Applied contrast adjustment with value {contrast}")
        except ValueError:
            print("Invalid contrast value entered.")                    

def black_and_white():
    global edited_image, edited_images, current_image_index
    if edited_image:
        edited_image = edited_image.convert("L")  # Convert to grayscale
        edited_images.append(edited_image.copy())
        current_image_index = len(edited_images) - 1
        display_image(edited_image)
        print("Applied black and white filter")
    else:
        print("no image to apply black and white filter")
####################Code for Drawing#######################
#######################################################
###############################

# Create global variables to store drawing settings
drawing = False
last_x, last_y = 0, 0
shape = None
# Event handler for mouse button down
def start_drawing(event):
    print("Drawing starts\n")
    global drawing, last_x, last_y
    last_x, last_y = event.x, event.y
    drawing = True
# Event handler for mouse motion

# Event handler for mouse button release
def stop_drawing(event):
    print("Drawing ends\n")
    global drawing
    drawing = False
    
def set_shape(new_shape):
    global shape
    shape = new_shape              
################Creating an window#######################
##########Adding canvass######################   
# Create the main application window
app = tk.Tk()
#app.overrideredirect(1)
app.geometry("1920x1080")
# Create a custom title bar
app.title("Quickflash")
app.configure(background='#635969')

custom_style=ttk.Style()
custom_style.configure("Custom.TButton",background="green",foreground="white",font=("Arial",12))
#app.configure(style="Custom.Tk")
# Load the logo image
app.iconbitmap("favicon.ico")

sliders_frame=tk.LabelFrame(app,text="Adjustments",width=400,bg="#352f38")
sliders_frame.pack(side="right",fill='y')

# Create sliders with associated functions
sharpness_button = tk.Button(sliders_frame,text="Sharpen",command=sharpen)
sharpness_button.pack()
#sharpness_scale.bind("<Motion>",update_image)

brightness_button = tk.Button(sliders_frame,text="Brighten",command=brighten)
brightness_button.pack()
#brightness_scale.bind("<Motion>",update_image)

contrast_button = tk.Button(sliders_frame,text="Contrast",command=contrast)
contrast_button.pack()
#contrast_scale.bind("<Motion>",update_image)
greyscale_button = tk.Button(sliders_frame, text="greyscale", command=black_and_white)
greyscale_button.pack()
#Create a frame to implement basic drawing tools
draw_frame=tk.LabelFrame(app,text="Geometric shape",width=300,height=200,bg="#352f38")
draw_frame.pack(side="left",fill="y")

#####Buttons for drawing##########
button_container = tk.Frame(draw_frame)
button_container.pack(side="top")

circle_button = tk.Button(button_container, text="Draw Circle", command=lambda: set_shape("circle"))
circle_button.pack(side="left")

rectangle_button = tk.Button(button_container, text="Draw Rectangle",command=lambda: set_shape("rectangle"))
rectangle_button.pack(side="left")

oval_button = tk.Button(button_container, text="Draw Oval",command=lambda: set_shape("oval"))
oval_button.pack(side="left")

line_button = tk.Button(button_container, text="Draw Line",command=lambda: set_shape("line"))
line_button.pack(side="left")

#Create a frame to implement painting inside draw frame
paint_frame=tk.LabelFrame(draw_frame,text="Paint",width=300,height=200,bg="#99959c")
paint_frame.pack(side="left")

# Create a canvas to display the image
canvas = tk.Canvas(app, width=1200, height=1070,bg='#d2bdde')
canvas.pack(anchor='nw',fill='both',expand=1)
def draw(event):
    global last_x,last_y,canvas
    if drawing:
        x, y = event.x, event.y
        if shape == "circle":
            canvas.create_oval(last_x, last_y, x, y, outline="black", width=2)
        elif shape == "rectangle":
            canvas.create_rectangle(last_x, last_y, x, y, outline="black", width=2)
        elif shape == "oval":
            canvas.create_oval(last_x, last_y, x, y, outline="black", width=2)
        elif shape == "line":
            canvas.create_line(last_x, last_y, x, y, fill="black", width=2)
        last_x, last_y = x, y
# Bind mouse events to the canvas
canvas.bind("<Button-1>", start_drawing)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_drawing)

# Create a menu bar
# Create a custom style for the menu bar
menu_style = ttk.Style()
menu_style.configure("Custom.TMenubutton", background="green", foreground="white", font=("Arial", 12))
menu_bar = tk.Menu(app,bg="green")
app.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0,bg="green")
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_image)
file_menu.add_command(label="Save", command=save_image)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app.quit)

# Edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=undo)
edit_menu.add_command(label="Redo", command=redo)
edit_menu.add_separator()

#Filter
filter_menu=tk.Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label='Filter',menu=filter_menu)
filter_menu.add_command(label="Blur", command=lambda: apply_filter("Blur"))
filter_menu.add_command(label="Contour", command=lambda: apply_filter("Contour"))
filter_menu.add_command(label="Edge enhance", command=lambda: apply_filter("Edge enhance"))
filter_menu.add_command(label="Edge enhance more", command=lambda: apply_filter("Edge enhance more"))
filter_menu.add_command(label="Emboss", command=lambda: apply_filter("Emboss"))
filter_menu.add_command(label="Find edges", command=lambda: apply_filter("Find edges"))
filter_menu.add_command(label="Smooth", command=lambda: apply_filter("Smooth"))
filter_menu.add_command(label="Smooth more", command=lambda: apply_filter("Smooth more"))
filter_menu.add_command(label="Sharpen", command=lambda: apply_filter("Sharpen"))
filter_menu.add_command(label="Remove noise", command=lambda: apply_filter("Remove noise"))

#tools
tool_menu=tk.Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label='Tools',menu=tool_menu)
tool_menu.add_command(label="Rotate 90 degree clockwise",command=rotate)
tool_menu.add_command(label="Rotate 90 degree anticlockwise",command=rotate)
tool_menu.add_command(label="Mirror",command=mirror)
tool_menu.add_command(label="Resize",command=perform_resize)
tool_menu.add_command(label="Interactive Crop",command=crop)

login_popup()
# Run the Tkinter main loop
app.mainloop()
