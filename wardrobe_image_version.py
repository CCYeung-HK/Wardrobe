import os
import random

import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import search_image
import search_image_bottoms


WINDOW_TITLE = 'wardorbe'
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 220
IMG_WIDTH = 250
IMG_HEIGHT = 250

# Store all the Tops into a file we can access
ALL_TOPS = [str('tops/') + imagefile for imagefile in os.listdir('tops/') if not imagefile.startswith('.')]
ALL_BOTTOMS = [str('bottoms/') + imagefile for imagefile in os.listdir('bottoms/') if not imagefile.startswith('.')]

class wardrobeApp:
    def __init__(self, root):
        self.root = root

        #show top/bottoms image in the window
        self.top_images = ALL_TOPS
        self.bottom_images = ALL_BOTTOMS
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
        top_prev_button = tk.Button(self.tops_frame, text='Give me some ideas', command = self.create_outfit)
        top_prev_button.pack(side=tk.LEFT)

        top_next_button = tk.Button(self.tops_frame, text='Love it', command=self.get_similar_outfit)
        top_next_button.pack(side=tk.RIGHT)

        # bottom_prev_button = tk.Button(self.bottom_frame, text='Prev', command = self.get_prev_bottom)
        # bottom_prev_button.pack(side=tk.LEFT)

        # bottom_next_button = tk.Button(self.bottom_frame, text='Next', command=self.get_next_bottom)
        # bottom_next_button.pack(side=tk.RIGHT)

        #create outfit button
        # create_outfit_button = tk.Button(self.bottom_frame, text='Create Outfit', command=self.create_outfit)
        # create_outfit_button.pack(side=tk.LEFT)


    #general fcn that will allow us to move front and back
    # def _get_next_item(self, current_item, category, increment = True):
    #     #if we know where the current item index is in a category, then we find the pic before and after it
    #     item_index = category.index(current_item)
    #     final_index = len(category) - 1
    #     next_index = 0

    #     if increment and item_index == final_index:
    #         #add the end, and need to up, cycle back to beginning
    #         next_index = 0
    #     elif not increment and item_index == 0:
    #         #cycle back to end
    #         next_index = final_index
    #     else:
    #         #regular up and down
    #         #based on increment
    #         increment = 1 if increment else -1
    #         next_index = item_index + increment
        
    #     next_image = category[next_index]

    #     # reset update the image based on next_image path
    #     if current_item in self.top_images:
    #         image_label = self.top_image_label
    #         self.top_image_path = next_image
    #     else:
    #         image_label = self.bottom_image_label
    #         self.bottom_image_path = next_image

    #     #use update function to change image
    #     self.update_image(next_image, image_label)

    def update_image(self, new_image_path, image_label):
        #collect and change image into tk photo obj
        image_file = Image.open(new_image_path)
        image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
        tk_photo = ImageTk.PhotoImage(image_resized)

        #update based on provided image label
        image_label.configure(image=tk_photo)

        image_label.image = tk_photo

    def get_similar_outfit(self): 
        #Now treat it as a like button
        # self._get_next_item(self.top_image_path, self.top_images)
        self.like_outfit(self.top_image_path, self.bottom_image_path)

    # def get_prev_top(self):
    #     self._get_next_item(self.top_image_path, self.top_images, increment=False)

    # def get_next_bottom(self): 
    #     self._get_next_item(self.bottom_image_path, self.bottom_images)

    # def get_prev_bottom(self):
        # self._get_next_item(self.bottom_image_path, self.bottom_images, increment=False)

    def create_photo(self, image_path, frame):
        #get PIL image
        image_file = Image.open(image_path)
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
        self.top_image_path = self.top_images[new_top_index]
        self.update_image(self.bottom_images[new_bottom_index], self.bottom_image_label)
        self.bottom_image_path = self.bottom_images[new_bottom_index]
        print(self.top_image_path)

        search_image.clear_previous_search_data()
        search_image_bottoms.clear_previous_search_data()

    def like_outfit(self, current_item_top, current_item_bottom):
        print(current_item_top)
        recommendation_index_top = search_image.search(current_item_top)
        reco_image_top = self.top_images[recommendation_index_top]
        self.top_image_path = reco_image_top
        self.update_image(reco_image_top, self.top_image_label)

        recommendation_index_bottoms = search_image_bottoms.search(current_item_bottom)
        reco_image_bottom = self.bottom_images[recommendation_index_bottoms]
        self.bottom_image_path = reco_image_bottom
        self.update_image(reco_image_bottom, self.bottom_image_label)


root = tk.Tk()
app = wardrobeApp(root)
root.mainloop()