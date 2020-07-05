from bs4 import BeautifulSoup
import requests
from time import sleep
from random import randint
import urllib.request
import shutil
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}
def webscraping_top(urls):

    image_info = []

    for url in urls: 
        req = requests.get(url , headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(req.content, 'html.parser')

        container = soup.find_all("img", class_="item-image")

        for i in container:
            image_info.append((i.get("data-src"), i.get("alt")))

    image_url = []
    image_alt = []

    for image in image_info:
        image_url.append('http:' + image[0])
        image_alt.append(image[1])
    
    tops_df = pd.DataFrame({
        'Description': image_alt,
        'Image_url': image_url
    })

    tops_df.to_csv("man_tops.csv")


def webscraping_bottoms(urls):

    image_info = []

    for url in urls: 
        req = requests.get(url , headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(req.content, 'html.parser')

        container = soup.find_all("img", class_="item-image")

        for i in container:
            image_info.append((i.get("data-src"), i.get("alt")))

    image_url = []
    image_alt = []

    for image in image_info:
        image_url.append('http:' + image[0])
        image_alt.append(image[1])
    
    tops_df = pd.DataFrame({
        'Description': image_alt,
        'Image_url': image_url
    })

    tops_df.to_csv("man_bottoms.csv")
    



    # def download_image(image, number):
    #     response = requests.get('http:'+image[0], stream=True)
    #     realname = ''.join(e for e in image[1] if e.isalnum()) + str(number)
    
    #     file = open("C://Users//chris//Desktop//Play//tops//{}.jpg".format(realname), 'wb')
    
    #     response.raw.decode_content = True
    #     shutil.copyfileobj(response.raw, file)
    #     del response

    # for i in range(0, len(image_info)):
    #     sleep(randint(2,5))
    #     download_image(image_info[i], i)

# def webscraping_bottom(url):

#     req = requests.get(url , headers={'User-Agent': 'Mozilla/5.0'})
#     soup = BeautifulSoup(req.content, 'html.parser')

#     container = soup.find_all("img", class_="item-image")

#     image_info = []

#     for i in container:
#         image_info.append((i.get("data-src"), i.get("alt")))

#     def download_image(image, number):
#         response = requests.get('http:'+image[0], stream=True)
#         realname = ''.join(e for e in image[1] if e.isalnum()) + str(number)
    
#         file = open("C://Users//chris//Desktop//Play//bottoms//{}.jpg".format(realname), 'wb')
    
#         response.raw.decode_content = True
#         shutil.copyfileobj(response.raw, file)
#         del response

#     for i in range(0, len(image_info)):
#         sleep(randint(2,5))
#         download_image(image_info[i], i)

urls_top = [
    'https://www2.hm.com/en_gb/men/shop-by-product/t-shirts-and-vests.html?product-type=men_tshirtstanks&sort=stock&image-size=small&image=model&offset=0&page-size=396',
    'https://www2.hm.com/en_gb/men/shop-by-product/hoodies-sweatshirts.html?product-type=men_hoodiessweatshirts&sort=stock&image-size=small&image=model&offset=0&page-size=72',
    'https://www2.hm.com/en_gb/men/shop-by-product/jackets-and-coats.html?product-type=men_jacketscoats&sort=stock&image-size=small&image=model&offset=0&page-size=83',
    'https://www2.hm.com/en_gb/men/shop-by-product/shirts.html?product-type=men_shirts&sort=stock&image-size=small&image=model&offset=0&page-size=233',
    'https://www2.hm.com/en_gb/men/shop-by-product/cardigans-and-jumpers.html?product-type=men_cardigansjumpers&sort=stock&image-size=small&image=model&offset=0&page-size=72'
    ]

urls_bottoms = [
    'https://www2.hm.com/en_gb/men/shop-by-product/trousers.html?product-type=men_trousers,men_trousers_trousers,men_trousers_chinos,men_trousers_all,Trousers_men_trousers_joggers,men_trousers_joggers,men_trousers_newarrivals,men_trousers_cargo,men_trousers_dressed,men_trousers_casual&sort=stock&image-size=small&image=model&offset=0&page-size=190',
    'https://www2.hm.com/en_gb/men/shop-by-product/jeans.html?product-type=men_jeans&sort=stock&image-size=small&image=model&offset=0&page-size=82'
    ]

webscraping_bottoms(urls_bottoms)