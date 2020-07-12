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

#load the MMIST dataset
#WE NEEDA CHANGE THIS
print('[INFO] loading tops images')
tops = [str('tops/') + imagefile for imagefile in os.listdir('tops/') if not imagefile.startswith('.')]
tops_image_uint8 = []
for image in tops:
    im = Image.open(image)
    im_resized = im.resize((256, 256), Image.ANTIALIAS)
    im_uint8 = np.array(im_resized)
    tops_image_uint8.append(im_uint8)
trainX, testX = train_test_split(tops_image_uint8, train_size = 0.8, test_size = 0.2, random_state=6)

#add a channel dimension to every image in the training split, then scale the pixel intensities to the range [0,1]
trainX = np.expand_dims(trainX, axis=-1)
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

#construct a dictionary that maps the index of the MNIST training
#image to its correspinding latent-space representation
indexies = list(range(0, trainX.shape[0]))
#indexies = integer indicies of each MNIST digit image in the dataset
#features = the corresponding feature vetor for each image in the dataset
data = {'indexies': indexies, 'features': features}

#write the data dictionary to disk in pickle format
print('[INFO] saving index.....')
f = open(args['index'], 'wb')
f.write(pickle.dumps(data))
f.close()

