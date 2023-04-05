import requests
import datetime
import time
import variables


def get_iss_lat_lng() -> (str, str):
    """
    Returns the latitude and longitude of the ISS as a tuple
    :return: latitude and longitude
    """
    response = requests.get('http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    data = response.json()
    lat = float(data['iss_position']['latitude'])
    lng = float(data['iss_position']['longitude'])
    return lat, lng


def is_it_nighttime() -> bool:
    """
    Returns True if the current time (now) is between sunset and sunrise
    :return: bool
    """
    params = {'lat': variables.LAT, 'lng': variables.LON, 'formatted': 0}
    response = requests.get('https://api.sunrise-sunset.org/json', params=params)
    response.raise_for_status()
    data = response.json()
    sunrise = datetime.datetime.fromisoformat(data['results']['sunrise']).time()
    sunset = datetime.datetime.fromisoformat(data['results']['sunset']).time()
    now = datetime.datetime.now().time()
    return sunset < now < sunrise


print(f'Current location lat: {variables.LAT}, lon: {variables.LON}.')
print()
while True:
    latitude, longitude = get_iss_lat_lng()
    print(f'ISS location lat: {latitude}, lon: {longitude}.')
    if variables.LAT - 5 <= latitude <= variables.LAT + 5 \
            and variables.LON - 5 <= longitude <= variables.LON + 5 \
            and is_it_nighttime():
        print('Near latitude and longitude and it is nighttime. Look up!')
    else:
        print('Sorry, the ISS is too far away or it is not yet nighttime.')
    time.sleep(5)
