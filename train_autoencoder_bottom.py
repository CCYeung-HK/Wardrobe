#Reference
#Adrian Rosebrock, Autoencoders for Content-based Image Retrieval with Keras and TensorFlow, PyImageSearch, https://www.pyimagesearch.com/2020/03/30/autoencoders-for-content-based-image-retrieval-with-keras-and-tensorflow/, accessed on 14 July 2020

#training autoencoder for bottoms images
#set the matplotlib nbackend so figures can be saved in background
import matplotlib
from pyimagesearch.convautoencoder_bottoms import ConvAutoencoder
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt
import numpy as np
import argparse
import cv2
import tensorflow as tf

from PIL import Image
from sklearn.model_selection import train_test_split
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

#construct the argument parse and parse the arguments
#adding commandline arguments
#-model -> points to the path of the trained output autoencoder
#-vis -> Path to the output visualisation image
#-plot -> path to the matplotlib output plot
ap = argparse.ArgumentParser()
ap.add_argument('-m', '--model', type=str, required=True, help='path to output trained aitoencoder')
ap.add_argument('-v', '--vis', type=str, default='recon_vis.png', help='path to output reconstruction visualisation file')
ap.add_argument('-p', '--plot', type=str, default='plot.png', help='path to output plot file')
args = vars(ap.parse_args())


#PREPARE TO TRAIN THE AUTOENCODER
#initialise the number of epochs to train for, initial learning rate and batch size
EPOCHS = 25
INIT_LR = 1e-3
BS = 20
#epochs = cycle through the full training set
#INIT_LR = learning rate (initial)
#BS = Batch size = number of training samples in one forward pass (<= number of samples ind train set)

#load the bottoms images data
#converting images from jpg format to uint8 for the encoder
print('[INFO] loading tops images')
bottoms = [str('bottoms/') + imagefile for imagefile in os.listdir('bottoms/') if not imagefile.startswith('.')]
bottoms_image_uint8 = []
for image in bottoms:
    im = Image.open(image)
    im_resized = im.resize((256, 256), Image.ANTIALIAS)
    im_uint8 = np.array(im_resized)
    bottoms_image_uint8.append(im_uint8)
#Split the dataset for training and testing purpose
trainX, testX = train_test_split(bottoms_image_uint8, train_size = 0.8, test_size = 0.2, random_state=6)

#then convert to float32 array
#We don't need to add another channel dimension as the MNIST data did since its already has 3 channel dimensions
trainX = np.array(trainX)
testX = np.array(testX)
trainX = trainX.astype('float32') / 255.0
testX = testX.astype('float32') / 255.0

#construct our convolutional autoencoder
print('[INFO] building autoencoder')
#build(width, height, depth)
autoencoder = ConvAutoencoder.build(256, 256, 3)
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
autoencoder.compile(loss='mse', optimizer=opt)

#train the convolutional autoencoder
H = autoencoder.fit(
    trainX, trainX, 
    validation_data=(testX, testX), 
    epochs=EPOCHS, 
    batch_size=BS
)

#use the convolutional autoencoder to make predictions on the testing images, construct the visualizationa, and then save it to disk
print('[INFO] making predictions...')
decoded = autoencoder.predict(testX)

#For visualising the convolutional results
n = 10  # how many digits we will display
plt.figure(figsize=(20, 4))
for i in range(n):
    # display original
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(testX[i].reshape(256, 256, 3))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # display reconstruction
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded[i].reshape(256, 256, 3))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()

# vis = visualize_predictions(decoded, testX)
# cv2.imwrite(args['vis'], vis)

#construct a plot that plots and saves the training history
N= np.arange(0, EPOCHS)
plt.style.use('ggplot')
plt.figure()
plt.plot(N, H.history['loss'], label='train_loss')
plt.plot(N, H.history['val_loss'], label='val_loss')
plt.title('training loss and accuracy')
plt.xlabel('EPOCH #')
plt.ylabel('loss/accuracy')
plt.legend(loc='lower left')
plt.savefig(args['plot'])

#serialize the autoencoder model to disk
print('[INFO] saving autoencoder...')
autoencoder.save(args['model'], save_format='h5')

