# purpleair.py

import json
import urllib.parse
import urllib.request
import math
import api_class


class PurpleAir_API_Data:
    ''' This class handles the purpleair json file/API methods '''
    # for purpleair
    def __init__(self, result: list):
        self._result = result
    
    def get_pm(self) -> int:
        ''' retrieves the pm in the list '''
        return self._result[1]

    def get_age(self) -> int:
        ''' retrieves the age in the list '''
        return self._result[4]

    def get_type(self) -> int:
        ''' retrieves the type in the list '''
        return self._result[25]

    def get_lat(self) -> float:
        ''' retrieves the latitude in the list '''
        return self._result[27]

    def get_lon(self) -> float:
        ''' retrieves the longitude in the list '''
        return self._result[28]



def calculate_AQI(pm: float) -> int:
    ''' calculates the AQI given the pm value'''
    if 0 <= pm < 12.1:
        AQI = (pm * 50) / 12

    elif 12.1 <= pm < 35.5:
        AQI = (((pm - 12.1) * 49) / (23.3)) + 51
        
    elif 35.5 <= pm < 55.5:
        AQI = (((pm - 35.5) * 49) / (19.9)) + 101

    elif 55.5 <= pm < 150.5:
        AQI = (((pm - 55.5) * 49) / (94.9)) + 151
        
    elif 150.5 <= pm < 250.5:
        AQI = (((pm - 150.5) * 99) / (99.9)) + 201

    elif 250.5 <= pm < 350.5:
        AQI = (((pm - 250.5) * 99) / (99.9)) + 301

    elif 350.5 <= pm < 500.5:
        AQI = (((pm - 350.5) * 99) / (149.9)) + 401

    elif pm >= 500.5:
        AQI = 501



    # checks to see if the float value is an even number
    # so that round function will work
    if int(AQI) % 2 == 0:
            AQI += 0.00001
    
    return round(AQI)
    

def find_lat_lon(miles: int, center_lat: float, center_lon: float, brng: float) -> tuple:
    R = 3958.8 # in miles
    distance = miles

    # convert lon and lat into 
    lat1 = math.radians(float(center_lat))
    lon1 = math.radians(float(center_lon))

    # find the coordinates
    lat2 = math.asin(math.sin(lat1) * math.cos(distance/R)
                     + math.cos(lat1) * math.sin(distance/R) * math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng)* math.sin(distance/R) * math.cos(lat1),
                              math.cos(distance/R) - math.sin(lat1))
                              

    # convert radians to degrees
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    return lat2, lon2

def _north_boundary(miles: int, center_lat: float, center_lon: float) -> tuple:
    
    return find_lat_lon(miles, center_lat, center_lon, 0)

def _south_boundary(miles: int, center_lat: float, center_lon: float) -> tuple:
    
    return find_lat_lon(miles, center_lat, center_lon, 3.14)
                              
def _east_boundary(miles: int, center_lat: float, center_lon: float) -> tuple:
    
    return find_lat_lon(miles, center_lat, center_lon, 1.57)

def _west_boundary(miles: int, center_lat: float, center_lon: float) -> tuple:
    
    return find_lat_lon(miles, center_lat, center_lon, 4.71239)


                              
def create_results_boundary(search_result: dict, miles: int, center_lat: float, center_lon: float) -> list:
    '''
    This function creates a list where the values are all of the
    results within the long and lat boundaries
    '''

    # get north coordinates
    north_x, north_y = _north_boundary(miles, center_lat, center_lon)
    # get south coordinates
    south_x, south_y = _south_boundary(miles, center_lat, center_lon)
    # get east coordinates
    east_x, east_y = _east_boundary(miles, center_lat, center_lon)
    # get west coordinates
    west_x, west_y = _west_boundary(miles, center_lat, center_lon)

    # boundaries that will matter
    # range from south_x to north_x (least to greatest) for lat
    # range from west_y to east_y (least to greatest) for lon
    result = []

    # in this case, should be looking for given range for lat and lon
    # skip over any list with a 'Type'[25] value of 1 (skip indoor sensors)
    for item in search_result['data']:
        list_result = PurpleAir_API_Data(item)
        latitude = list_result.get_lat()
        longitude = list_result.get_lon()

        # skips the none types for lat and lon
        if latitude != None and latitude != 'null' and longitude != None and longitude != 'null':
            if latitude >= south_x and latitude <= north_x and longitude >= west_y and longitude <= east_y:
                result.append(item)
            
            
    return result 

def _skip_type_indoors(result: list) -> list:
    ''' this function finds all indoor sensors and removes it from the list '''

    new_result = []
    
    for i in result:
        list_result = PurpleAir_API_Data(i)
        ind_or_out = list_result.get_type()
        # skips the 'None' values
        if ind_or_out != None and ind_or_out != 'null':
            if ind_or_out != 1:
                new_result.append(i)
            
        
    return new_result
            
        
def _skip_age_hour(result: list) -> list:
    '''
    this function finds all sensors that hasn't reported within an hour and
    removes it from the list
    '''
    new_result = []
    # age is in seconds
    for i in result:
        list_result = PurpleAir_API_Data(i)
        age = list_result.get_age()
        if age != None and age != 'null':
            if age <= 3600:
                new_result.append(i)
            
        
    return new_result

def _skip_below_threshold(result: list, threshold: int) -> list:
    '''
    this function finds all sensors that is below the given threshold and
    removes it from the list
    '''
    new_result = []
    # have to convert pm into AQI
    for i in result:
        list_result = PurpleAir_API_Data(i)
        pm = list_result.get_pm()
        if pm != None and pm != 'null':
            AQI = calculate_AQI(pm)
            if AQI >= threshold:
                new_result.append(i)
            
        
    return new_result
    
    
    
def reduced_results_list(result: list, threshold: int) -> list:
    ''' reduces the created boundary list by removing unneeded items '''
    result = _skip_type_indoors(result)
    result = _skip_age_hour(result)
    result = _skip_below_threshold(result, threshold)

    return result

def _take_AQI(elem):
    ''' this function is a key for the ascending_order function '''
    AQI = calculate_AQI(elem[1])
    return AQI

def ascending_order(result: list) -> list:
    '''
    this function returns the list in ascending order based on the AQI value
    key
    '''

    result.sort(key=_take_AQI)

    return result

def final_matches(result: list, max_num: int) -> list:
    '''
    this function returns the final list after putting it
    in descending order and skipping over unneeded values
    '''
    result.reverse()
    result = result[0:max_num]

    return result



def run_PURPLEAIR(result: dict, threshold: int, max_num: int, miles: int, lat: float, lon: float) -> list:
    '''
    gathers the needed data from the online purpleair json file
    and returns the necessary list for later output
    '''
    result = create_results_boundary(result, miles, lat, lon) 
    result = reduced_results_list(result, threshold) # creates a list
    result = ascending_order(result)
    result = final_matches(result, max_num) 

    return result
    
