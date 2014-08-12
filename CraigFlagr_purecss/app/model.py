import requests
from BeautifulSoup import BeautifulSoup
import pickle
from collections import defaultdict
from gmaps import Geocoding

PICKLE_FILE = '/Users/robertamanfu/Documents/Insight/Project/craigslist_classifier.pickle'
f = open(PICKLE_FILE)
classifier = pickle.load(f)


def get_post_words(post, stopwords = []):
    pwords = [w for w in post.split() if not w in stopwords]
    return pwords


def feature_extractor(post):
    features = defaultdict(list)
    post_word = get_post_words(post)
    for w in post_word:
        features[w] = True
    return features


def get_zip(loc):
    latitude = loc[0].get('data-latitude')
    longitude = loc[0].get('data-longitude')
    google_api = Geocoding()
    map_loc = google_api.reverse(float(latitude), float(longitude))
    code = 'USA-' + map_loc[0]['address_components'][8]['long_name']
    return code


def read_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    find_section = soup.findAll('section', attrs={"id": "postingbody"})
    text = find_section[0].findAll(text=True)
    clean_text = ' '.join(text)

    find_loc = soup.findAll('div', attrs={"id": "map"})
    zipcode = get_zip(find_loc)

    return clean_text, zipcode, post_id


def flag_score(url):
    post, _ = read_url(url)
    result = classifier.prob_classify(feature_extractor(post))
    score = round(result.prob('flag'), 2)*100
    return score


def flag_score_post(post):
    result = classifier.prob_classify(feature_extractor(post))
    score = round(result.prob('flag'), 2)*100
    return score

