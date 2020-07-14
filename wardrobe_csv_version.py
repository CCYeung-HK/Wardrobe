#For reading the csv which extracts images from the web in real time when requested 
#instead of requiring to download all the images for the code
#ONLY in random wardrobe version (NO ML)
import os
import random

import requests
import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
import io

tops_df = pd.read_csv('man_tops.csv')
bottoms_df = pd.read_csv('man_bottoms.csv')

WINDOW_TITLE = 'wardorbe'
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 220
IMG_WIDTH = 250
IMG_HEIGHT = 250

# Store all the Tops into a file we can access
ALL_TOPS_IMAGE = tops_df["Image_url"] 
ALL_BOTTOMS_IMAGE = bottoms_df['Image_url']

class wardrobeApp:
    def __init__(self, root):
        self.root = root

        #show top/bottoms image in the window
        self.top_images = ALL_TOPS_IMAGE
        self.bottom_images = ALL_BOTTOMS_IMAGE
        #save single top
        self.top_image_path = self.top_images[0]
        self.bottom_image_path = self.bottom_images[0]
        #create and add top image into frame
        self.tops_frame = tk.Frame(self.root)
        self.bottom_frame = tk.Frame(self.root)
        self.top_image_label = self.create_photo(self.top_image_path, self.tops_frame)
        self.bottom_image_label = self.create_photo(self.bottom_image_path, self.bottom_frame)
        #add it to pack (add the label widgets to the window (i.e displaying it))
        self.top_image_label.pack(side=tk.TOP)
        self.bottom_image_label.pack(side=tk.TOP)

        #create background
        self.create_background()
        

    def create_background(self):

        #add title to window and change the size
        self.root.title(WINDOW_TITLE)
        self.root.geometry('{0}x{1}'.format(WINDOW_WIDTH, WINDOW_HEIGHT))

        #add all buttons
        self.create_buttons()

        #add clothing (fill both = vertically and horizontally expands to fill the window, expand = assign space if the widgets are oversized)
        self.tops_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.bottom_frame.pack(fill=tk.BOTH, expand=tk.YES)

    def create_buttons(self):
        #creating prev/next buttons
        #(master widget (frames), command = function to be called)
        top_prev_button = tk.Button(self.tops_frame, text='Prev', command = self.get_prev_top)
        top_prev_button.pack(side=tk.LEFT)

        top_next_button = tk.Button(self.tops_frame, text='Next', command=self.get_next_top)
        top_next_button.pack(side=tk.RIGHT)

        bottom_prev_button = tk.Button(self.bottom_frame, text='Prev', command = self.get_prev_bottom)
        bottom_prev_button.pack(side=tk.LEFT)

        bottom_next_button = tk.Button(self.bottom_frame, text='Next', command=self.get_next_bottom)
        bottom_next_button.pack(side=tk.RIGHT)

        #create outfit button
        create_outfit_button = tk.Button(self.bottom_frame, text='Create Outfit', command=self.create_outfit)
        create_outfit_button.pack(side=tk.LEFT)


    #general fcn that will allow us to move front and back
    def _get_next_item(self, current_item, category, increment = True):
        #if we know where the current item index is in a category, then we find the pic before and after it
        item_index = category[category == current_item].index[0]
        final_index = len(category) - 1
        next_index = 0

        if increment and item_index == final_index:
            #add the end, and need to up, cycle back to beginning
            next_index = 0
        elif not increment and item_index == 0:
            #cycle back to end
            next_index = final_index
        else:
            #regular up and down
            #based on increment
            increment = 1 if increment else -1
            next_index = item_index + increment
        
        next_image = category[next_index]

        # reset update the image based on next_image path
        if current_item in self.top_images.values:
            image_label = self.top_image_label
            self.top_image_path = next_image
        else:
            image_label = self.bottom_image_label
            self.bottom_image_path = next_image

        #use update function to change image
        self.update_image(next_image, image_label)

    def update_image(self, new_image_path, image_label):
        #collect and change image into tk photo obj
        response = requests.get(new_image_path, stream=True)
        image_file = Image.open(io.BytesIO(response.content))
        image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
        tk_photo = ImageTk.PhotoImage(image_resized)

        #update based on provided image label
        image_label.configure(image=tk_photo)

        image_label.image = tk_photo

    def get_next_top(self): 
        self._get_next_item(self.top_image_path, self.top_images)

    def get_prev_top(self):
        self._get_next_item(self.top_image_path, self.top_images, increment=False)

    def get_next_bottom(self): 
        self._get_next_item(self.bottom_image_path, self.bottom_images)

    def get_prev_bottom(self):
        self._get_next_item(self.bottom_image_path, self.bottom_images, increment=False)

    def create_photo(self, image_path, frame):
        #get PIL image
        response = requests.get(image_path, stream=True)
        image_file = Image.open(io.BytesIO(response.content))
        #resize with PIL
        image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
        #get tk image from the PIL image
        tk_photo = ImageTk.PhotoImage(image_resized)
        #create label for the image (frame = master widget)
        image_label = tk.Label(frame, image=tk_photo)
        image_label.image = tk_photo

        return image_label

    def create_outfit(self):
        #rand select a top&bottom index
        new_top_index = random.randint(0, len(self.top_images)-1)
        new_bottom_index = random.randint(0, len(self.bottom_images)-1)

        #add clothes onto screen
        self.update_image(self.top_images[new_top_index], self.top_image_label)
        self.update_image(self.bottom_images[new_bottom_index], self.bottom_image_label)

    


root = tk.Tk()
app = wardrobeApp(root)
root.mainloop()