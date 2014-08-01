import threetaps
import json

API_KEY = '082906284971364c1cb52da644536e37'
client = threetaps.Threetaps(API_KEY)

anchor = 1258324525

retvals = ['id', 'account_id', 'source', 'category', 'category_group', 'location',
           'external_id', 'external_url', 'heading', 'body', 'timestamp', 'timestamp_deleted',
           'expires', 'language', 'price', 'currency', 'images', 'annotations', 'status',
           'state', 'immortal', 'deleted', 'flagged_status']


number_files = 1000

for i in range(number_files):
    print str(i)
    response = client.search.search(params={'source': 'CRAIG',
                                            'retvals':','.join(retvals),
                                            'sort': 'timestamp',
                                            'status': 'for_rent',
                                            'anchor': str(anchor),
                                            'rpp': 100, })
    name = 'File' + str(i) + '.json'
    with open(name, 'w') as outfile:
        json.dump(response, outfile)
