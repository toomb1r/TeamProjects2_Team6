'''
check last three values. figure out the difference between max and min if less then 6 meters 

GPS Interfacing with Raspberry Pi using Pyhton
http://www.electronicwings.com
'''
import serial               #import serial pacakge
from time import sleep
import webbrowser           #import package for opening link in browser
import sys                  #import system package
import math

def GPS_Info():
    # global NMEA_buff 
    # global lat_in_degrees # wtf change this probs
    # global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
    
    print("NMEA Time: ", nmea_time,'\n')
    print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
    
    lat = float(nmea_latitude)                  #convert string into float for calculation
    longi = float(nmea_longitude)               #convert string into float for calculation
    
    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format
    return lat_in_degrees, long_in_degrees, lat, longi
    
#convert raw NMEA string into degree decimal format   
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position
    




def gps_init():
    """
    """
    gpgga_info = "$GPGGA,"
    ser = serial.Serial ("/dev/ttyS0")   #Open port with baud rate
    GPGGA_buffer = 0
    NMEA_buff = 0
    lat_in_degrees = 0 # delete this one?
    long_in_degrees = 0 # deleter this one?
    try:
        print("Hello")
        while True:
            ping_gps_location(ser, gpgga_info, GPGGA_buffer, NMEA_buff)
            sleep(20)

def ping_gps_location(ser, gpgga_info, GPGGA_buffer, NMEA_buff):
    received_data = (str)(ser.readline())                   #read NMEA string received
    print(received_data)
    GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
    if (GPGGA_data_available>0):
        GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
        NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
        return lat_in_degrees, long_in_degrees, lat, longi = GPS_Info()  

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6378.137  # Radius of earth in KM
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d * 1000  # meters

def save_gps_data():
    """Gets coordinates at the time of function call.

    After error checking it writes at time coordinates to a CSV file.

    Args: 
        none

    Returns: 
        csv_file_path (string) - file path to the csv 
    """
    #connection to the socket
    gpsd_connection = gps3.GPSDSocket()
    #streaming data from socket
    data_stream = gps3.DataStream()

    csv_file_path = 'gps_data.csv'

    try:
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = ['Latitude', 'Longitude']
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            csv_writer.writeheader()

            for new_data in gpsd_connection:
                if new_data:
                    # Parse new GPS data
                    data_stream.unpack(new_data)
                    # Check if GPS data is valid
                    if data_stream.TPV['lat'] and data_stream.TPV['lon']:
                        latitude = data_stream.TPV['lat']
                        longitude = data_stream.TPV['lon']

                        # Write data to CSV file
                        csv_writer.writerow({'Latitude': latitude, 'Longitude': longitude})

                        print(f"Latitude: {latitude}, Longitude: {longitude}")
                # Wait for 1 second
                sleep(1)
    finally:
        return csv_file_path
    
                           #get time, latitude, longitude
 
            # print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
            # map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees    #create link to plot location on Google map
            # print("<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n")               #press ctrl+c to plot on map and exit 
            # print("------------------------------------------------------------\n")
                        
# except KeyboardInterrupt:
#     webbrowser.open(map_link)        #open current position information in google map
#     sys.exit(0)