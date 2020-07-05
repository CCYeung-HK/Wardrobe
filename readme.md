# Wardrobe

Wardrobe is a Python programme to generate random outfit from the csv database
(current data scraped from H.M using BeautifulSoup)


## Current Version

Only worked on Man's clothing. Will scrape more data from woman's section soon for Machine Learning.

## Prerequistes

* Python 2.6 or greater
* pip package management tool

## Local Setup

1. To install all dependencies 
```bash
pip install -r dependencies.txt
```

2. Run the python script
```bash
python play2.py
```

3. Scraping website (Optional)
```bash
python scrape.py
```
(Please scrape with respect and not overshoot with requests to the server)

## ToDoList

1. Implement ML to generate outfit according to the user preference (tinder-like)
(Recommendation welcomed! If you are interested in Machine Learning in Fashion industry please feel free to contact me)
2. Migrate to SQL when needed

## Acknowledgements
* Thank you to [TheComeUpCode](https://github.com/TheComeUpCode/WardrobeApp/) for inspiration.
* Thank you to H.M. website for webscraping

