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

appeared_image = []

def clear_previous_search_data():
    appeared_image.clear()


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
trainX = trainX.astype('float32') / 255.0
testX = testX.astype('float32') / 255.0

#load the autoencofer model and index from disk
print('[INFO] loading autoencoder and index..')
autoencoder = load_model('output/autoencoder.h5')
index = pickle.loads(open('output/index.pickle', 'rb').read())

#create the encoder model which consists of *jsut* the encoder protion of the autoencoder
encoder = Model(inputs=autoencoder.input, outputs=autoencoder.get_layer('encoded').output)

def search(query):
#quantify the contents of our input testing images using the encoder
#CHANGE IT TO OUR INPUT IMAGE INSTEAD OF USING TESTING IMAGES
    print('[INFO] encoding testing images')
    # May needa convert query to uint8 here (query from index is maybe jpg)
    # Converting to uint8 (will be needed when implement)
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

    # FOR TESTING PURPOSE
    #display the query image
    # query_uint8_2 = (query_expanded * 255).astype('uint8')
    # query_squeeze = np.squeeze(query_uint8_2, axis=0)
    # b,g,r = cv2.split(query_squeeze)
    # query_squeeze = cv2.merge([r,g,b])
    # cv2.imshow("Query", query_squeeze)

    if query in appeared_image:
        pass
    else:
        appeared_image.append(query)
    
    images_indexes = [i[1] for i in images]

    for i in range(len(images_indexes)):
        print(i)
        if tops[images_indexes[i]] in appeared_image:
            pass
        else:
            appeared_image.append(tops[images_indexes[i]])
            print(appeared_image)
            return images_indexes[i]

    # FOR TESTING USE
    # recommendation = Image.open(tops[recommendation_index])
    # recommendation.show()
    # print(query)
    # print(recommendation_index)
        # build a montage from the results and display it
    # montage = build_montages((row[0] for row in images), (256,256), (10, 10))[0]
    # cv2.imshow('Results', montage)
    # cv2.waitKey(0) 