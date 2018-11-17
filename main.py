import ecobee
import firebase

if ecobee.validTokenCheck(): # We have a valid token
  print('Pyrate is authenticated and is reading temperature data.')
else:
  print('Pyrate needs to be added as an authorised app to your Ecobee '
        'account.')
  token = ecobee.initialAuth() # Get the token
  ecobee.storeToken(token) # Store the token
  
thermostat_output = ecobee.thermostatRequest() # Make the API call
temps = ecobee.parseTemperatures(thermostat_output)
firebase.storeTemperatures(temps)
all_temperatures = firebase.getRoomTemperatures('Bedroom', 15)
for temp_value in all_temperatures:
  print(u'{} => {}'.format(temp_value.id, temp_value.to_dict()))