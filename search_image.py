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
import pandas as pd

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


#PROBABY WILL DELETE THIS as we can assign it in the code instead (we know the path anyway)
ap = argparse.ArgumentParser()
# ap.add_argument('-m', '--model', type=str, required=True, help='path to trained autoencoder')
# ap.add_argument('-i', '--index', type=str, required=True, help='path to features index file')
#index of features to search through (i.e. the serialized index)
ap.add_argument('-s', '--sample', type=int, default=10, help='# of testing queries to perform')
#number of testing queries to perfrom with a default of 10
args=vars(ap.parse_args())

#load the MNIST dataset
print('[INFO] loading tops images')
tops = [str('tops/') + imagefile for imagefile in os.listdir('tops/') if not imagefile.startswith('.')]
tops_image_uint8 = []
for image in tops:
    im = Image.open(image)
    im_resized = im.resize((256, 256), Image.ANTIALIAS)
    im_uint8 = np.array(im_resized)
    tops_image_uint8.append(im_uint8)
tops_indexes = [*range(len(tops))]
trainX, testX, trainY, testY = train_test_split(tops_image_uint8, tops_indexes, train_size = 0.8, test_size = 0.2, random_state=6)


#add a channel dimension to every image in the dataset, then scale the pixel intensities to the range[0,1]
trainX = np.array(trainX)
testX = np.array(testX)
# trainX = np.expand_dims(trainX, axis=-1)
# testX = np.expand_dims(testX, axis=-1)
trainX = trainX.astype('float32') / 255.0
testX = testX.astype('float32') / 255.0

#load the autoencofer model and index from disk
print('[INFO] loading autoencoder and index..')
autoencoder = load_model('output/autoencoder.h5')
index = pickle.loads(open('output/index.pickle', 'rb').read())

#create the encoder model which consists of *jsut* the encoder protion of the autoencoder
encoder = Model(inputs=autoencoder.input, outputs=autoencoder.get_layer('encoded').output)

#quantify the contents of our input testing images using the encoder
#CHANGE IT TO OUR INPUT IMAGE INSTEAD OF USING TESTING IMAGES
def search(query):
    print('[INFO] encoding testing images')
    # features = encoder.predict(testX)
    # May needa convert query to uint8 here (query from index is maybe jpg)
    # Converting to uint8 (will be needed when implement)
    # query = Image.open(query)
    # query_resized = query.resize((256, 256), Image.ANTIALIAS)
    # query_uint8 = np.array(query_resized) 
    # query = query_uint8.astype('float32') / 255.0
    query = np.expand_dims(query, axis=0)
    features = encoder.predict(query)

    #randomly sample a set of testing query image indexes
    #HERE CAN BE REMOVED AS INPUT QUERY WILL BE FROM USERS
    # queryIdxs = list(range(0, testX.shape[0]))
    # queryIdxs = np.random.choice(queryIdxs, size=args['sample'], replace=False)

    #loop over the testing indexes
    #for i in queryIdxs:
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

        #display the query image
    query = (query * 255).astype('uint8')
    query = np.squeeze(query, axis=0)
    b,g,r = cv2.split(query)
    query = cv2.merge([r,g,b])
    cv2.imshow("Query", query)

    recommendation_index = images[0][1]
    recommendation = Image.open(tops[recommendation_index])
    recommendation.show()

        #build a montage from the results and display it
    montage = build_montages((row[0] for row in images), (256,256), (10, 10))[0]
    cv2.imshow('Results', montage)
    cv2.waitKey(0)