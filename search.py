from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model
from tensorflow.keras.datasets import mnist
from imutils import build_montages
import numpy as np
import argparse
import pickle
import cv2

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

ap = argparse.ArgumentParser()
ap.add_argument('-m', '--model', type=str, required=True, help='path to trained autoencoder')
ap.add_argument('-i', '--index', type=str, required=True, help='path to features index file')
#index of features to search through (i.e. the serialized index)
ap.add_argument('-s', '--sample', type=int, default=10, help='# of testing queries to perform')
#number of testing queries to perfrom with a default of 10
args=vars(ap.parse_args())

#load the MNIST dataset
print('[INFO] loading MNIST DATASET')
((trainX, _), (testX, _)) = mnist.load_data()

#add a channel dimension to every image in the dataset, then scale the pixel intensities to the range[0,1]
trainX = np.expand_dims(trainX, axis=-1)
testX = np.expand_dims(testX, axis=-1)
trainX = trainX.astype('float32') / 255.0
testX = testX.astype('float32') / 255.0

#load the autoencofer model and index from disk
print('[INFO] loading autoencoder and index..')
autoencoder = load_model(args['model'])
index = pickle.loads(open(args['index'], 'rb').read())

#create the encoder model which consists of *jsut* the encoder protion of the autoencoder
encoder = Model(inputs=autoencoder.input, outputs=autoencoder.get_layer('encoded').output)

#quantify tje contents of our input testing images using the encoder
print('[INFO] encoding testing images')
features = encoder.predict(testX)



#randomly sample a set of testing query image indexes
queryIdxs = list(range(0, testX.shape[0]))
queryIdxs = np.random.choice(queryIdxs, size=args['sample'], replace=False)

#loop over the testing indexes
for i in queryIdxs:
    #take the features for the current image, find all similar iamges in our dataset, then initialize our list of result images
    queryFeatures = features[i]
    results = perform_search(queryFeatures, index, maxResults=225)
    images = []

    #loop over the results
    for (d,j) in results:
        #grab the result image, convert back to the range [0,225], then update the images list
        image = (trainX[j] * 225).astype('uint8')
        image = np.dstack([image] * 3)
        images.append(image)

    #display the query image
    query = (testX[i] * 225).astype('uint8')

    #build a montage from the results and display it
    montage = build_montages(images, (28, 28), (15, 15))[0]
    cv2.imshow('Results', montage)
    cv2.waitKey(0)
