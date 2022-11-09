## Import packages 
import pip._vendor.requests as requests
import pandas as pd
from datetime import datetime

## define variables needed for all functions
api_key = 'AgBiJtYweO2YqUCaDeNV05h1bMA3fTkI6LdeMhXr'

headers = {
    'accept': 'application/json',
    'x-api-key': api_key,
}



#### Required parameters:
# lat: latitude of the center point for the region of interest
# longt: longitude of the center point for the region of interest
#### optional parameters: 
# age: hours ago the latest vessel position reports were received (must be between 1 - 2160) --default 2160
# number of statute miles to search for vessels (must be between 1 - 100) --default 100
def get_vessels(lat, longt, age=2160, radius=100):
  vessels_url = "https://api.seavision.volpe.dot.gov/v1/vessels"
  api_key = 'AgBiJtYweO2YqUCaDeNV05h1bMA3fTkI6LdeMhXr'
  headers = {
    'accept': 'application/json',
    'x-api-key': api_key,
  }
  params = {
    'latitude': lat,
    'longitude': longt,
    'age': age,
    'radius': radius,
  }
  response = requests.get(vessels_url, params=params, headers=headers)
  result = pd.read_json(response.text)
  ## convert timestamp to datetime and append an additional column to the dataframe
  result['time'] = pd.to_datetime(result['timeOfFix'], unit='s')
  return result


  #### Required parameter:
# mmsi: vesselid --MMSI associated to the vessel to acquire historical position data for
#### Optional prameter:
# age: number of days back the history will cover (1- 90 days) -default set to 90 days
# time: start time for history of vessel search to begin with (time can be up to 2 years old) --- not implement yet
def get_vessel_history(mmsi, age= 90):
  vessel_history_url = 'https://api.seavision.volpe.dot.gov/v1/vessels/'+ str(mmsi)+'/history'
  headers = {
    'accept': 'application/json',
    'x-api-key': api_key,
  }
  params = {
    'age': age,
  }
  response = requests.get(vessel_history_url, params=params, headers=headers)
  result = pd.read_json(response.text)
  ## convert timestamp to datetime and append an additional column to the dataframe
  result['time'] = pd.to_datetime(result['timeOfFix'], unit='s')
  result['mmsi'] = mmsi
  return result






