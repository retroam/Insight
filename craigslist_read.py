from os import listdir
from collections import Counter
import json
import urllib2
import requests
from BeautifulSoup import BeautifulSoup
import matplotlib.pyplot as plt




files = listdir('./data_dump')
print files
flag_message = 'This posting has been flagged for removal.[?]'
no_flag = {}
flag = {}
for i in range(50):
    print i
    with open('./data_dump/' + files[i + 1]) as f:
        my_dict = json.load(f)


        for j in range(100):
            url = my_dict['postings'][j]['external_url']
            id = my_dict['postings'][j]['id']
            body = my_dict['postings'][j]['body']
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text)
                tag = soup.find('h2').text
                if tag == flag_message:
                    flag[id] = body
                else:
                    no_flag[id] = body
            except:
                print 'error'
        f.close()


words_flag = [w for id in flag
                  for w in flag[id].split()]

words = [w for id in no_flag
                  for w in no_flag[id].split()]

word_counts = sorted(Counter(words_flag).values(), reverse=True)
plt.loglog(word_counts)
plt.ylabel('Freq')
plt.xlabel('Word Rank')
plt.savefig('./Images/flag')

word_counts = sorted(Counter(words).values(), reverse=True)
plt.loglog(word_counts)
plt.ylabel('Freq')
plt.xlabel('Word Rank')
plt.savefig('./Images/no_flag')


name = 'words_flag.json'
with open(name, 'w') as outfile:
    json.dump({words_flag}, outfile)

name = 'words.json'
with open(name, 'w') as outfile:
    json.dump({words}, outfile)