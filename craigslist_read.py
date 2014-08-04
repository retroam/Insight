from os import listdir
from collections import Counter
import json
import urllib2
import requests
from BeautifulSoup import BeautifulSoup
import matplotlib.pyplot as plt


files = listdir('./data_dump')

flag_message = 'This posting has been flagged for removal.[?]'
no_flag = {}
flag = {}
for i in range(1, len(files)):
    print i
    with open('./data_dump/' + files[i]) as f:
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
print "Number of normal posts:" + str(len(no_flag))
print "Number of flagged posts:" + str(len(flag))

words_flag = [w for post_id in flag
              for w in flag[post_id].split()]

words = [w for post_id in no_flag
         for w in no_flag[post_id].split()]

# word_counts = sorted(Counter(words_flag).values(), reverse=True)
# plt.loglog(word_counts)
# plt.ylabel('Freq')
# plt.xlabel('Word Rank')
# plt.savefig('./Images/flag')
#
# word_counts = sorted(Counter(words).values(), reverse=True)
# plt.loglog(word_counts)
# plt.ylabel('Freq')
# plt.xlabel('Word Rank')
# plt.savefig('./Images/no_flag')


name = 'no_flag.json'
file_save = {'result': no_flag}
with open(name, 'w') as outfile:
    json.dump(file_save, outfile)

file_save = {'result': flag}
name = 'flag.json'
with open(name, 'w') as outfile:
    json.dump(file_save, outfile)