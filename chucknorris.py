import json
import random
import urllib.request
import urllib.parse
 

CN_SEARCH_URL = 'https://api.chucknorris.io/jokes/search?query='

def get_joke_dict(query: str) -> dict:
            
    url = CN_SEARCH_URL + urllib.parse.quote(query)
    response = None
    try:
        print(url)      
        response = urllib.request.urlopen(url)
        print(response)
        joke_dict = json.load(response)
                    
        if joke_dict == {}:
            return None
        else:
            return joke_dict
    except (urllib.error.HTTPError, urllib.error.URLError):
        return None
    finally:
        if response != None:
            response.close()
            
def get_random_joke(joke_dict: dict) -> str:
    '''
    Getes a random joke from the joke_dict
    '''
    joke = random.choice(joke_dict['result'])
    return joke['value']


joke_dict = get_joke_dict('animal')
if joke_dict != None:
    print(get_random_joke(joke_dict))
else:
    print('error')
