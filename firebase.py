import datetime

from google.cloud import exceptions
from google.cloud import firestore

db = firestore.Client() # Create Cloud Firestore client

def storeTemperatures(temps):
  """
    Stores temperatures into a Firestore database
  """

  # We are using batched writes to reduce the number of writes
  batch = db.batch() # Create batch

  for temp in temps:
    temperature_doc = db.collection(temp).document()
    batch.set(temperature_doc,
              {
                u'temp': temps[temp],
                u'time': str(datetime.datetime.now())
              }
             )

  batch.commit() # TODO(llatif) - catch the exception

def getAllTemperatures():
  """ 
  Reads the temperature from Cloud Firestore and prints it out.
  """

  all_temps = db.collection('temperatures')
  temperatures = all_temps.get()

  return temperatures

def getRoomTemperatures(room, resultLimit):
  """
  Get temperatuers of a specific room
  """

  try:
     #temperatures = db.collection(room).where(u'temp', u'>', u'0').order_by(u'temp', direction=firestore.Query.DESCENDING).limit(10).get()
    temperatures = db.collection(room).order_by(u'time', direction=firestore.Query.DESCENDING).limit(resultLimit).get()
    return temperatures
  except exceptions.NotFound:
    print(u'No such document!')