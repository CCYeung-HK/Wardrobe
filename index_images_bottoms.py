#Reference
#Adrian Rosebrock, Autoencoders for Content-based Image Retrieval with Keras and TensorFlow, PyImageSearch, https://www.pyimagesearch.com/2020/03/30/autoencoders-for-content-based-image-retrieval-with-keras-and-tensorflow/, accessed on 14 July 2020

from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model
from tensorflow.keras.datasets import mnist
from sklearn.model_selection import train_test_split
from PIL import Image

import os
import numpy as np
import argparse
import pickle

ap=argparse.ArgumentParser()
ap.add_argument('-m', '--model', type=str, required=True, help='path to trained autoencoder')
# the path to the output features index file in .pickle format
ap.add_argument('-i', '--index', type=str, required=True, help='path to output features index file')
args=vars(ap.parse_args())

#loading the bottoms images, same as format conversion from train_encoder
print('[INFO] loading bottoms images')
bottoms = [str('bottoms/') + imagefile for imagefile in os.listdir('bottoms/') if not imagefile.startswith('.')]
bottoms_image_uint8 = []
for image in bottoms:
    im = Image.open(image)
    im_resized = im.resize((256, 256), Image.ANTIALIAS)
    im_uint8 = np.array(im_resized)
    bottoms_image_uint8.append(im_uint8)
trainX, testX = train_test_split(bottoms_image_uint8, train_size = 0.8, test_size = 0.2, random_state=6)

#add a channel dimension to every image in the training split, then scale the pixel intensities to the range [0,1]
trainX = np.array(trainX)
trainX = trainX.astype('float32') / 255.0

#load our autoencoder from disk
print('[INFO] loading autoencoder model...')
autoencoder = load_model(args['model'])

#create the encoder model which consists of *just* the encoder portion of the autoencoder
encoder = Model(inputs=autoencoder.input,
    outputs=autoencoder.get_layer('encoded').output)

#quantify the contents of our input images using the encoder 
print('[INFO] encoding images...')
features = encoder.predict(trainX)

#construct a dictionary that maps the index of the training
#image to its correspinding latent-space representation
indexies = list(range(0, trainX.shape[0]))
#indexies = integer indicies of each image in the dataset
#features = the corresponding feature vetor for each image in the dataset
data = {'indexies': indexies, 'features': features}

#write the data dictionary to disk in pickle format
print('[INFO] saving index.....')
f = open(args['index'], 'wb')
f.write(pickle.dumps(data))
f.close()

