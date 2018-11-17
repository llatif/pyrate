import ecobee
import firebase

if ecobee.validTokenCheck(): # We have a valid token
  """
  thermostatOutput = ecobee.thermostatRequest() # Make the API call
  temps = ecobee.parseTemperatures(thermostatOutput)
  firebase.storeTemperatures(temps)
  all_temperatures = firebase.getRoomTemperatures('Bedroom', 15)
  for temp_value in all_temperatures:
    print(u'{} => {}'.format(temp_value.id, temp_value.to_dict()))
  """
else:
  token = ecobee.initialAuth() # Get the token
  ecobee.storeToken(token) # Store the token
  
thermostatOutput = ecobee.thermostatRequest() # Make the API call
temps = ecobee.parseTemperatures(thermostatOutput)
firebase.storeTemperatures(temps)
all_temperatures = firebase.getRoomTemperatures('Bedroom', 15)
for temp_value in all_temperatures:
  print(u'{} => {}'.format(temp_value.id, temp_value.to_dict()))