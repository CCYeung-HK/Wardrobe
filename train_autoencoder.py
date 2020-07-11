#set the matplotlib nbackend so figures can be saved in background
import matplotlib
matplotlib.use('Agg')

from pyimagesearch.convautoencoder import ConvAutoencoder
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt
import numpy as np
import argparse
import cv2

from PIL import Image
from sklearn.model_selection import train_test_split
import os

def visualize_predictions(decoded, gt, samples=10):
    #initialize our list of output samples
    outputs = None

    #loop over our number of output samples
    #original vs decoded
    for i in range(0, samples):
        original = (gt[i] * 225).astype('uint8')
        recon = (decoded[i] * 225).astype('uint8')

    #stack the original image and reconstructed image side-by-side
    output = np.hstack([original, recon])

    #if the outside array is empty, initialise it as the current side-by-side image display
    if outputs is None:
        outputs = output

    #otherwise, vertically stack the outputs
    else:
        outputs = np.vstack([outputs, output])

    #return the output images
    return outputs

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
EPOCHS = 20
INIT_LR = 1e-3
BS = 32
#epochs = cycle through the full training set
#INIT_LR = learning rate (initial)
#BS = Batch size = number of training samples in one forward pass (<= number of samples ind train set)

#load the MNISR dataset
#(xtrain, ytrain), (xtest, ytest)
#HERE TO MODIFY AS THE IMAGE DATA
print('[INFO] loading tops images')
tops = [str('tops/') + imagefile for imagefile in os.listdir('tops/') if not imagefile.startswith('.')]
tops_image_uint8 = []
for image in tops:
    im = Image.open(image)
    im_resized = im.resize((250, 250), Image.ANTIALIAS)
    im_uint8 = np.array(im_resized)
    tops_image_uint8.append(im_uint8)
print(tops_image_uint8[0])
print(tops_image_uint8[0].dtype)
trainX, testX = train_test_split(tops_image_uint8, train_size = 0.8, test_size = 0.2, random_state=6)

#add a channel dimension to every image in the dataset, then scale the pixel intensities to the range [0,1]
trainX = np.expand_dims(trainX, axis=-1)
testX = np.expand_dims(testX, axis=-1)
#expand the shape of an array, axis -> position in the epanded axes where the new axis is placed
#then convert to float32 array
trainX = trainX.astype('float32') / 255.0
testX = testX.astype('float32') / 255.0

#construct our convolutional autoencoder
print('[INFO] building autoencoder')
#build(width, height, depth)
autoencoder = ConvAutoencoder.build(28, 28, 1)
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
vis = visualize_predictions(decoded, testX)
cv2.imwrite(args['vis'], vis)

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

