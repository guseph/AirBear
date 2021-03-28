import inputs
import purpleair
import api_class
import json
import urllib.parse
import urllib.request


# find center and long/lat for center

    
    
def output_center(lat: str, lon: str) -> None:
    ''' prints the center lat and lon in format of direction '''
    if float(lat) < 0:
        north_or_south = 'S'
        lat = float(lat) * -1
    elif float(lat) >= 0:
        north_or_south = 'N'

    if float(lon) < 0:
        east_or_west = 'W'
        lon = float(lon) * -1
    elif float(lon) >= 0:
        east_or_west = 'E'
        
    print(f'CENTER {lat}/{north_or_south} {lon}/{east_or_west}')

def output_AQI(AQI: int) -> None:
    ''' prints the AQI formatted '''

    print(f'AQI {AQI}')
    
    

def output_results(aqi_input: list, reverse: str) -> None:
    ''' prints the final results '''
    
    for i in aqi_input:
        # output the AQI
        output_AQI(purpleair.calculate_AQI(i[1]))
        # get the lat and lon to find the center
        output_center(i[27], i[28])

        # output the description
        if reverse == 'online':
            api_class.run_reverse(i[27], i[28])
        else:
            api_class.run_reverse_offline(reverse, i[27], i[28])
        

def lat_lon_mode(lat, lon):
  print("LAT LON MODE")
  miles = 25

  aqi_threshold = 0

  max_num = 1

  aqi_data = inputs.input_AQI(int(aqi_threshold), int(max_num),
                          float(miles), float(lat), float(lon))

  if not aqi_data:
    return -1
  
  # 6TH INPUT
  reverse = 'online'
  print("BLAH", lat, lon)
  # OUTPUTS
  # output_center(lat, lon)

  return purpleair.calculate_AQI(aqi_data[0][1])

def addr_mode(addr):
  lat, lon = inputs.input_location_center(addr)

  if lat == 0 and lon == 0:
    return -1

  miles = 25

  aqi_threshold = 0

  max_num = 1

  aqi_data = inputs.input_AQI(int(aqi_threshold), int(max_num),
                          float(miles), float(lat), float(lon))

  if not aqi_data:
    return -1
  
  # 6TH INPUT
  reverse = 'online'

  # OUTPUTS
  # output_center(lat, lon)

  # output_results(aqi_data, reverse)

  return purpleair.calculate_AQI(aqi_data[0][1])
