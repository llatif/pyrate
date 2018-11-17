"""
  ecobee.py - v0.6

  This script authenticates with the Ecobee server, gets an auth token and
  stores it.
"""

import datetime
import json
import requests
import shelve
import os

# API Key
api_key = 'ECOBEE_API_KEY'

# Use Shelve for persistent key storage
auth_file = shelve.open(str(os.getcwd()) + '/ecobee.token')

def initialAuth():
  """
    Auth request payload
    The scope for this request is smartRead - we only want to read data not set
    thermostat controls
  """
 
  auth_payload = {'response_type': 'ecobeePin',
                  'client_id': api_key,
                  'scope': 'smartWrite'} # TODO: Change this to smartRead

  pin_request = requests.get('https://api.ecobee.com/authorize', params=auth_payload)

  ecobee_auth_output = json.loads(pin_request.text) # Catch the r.json exception

  """
  From the payload above we want
  1) ecobeePin - display to the user
  2) code - this is passed onto the token request
  """

  auth_code = ecobee_auth_output['code']
  print ('Pin: ', ecobee_auth_output['ecobeePin'])

  input("Press Enter to continue.") # Wait until the pin is entered in the portal

  # Token request payload
  request_payload = {'grant_type': 'ecobeePin',
                    'code': auth_code,
                    'client_id': api_key}

  token_request = requests.post('https://api.ecobee.com/token', request_payload)
  token_output = json.loads(token_request.text)

  return token_output

def refreshToken():
  """
    Refreshes an expired token
  """

  request_payload = {'grant_type': 'refresh_token',
                    'code': auth_file['refresh_token'],
                    'client_id': api_key}
  
  token_request = requests.post('https://api.ecobee.com/token', request_payload)
  token_output = json.loads(token_request.text)

  storeToken(token_output) # Update the token information

def storeToken (token):
  """
    Store the auth token
  """

  auth_file['access_token'] = token['access_token']
  auth_file['token_type'] = token['token_type']
  auth_file['expiration'] = datetime.datetime.now() + datetime.timedelta(minutes=int(token['expires_in']))
  auth_file['refresh_token'] = token['refresh_token']

def thermostatRequest():
  """
    Makes the request to the Ecobee API to get thermostat data
  """

  # Create the headers
  auth_header = 'Bearer '+ auth_file['access_token']

  headers = {'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': auth_header }

  api_url = 'https://api.ecobee.com/1/thermostat'

  # Build the request
  thermostat_request_payload = {"selection":{
                                  "includeAlerts":"",
                                  "selectionType":"registered",
                                  "selectionMatch":"",
                                  "includeEvents":"",
                                  "includeSettings":"",
                                  "includeSensors":"true",
                                  "includeRuntime":""
                                }}

  thermostat = requests.get(api_url, params = {'json': json.dumps(thermostat_request_payload)}, headers=headers)
  thermostat_info = json.loads(thermostat.text)

  return thermostat_info

def validTokenCheck():
  """
    Check to see if we have a valid token.
    
    If a token exists, then check if it needs refreshing. If it does, then
    refresh.
    If the token is not valid then we need to re-auth
  """

  if 'refresh_token' in auth_file:
    refreshToken()
    return True
  else:
    return False

def parseTemperatures(requestOutput):
  """
    Extract temperature and humidity data from sensors then return them in a
    dictionary
  """
  # CYCLE THROUGH DATASTRUCTURE AND RETURN ALL SENSORNAME + TEMP TUPLES

  temps = dict()

  for sensors in requestOutput['thermostatList'][0]['remoteSensors']:
    temps.update({sensors['name']:sensors['capability'][0]['value']})
  
  return temps