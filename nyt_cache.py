### Lecture 8 Exercise: Web APIs and Caching
### Zheyi Tian, tzheyi, 36521510

from secrets import * # Import everything from secrets.py
from datetime import datetime # For Cache expiration
import requests
import json

#Try cache first, is there is a json file.
CACHE_FNAME = 'cache_file_name.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}


def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res) 
# input params is a dict.
# str.join(list), output a string, with str added between each elements of list. The types of elements of lists should be <str>.
# Used as a key in CACHE_DICTION


MAX_STALENESS = 30  # 30 seconds

def is_fresh(cache_entry):
    now = datetime.now().timestamp()
    staleness = now - cache_entry['cache_timestamp']
    return staleness < MAX_STALENESS 
    # The returned value is a Boolean.


def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    if unique_ident in CACHE_DICTION:
        if is_fresh(CACHE_DICTION[unique_ident]): 
            print("Getting cached data...")
            return CACHE_DICTION[unique_ident]
    else:
        pass #It seems to me that this 2 lines can be deleted.

    print("Making a request for new data...")
    resp = requests.get(baseurl, params)   # requests.get(baseurl, params)
    CACHE_DICTION[unique_ident] = json.loads(resp.text)    # json.loads(resp.text)
    CACHE_DICTION[unique_ident]['cache_timestamp'] = datetime.now().timestamp() 
    #Because the format of cache file changed, delete the old cache file first.
    dumped_json_cache = json.dumps(CACHE_DICTION)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json_cache)
    fw.close() # Update the CACHE_FNAME
    return CACHE_DICTION[unique_ident]


def get_stories(section):
    baseurl = 'https://api.nytimes.com/svc/topstories/v2/'
    extendedurl = baseurl + section + '.json'
    params={'api-key': nyt_key} #nyt_key is imported from secrets.py
    return make_request_using_cache(extendedurl, params)

def get_headlines(nyt_results_dict):
    results = nyt_results_dict['results']
    headlines = []
    for r in results:
        headlines.append(r['title'])
    return headlines

story_list_json = get_stories('science')
headlines = get_headlines(story_list_json)
for h in headlines:
    print(h)