import requests
from BeautifulSoup import BeautifulSoup
import pickle
from collections import defaultdict

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


def read_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    find_section = soup.findAll('section', attrs={"id": "postingbody"})
    text = find_section[0].findAll(text=True)
    clean_text = ' '.join(text)
    return clean_text


def flag_score(url):
    post = read_url(url)
    result = classifier.prob_classify(feature_extractor(post))
    score = round(result.prob('flag'), 2)*100
    return score


def flag_score_post(post):
    result = classifier.prob_classify(feature_extractor(post))
    score = round(result.prob('flag'), 2)*100
    return score

