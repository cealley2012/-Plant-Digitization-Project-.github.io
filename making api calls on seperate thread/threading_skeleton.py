# Python 3.6.5
# consumer, producer model for threads --- main Tkinter thread is the consumer
# ideas came from Programming Python 4th Edition
# gps_sample.csv is a file with the GPS coordinates of
## some sample of airports.
import _thread as thread
import requests
import csv
import time
import queue
from tkinter import *
from tkinter.scrolledtext import ScrolledText

resultQueue = queue.Queue() # infinite size

def TkConsumer(root):
    try:
        data = resultQueue.get(block=False) # should not block!
    except queue.Empty:
        pass
    else:
        root.insert('end', 'consumer pulled from queue => %s\n\n' % data[1]) # two newlines to make things easier to read
        root.see('end')
    root.after(1500, lambda: TkConsumer(root)) # 1.5 seconds

def ReverseGeolocate(latitude, longitude):
    apiKey = 'AIzaSyCwugFdGLz6QUtcYqD1z0PKKsYJhay3vIg'
    apiUrl = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + str(latitude) + ',' + str(longitude) + '&key=' + apiKey
    apiCall = requests.get(apiUrl)
    status = apiCall.json()['status']
    if status == 'OK':
        results = apiCall.json()['results']
        addressComponents = results[0]['address_components']
        return (status, addressComponents)
    else:
        return (status, 'No Data')

def ProcessCoordinates():
    with open('gps_sample_short.csv', newline='') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        for row in csvReader:
            result = ReverseGeolocate(row[0], row[1])
            if (result[0] != 'INVALID_REQUEST'):
                resultQueue.put(result)

def StartAPICalls():
    thread.start_new_thread(ProcessCoordinates, ())

if __name__ == '__main__':
    # main GUI thread, start thread on button click
    root = ScrolledText()
    root.pack()
    root.bind('<Button-1>', lambda event: StartAPICalls())
    TkConsumer(root)
    root.mainloop()
