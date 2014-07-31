import threetaps
import urllib2
from BeautifulSoup import BeautifulSoup
import json

API_KEY = '082906284971364c1cb52da644536e37'
client = threetaps.Threetaps(API_KEY)

response = client.search.search(params={'source': 'CRAIG',
                                        'retvals': 'external_url,body,heading',
                                        'sort': 'timestamp',
                                        'rpp': 100})

with open('example_response.txt', 'w') as outfile:
    json.dump(response, outfile)

urls = [response['postings'][i]['external_url'] for i in range(100)]
print urls[0]

url_tag = {}
for i in range(100):
    response = urllib2.urlopen(urls[i]).read()
    soup = BeautifulSoup(response)
    tag = soup.find('h2').text
    if tag in url_tag:
        url_tag[tag] += 1
    else:
        url_tag[tag] = 1


print url_tag['This posting has been flagged for removal.[?]']


