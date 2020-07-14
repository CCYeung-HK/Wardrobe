# Personalised Wardrobe

A wardrobe to generate random outfit ideas and provides suggestions based on your previous preference.
(current data scraped from H.M using BeautifulSoup)

## Current Version

Only worked on Man's clothing. Will scrape more data from woman's section later and develop and woman wardrobe as well.

## Prerequistes

* Python 3.5 or greater
* pip package management tool
* pip 19.0 or greater
* Ubuntu 16.04 or later (64-bit)
* macOS 10.12.6 (Sierra) or later (64-bit)
* Windows 7 or later (64-bit)
Most of them are the basic requirements for tensorflow

## Installing dependencies

1. To install all dependencies 
```bash
pip install -r dependencies.txt
```
2. For tensorflow installation, please refer to https://www.tensorflow.org/install/pip

3. (Optional) If you want to utilize GPUs when running tensorflow, please refer to https://www.tensorflow.org/install/gpu 

## Local Setup

* To run the wardrobe app with existing database (Images currently from H.M websites)
1. Run the python script
```bash
python wardrobe_image_version.py
```

* To setup your own database
1. Upload images to folder 'tops' & 'bottoms' respectively

2. Train the models
    * Train the Tops autoencoder model
    ```bash
    python train_autoencoder.py --model output/autoencoder.h5 --vis output/recon_vis.png --plot output/plot.png
    ```
    * Train the Bottoms autoencoder model
    ```bash
    python train_autoencoder_bottom.py --model output/autoencoder_bottoms.h5 --vis output/recon_vis.png --plot output/plot_bottoms.png
    ```

3. Indexing the training model features
    * Index Tops model
    ```bash
    python index_images.py --model output/autoencoder.h5 --index output/index.pickle
    ```

    * Index Bottoms model
    ```bash
    python index_images_bottoms.py --model output/autoencoder_bottoms.h5 --index output/index_bottoms.pickle
    ```
4. Run the wardrobe app 
```bash
python wardrobe_image_version.py
```
* To webscrape (optional)
1. Scraping website (Optional)
```bash
python scrape.py
```
(Please scrape with respect and not overshoot with requests to the server)

## Project description

The wardrobe is designed to generate random outfit ideas by looking up the database (Tops and Bottoms). When users like the current outfit by clicking 'Love it' Button, the machine learning model will intake the current images and perform query search in the database to find the most alike or similar outfits. 

The neural network used here is autoencoder which is used commonly in image recognition. By importing the dataset, feature vectors are obtained through the layers and the model and allow us to quantify the features of the inputed images. Utilising such representation (the latent vector), similar outfit (images) are found by calculating the relative distance from the query images (outfit that the user likes).   

## Future outlook

The project is still far from perfect. First thing to be improved would be the features of the images. The training loss and validation loss could be further optimised to return a better trained model. 
Also, instead of the current suggestions which compute both the tops and bottoms individually, the training model can be trained with combined images and respective score to allow a better representation of the outfit display (i.e. adding labels to the training data). In addition, the engine should be able to further rank the outfit with the feedback from the users to improve the existing trained model. 
Lastly, presentation could be improved by displaying a web page by maybe using React instead of displaying with the python standard library tkinker. 

## Acknowledgements
* Thank you to [TheComeUpCode](https://github.com/TheComeUpCode/WardrobeApp/) for inspiration of a random wardrobe.
* Thank you to H.M. website for webscraping
* Thank you to Adrian Rosebrock for the Autoencoder codes
    * Adrian Rosebrock, Autoencoders for Content-based Image Retrieval with Keras and TensorFlow, PyImageSearch, https://www.pyimagesearch.com/2020/03/30/autoencoders-for-content-based-image-retrieval-with-keras-and-tensorflow/, accessed on 14 July 2020

