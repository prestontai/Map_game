import random
import urllib.request
import json
import urllib.parse
import codes

URL_START = 'https://en.wikipedia.org/w/api.php?action=query&titles='
URL_END = '&prop=revisions&rvprop=content&format=json&formatversion=2'
LETTER_LIST = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def get_info (url:str) -> dict:
    response = None
    try:
        response = urllib.request.urlopen(url)
        return json.load(response)
    except:
        pass
    finally:
        if response != None:
            response.close()

def get_city() -> list:
    letter = random.choice(LETTER_LIST)
    url = URL_START + 'List_of_towns_and_cities_with_100%2C000_or_more_inhabitants%2Fcityname%3A_' + letter + URL_END
#     url = URL_START + 'List_of_urban_areas_by_population' + URL_END
    response = get_info(url)
    ret_string = response['query']['pages'][0]['revisions'][0]['content']
    ret_string = ret_string.replace(']]', '').replace(
        '\n', '').replace('|-', '').replace('==See also==*', 
        '').replace('|', ',').replace('{', '').replace('}', '')
    return ret_string.split('[[')

def get_coords(city_name:str)->list:
    url = URL_START + urllib.parse.quote(city_name) + URL_END
    response = get_info(url)
    ret_string = response['query']['pages'][0]['revisions'][0]['content']
    fun_fact = ret_string.split('==')[6].split('.')[0].strip('=')
    if 'File' not in fun_fact and 'image' not in fun_fact:
        return (ret_string, fun_fact)
    return (ret_string, '')

# def get_country_name():
#     url = 'https://en.wikipedia.org/w/api.php?action=query&titles=ISO_3166-1_alpha-3&prop=revisions&rvprop=content&format=json&formatversion=2'
#     response = get_info(url)
#     ret_string = response['query']['pages'][0]['revisions'][0]['content'].split('mono')[1:]
#     for i in ret_string:
#         if 'mono' in ret_string:
#             print(i)
#     print(ret_string)

def all()->bool:
#     get_country_name()
    city_list = []
    for i in get_city()[2:-4]:
        if not i.startswith('File:'):
            city_list.append((i[:-7].split(',')[0], i.split(',')[-2].strip(' ')))
    city_tup = random.choice(city_list)
    city_name = city_tup[0]
    country = city_tup[1]
#     print(country)
    ret_info = get_coords(city_name)
    fun_fact = ret_info[1]
    lat_long = ret_info[0]
    for coords in lat_long.split('\n'):
        if 'coordinates' in coords and 'coor_type' not in coords and len(coords.split('|')) != 2:
            coords = coords.split('|')
            coord_list = []
            for item in coords:
                if 'N' == item or 'W' == item or 'E' == item or 'S' == item:
                    coord_list.append(item)
                else:
                    try:
                        assert(type(int(item)) == int)
                        coord_list.append(item)
                    except:
                        pass
            if coord_list == [] or len(coord_list) == 2:
                return (True, city_name, coord_list)
            return (False, city_name, country, coord_list, fun_fact)
    
def create_count(country:str)->list:
    country_list = [country]
    
    for num in range(10):
        country = random.choice(codes.random_country)
        country_list.append(country)

    return sorted(country_list, key = lambda x:x[int(random.random()*3)])
    
if __name__ == '__main__':
    score = 0
    streak = 0
    try: 
        start_round = ''
        while start_round == '':
            start_round = input('Press enter to play or enter quit to end\n')
            assert(start_round.lower() != 'quit')
            valid = True
            while valid == True:
                try:
                    ret_tuple = all()
                    valid = ret_tuple[0]
                    city_name = ret_tuple[1]
                    country = ret_tuple[2]
                    coords = ret_tuple[3]
                    fun_fact = ret_tuple[4]
                except:
                    pass
                    
            print('City name:', city_name)
            print('Latitude and Longitude:', coords)
            for fun in fun_fact.split(','):
                print(fun)
            print("Enter one of the countries", create_count(country))
            country_input = input('\nEnter the country or enter quit to end\n')
            assert(country_input.lower() != 'quit')
            if country in  country_input.upper() and len(country_input) <6:#country_input in acronym_dict and acronym_dict[country_input] == country:
                score += 1 + streak
                streak += 1
                print("You're correct!")
            else:
                score -= 3
                streak = 0
                print('Correct answer was', country)
            print('SCORE =', score, 'You got', streak,'right in a row')
    except AssertionError:
        if score <= -6:
            print('Bye Bye, your score was', score, "That's not that great :(")
        else:
            print('Bye Bye, your score was', score)



