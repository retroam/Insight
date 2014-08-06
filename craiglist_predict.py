import json
import random
from nltk import NaiveBayesClassifier, classify
from collections import defaultdict
import requests
from BeautifulSoup import BeautifulSoup
import pickle


def get_post_words(post, stopwords = []):
    pwords = [w for w in post.split()
              if not w in stopwords]
    return pwords


def features_from_posts(posts, label, feature_extractor):
    features_labels = []
    for post in posts:
        features = feature_extractor(post)
        features_labels.append((features,label))
    return features_labels


def feature_extractor(post):
    features = defaultdict(list)
    post_word = get_post_words(post)
    for w in post_word:
        features[w] = True
    return features


def read_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    find_meta = soup.findAll('meta', attrs={"name": "description"})
    content = find_meta[0]['content']
    return content
#Simple Naive Bayes classifier

#Load files
json_file = open('./flag.json')
flag = json.load(json_file)
json_file = open('./no_flag.json')
no_flag = json.load(json_file)

#Parse posts into list
no_flag_list = [no_flag['result'][idx] for idx in no_flag['result']]
flag_list = [flag['result'][idx] for idx in flag['result']]
flag_posts = [(post, 'flag') for post in flag_list]
no_flag_posts = [(post, 'no_flag') for post in no_flag_list[:len(flag_list)]]


#Create feature sets
posts = flag_posts + no_flag_posts
random.shuffle(posts)
featuresets = [(feature_extractor(post), flag_status)
               for (post, flag_status) in posts]
data_size = len(featuresets)
train_set, test_set = featuresets[data_size/2:], featuresets[:data_size/2]

#Run NaiveBayes algorithm

classifier = NaiveBayesClassifier.train(train_set)
print classify.accuracy(classifier, test_set)
classifier.show_most_informative_features(5)

post = read_url('http://newyork.craigslist.org/mnh/sub/4590104096.html')
result = classifier.prob_classify(feature_extractor(post))

print round(result.prob('flag'), 2)*100
print classifier.classify(feature_extractor(post))

f = open('craigslist_classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()