# This module consists of necessary classes that runs the API's whether through an online API or on file

import purpleair
import json
import urllib.parse
import urllib.request


class API:
    ''' This class builds a url based on passed parameter of a base url '''
    def __init__(self, url: str):
        self._url = url

    def build_search_url(self, search_query: str) -> str:
        ''' this method builds a search url given parameters '''
            
        query_parameters = [('q', search_query), ('format', 'json')]
            
        return self._url + '/search?' + urllib.parse.urlencode(query_parameters)
        
    def build_reverse_url(self, latitude: float, longitude: float) -> str:
        ''' this method builds a search url given parameters '''

        query_parameters = [('format', 'json'), ('lat', str(latitude)), ('lon', str(longitude))]
            
        return self._url + '/reverse?' + urllib.parse.urlencode(query_parameters)
        
    def get_result(self, url: str) -> dict:
        '''
        This method  takes a URL and returns a Python dictionary representing the
        parsed JSON response.
        '''
        response = None

        try:
            # headers = {}
            # key = Referer,
            # https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/YOUR_UCINETID

            # 
            request = urllib.request.Request(url)
            #request.sleep(1)
            response = urllib.request.urlopen(request)
            
            json_text = response.read().decode(encoding = 'utf-8')
            return json.loads(json_text)

        finally:
            if response != None:
                response.close()
    def get_status(self, url: str) -> int:
        '''retrieves thes status of the network '''
        response = None
        try:
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            status = response.getcode()

        except:
            status = 0

        finally:
            if response != None:
                response.close()

        return status
    def check_incorrect_format(self, url: str) -> bool:
        ''' checks to see if the json file is in incorrect format '''
        
        response = None
        
        try:
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            json_text = response.read().decode(encoding = 'utf-8')

            # checks to see if json is empty
            if not json_text:
                return True
            else:
                return False
        except:
            return True
        
        finally:
            if response != None:
                response.close()
    def check_network_error(self, url: str) -> bool:
        response = None
        try:
            response = urllib.request.urlopen(url, timeout=50)
            return False

        except urllib.error.HTTPError:
            return True

        finally:
            if response != None:
                response.close()

            
class Nominatim_API_Data:
    ''' This class handles the nomination file/API methods '''
    def __init__(self, search_result: dict):
        self._search_result = search_result

    # for nomination
    def get_lat(self) -> float:
        ''' retrieves longitude '''
    
        latitude = [i['lat'] for i in self._search_result]
        
        return latitude[0]

    def get_lon(self) -> float:
        ''' retrieves longitude '''
        longitude = [i['lon'] for i in self._search_result]
        return longitude[0]
        
    def get_description(self) -> str:
        '''
        This function takes a parsed JSON response from the nomination api
        search request and prints the location's full description
        '''
        return self._search_result['display_name']


# runs the necessary API searches   
def run_search_center(search_query: str) -> tuple:
    ''' this function runs the search and retrieves the long and lat from OSM'''
    result = API('https://nominatim.openstreetmap.org/')
    url = result.build_search_url(search_query)

    latitude = 0
    longitude = 0
    # validate URL
    status = result.get_status(url)
    incorrect_format = result.check_incorrect_format(url)
    network_error = result.check_network_error(url)

    if status != 200 or incorrect_format or network_error:
        print('FAILED')
        print(status, url)

        print('format', incorrect_format)
        print('network', network_error)
        if status != 200:
            print('NOT 200')
        elif incorrect_format:
            print('FORMAT')
        elif network_error:
            print('NETWORK')

        return latitude, longitude

    # if url is valid, continue finding lat and long
    else:
   
        result = result.get_result(url)
        data = Nominatim_API_Data(result)

        latitude = data.get_lat() 
        longitude = data.get_lon()
    
        return latitude, longitude

def run_search_offline(data_list: list) -> tuple:
    '''
    runs the search function utilizing a json file
    on the hard drive for Nomanatim
    '''
    data = Nominatim_API_Data(data_list)
    latitude = data.get_lat() 
    longitude = data.get_lon()

    return latitude, longitude
    

def run_reverse(latitude: float, longitude: float) -> str:
    ''' this functions runs the reverse geocoding and retrieves the full address'''
    result = API('https://nominatim.openstreetmap.org/')
    url = result.build_reverse_url(latitude, longitude)
    result = result.get_result(url)


    data = Nominatim_API_Data(result)
    
    print(data.get_description())

def run_reverse_offline(paths: str, latitude: float, longitude: float) -> str:
    ''' this functions runs the reverse geocoding and retrieves the full address'''
    result = []
    paths = paths.split(' ')
    
    for i in paths:
        i = i.replace('\\\\', '\\')
        with open(i, encoding= 'utf8') as f:
            d = json.load(f)
            result.append(d)

    for i in result:
        lat = i['lat']
        lon = i['lon']
        # round to 4th decimal place to find a match more easily 
        if round(float(lat),4) == round(float(latitude), 4) and round(float(lon), 4) == round(float(longitude), 4):
            print(i['display_name'])
        

def run_purpleair(threshold: int, max_num: int, miles: int, lat: float, lon: float) -> list:
    ''' retrieves necessary information from the purple air json file online'''
    url = 'https://www.purpleair.com/data.json'
    result = API('https://www.purpleair.com/data.json')
    result = result.get_result(url)
    result = purpleair.run_PURPLEAIR(result, threshold, max_num, miles, lat, lon)
    return result


def run_purpleair_offline(data: dict, threshold: int, max_num: int, miles: int, lat: float, lon: float) -> list:
    result = purpleair.run_PURPLEAIR(data, threshold, max_num, miles, lat, lon)
    return result
    

