from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model
from tensorflow.keras.datasets import mnist
from imutils import build_montages
from sklearn.model_selection import train_test_split
from PIL import Image


import matplotlib.pyplot as plt
import numpy as np
import argparse
import pickle
import cv2
import os

def euclidean(a, b):
    #compile and return the euclidean distance between two vectors
    return np.linalg.norm(a - b)

def perform_search(queryFeatures, index, maxResults=64):
    #initialize our list of results
    results = []

    #loop over our index
    for i in range(0, len(index['features'])):
        #compute the euclidean distance between our query features
        #and the features for the current image in our index, then
        #update our results list with a 2-tuple consisting of the 
        #computed distance and the index of the image
        d = euclidean(queryFeatures, index['features'][i])
        results.append((d, i))

    #sort the results and grab the top ones
    results = sorted(results)[:maxResults]

    #return the list of results
    return results

#To ensure same suggestions would not come up when users consecutively like the outfit 
appeared_image = []

#Clear the above restrictions when users generate new random oufit
def clear_previous_search_data():
    appeared_image.clear()


#load the bottoms dataset, same conversion as train_autoencoder
print('[INFO] loading bottoms images')
bottoms = [str('bottoms/') + imagefile for imagefile in os.listdir('bottoms/') if not imagefile.startswith('.')]
bottoms_image_uint8 = []
for image in bottoms:
    im = Image.open(image)
    im_resized = im.resize((256, 256), Image.ANTIALIAS)
    im_uint8 = np.array(im_resized)
    bottoms_image_uint8.append(im_uint8)
#using labels for finding the image at later stage
bottoms_indexes = [*range(len(bottoms))]
trainX, testX, trainY, testY = train_test_split(bottoms_image_uint8, bottoms_indexes, train_size = 0.8, test_size = 0.2, random_state=6)


trainX = np.array(trainX)
testX = np.array(testX)
trainX = trainX.astype('float32') / 255.0
testX = testX.astype('float32') / 255.0

#load the autoencofer model and index from disk
print('[INFO] loading autoencoder and index..')
autoencoder = load_model('output/autoencoder_bottoms.h5')
index = pickle.loads(open('output/index_bottoms.pickle', 'rb').read())

#create the encoder model which consists of *jsut* the encoder protion of the autoencoder
encoder = Model(inputs=autoencoder.input, outputs=autoencoder.get_layer('encoded').output)

def search(query):
    #quantify the contents of our input image using the encoder
    print('[INFO] encoding testing images')
    #converting format of the query from the app from jpg to uint8 and float32
    query_image = Image.open(query)
    query_resized = query_image.resize((256, 256), Image.ANTIALIAS)
    query_uint8 = np.array(query_resized) 
    query_float32 = query_uint8.astype('float32') / 255.0
    query_expanded = np.expand_dims(query_float32, axis=0)
    features = encoder.predict(query_expanded)

    #take the features for the current image, find all similar iamges in our dataset, then initialize our list of result images
    queryFeatures = features
    results = perform_search(queryFeatures, index, maxResults=225)
    images = []

    #loop over the results
    for (d,j) in results:
        #grab the result image, convert back to the range [0,225], then update the images list
        image = [(trainX[j] * 255).astype('uint8'), trainY[j]]
        b,g,r = cv2.split(image[0])
        image[0] = cv2.merge([r,g,b])
        image[0] = np.dstack([image[0]])
        images.append(image)

    #Ensure same outfit would not come up
    if query in appeared_image:
        pass
    else:
        appeared_image.append(query)
    
    images_indexes = [i[1] for i in images]

    for i in range(len(images_indexes)):
        if bottoms[images_indexes[i]] in appeared_image:
            pass
        else:
            appeared_image.append(bottoms[images_indexes[i]])
            return images_indexes[i]