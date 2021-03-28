# Calls to read user inputs

import api_class
import json

def _read_user_input() -> str:
    ''' reads the user inputs that aren't empty strings'''

    # CENTER NOMINATION {location}
    # {location} any non empty string reading the center point of analysis
    while True:
        try:
            user_input = input()
            if not user_input:
                raise ValueError
            else:
                break
        except ValueError:
            print('Please input a valid input')
            
    return user_input

def input_location_center(addr) -> tuple:
    ''' finds the lat and long (center) with user's given location '''
    user_input = addr
    # initialize variable
    latitude = 0
    longitude = 0
    if user_input.startswith('CENTER NOMINATIM '):
        
        center = _get_location(user_input)
        center = center.replace(',', '')
        latitude, longitude = api_class.run_search_center(center)
        
        
        return latitude, longitude

    elif user_input.startswith('CENTER FILE '):
        while True:
            try:
                d = ''
                # FIND FILE PATH DIRECTORY
                center = _get_path(user_input)
                with open(center, encoding = 'utf8') as f:
                    d = json.load(f)
                
                latitude, longitude = api_class.run_search_offline(d)
                
        
            except:
                print('FAILED')
                print(center)
                if d == ' ':
                    print('FORMAT')
                else:
                    print('MISSING')
                
            finally:
                break
                
                
        return latitude, longitude
   


def input_integer() -> int:
    '''
    retrieves user's inputted integers and reads the user line
    to determine what value to store in a variable for either miles
    AQI or max
    '''
    user_input = _read_user_input()
    
    if user_input.startswith('RANGE '):
        int_value = _get_miles(user_input)

    elif user_input.startswith('THRESHOLD '):
        int_value = _get_AQI(user_input)

    elif user_input.startswith('MAX '):
        int_value = _get_number(user_input)


    return int_value
    
def input_AQI(threshold: int, max_num: int,
              miles: int, lat: float, lon: float) -> list:
    ''' returns user selection '''
    result = []
    user_input = _read_user_input()
    if user_input.startswith('AQI PURPLEAIR'):
        result = api_class.run_purpleair(threshold, max_num, miles,
                           lat, lon)
    elif user_input.startswith('AQI FILE '):
        # FIND FILE PATH DIRECTORY
        while True:
            try:
                value = _get_AQI_path(user_input)
                with open(value, encoding= 'utf8') as f:
                    d = json.load(f)
                result = api_class.run_purpleair_offline(d,threshold,
                                                         max_num, miles,lat, lon)
            except:
                print('FAILED')
                print(value)
                print('MISSING')
                if d == '':
                    print('FORMAT')
            finally:
                break

        
    return result

def input_reverse() -> str:
    ''' returns user selection '''
    user_input = _read_user_input()
    if user_input == 'REVERSE NOMINATIM':
        value = 'online'
    elif user_input.startswith('REVERSE FILES '):
        value = _get_reverse_files(user_input) # prints a string of path

    return value


# FIRST LINE OF INPUT IN ONE OF THE TWO FORMATS
def _get_location(user_input: str) -> str:
    '''
    retrieves location from user input
    if this line of input said CENTER NOMINATIMBren Hall Irvine,
    CA, the center of our analysis is Bren Hall on the campus of UC Irvine. 
    '''


    return user_input.replace('CENTER NOMINATIM ', '')

def _get_path(user_input: str) -> str:
    '''
    The expectation is the file will contain data in the same format
    that Nominatim would've given you, but will allow you to test your work
    without having to call the API every time
    '''

    return user_input.replace('CENTER FILE ', '')

# SECOND LINE OF INPUT IN FOLLOWING FORMAT
def _get_miles(user_input: str) -> int:
    '''
    retrieves the miles
    For example, if this line of input said RANGE 30,
    then the range of our analysis is 30 miles from the center location
    '''
    
    user_input = user_input.replace('RANGE ', '')

    return int(user_input)

# THIRD LINE OF INPUT IN FOLLOWING FORMAT
def _get_AQI(user_input: str) -> float:
    '''
    a positive integer specifying the AQI threshold, which means
    we're interested in finding places that have AQI values at least as high as the threshold.
    It is
    safe to assume that the AQI threshold is non-negative, though it could be
    zero
    '''

    user_input = user_input.replace('THRESHOLD ', '')

    return int(user_input)

# FOURTH LINE OF INPUT IN FOLLOWING FORMAT
def _get_number(user_input: str) -> int:
    '''
    for example, if this line of input said MAX 5, then we're looking for up to five locations
    where the AQI value is at or above the AQI threshold
    '''
    
    user_input = user_input.replace('MAX ', '')

    return int(user_input)
    
# FIFTH LINE OF INPUT IN ONE OF THE TWO FORMATS
def _get_PURPLEAIR(user_input: str) -> str:
    '''
    AQI PURPLEAIR which means that we want to obtain our air quality information
    from PurpleAir's API with all of the sensor data in it
    '''
    return user_input

def _get_AQI_path(user_input: str) -> str:
    '''
    where path is the path to a file on your hard drive containing the result of a
    previous call to PurpleAir's API with all of the sensor data in it.
    '''
    user_input = user_input.replace('AQI FILE ', '')

    return user_input

# SIXTH LINE OF INPUT IN ONE OF THE TWO FORMATS
def _get_reverse(user_input: str):
    '''
    which means that we want to use the Nominatim API to do reverse geocoding, i.e., to
    determine a description of where problematic air quality sensors are located
    '''
    return True

def _get_reverse_files(user_input: str) -> str:
    '''
    which means that we want to use files stored on our hard drive containing the results
    of previous calls to Nominatim's reverse geocoding API instead. Paths are separated by
    spaces - which means they CAN'T CONTAIN spaces — and we expect there to be as many paths
    listed as the number we passed to MAX (e.g., if we said MAX 5 previously, then we'd
    specify five files containing reverse geocoding data)
    '''
    user_input = user_input.replace('REVERSE FILES ', '')

    return user_input


    
    
    
