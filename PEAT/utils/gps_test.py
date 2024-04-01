'''
GPS Interfacing with Raspberry Pi using Pyhton
http://www.electronicwings.com
'''
import serial               #import serial pacakge
from time import sleep
import webbrowser           #import package for opening link in browser
import sys                  #import system package
import math

gpgga_info = "$GPGGA,"
# print("GPGGA")
ser = serial.Serial ("/dev/ttyAMA0")              #Open port with baud rate
# print("Serial")
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0

def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string

    print("NMEA Time: ", nmea_time,'\n')
    print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')

    lat = float(nmea_latitude)                  #convert string into float for calculation
    longi = float(nmea_longitude)               #convertr string into float for calculation

    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format

#convert raw NMEA string into degree decimal format
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position

def convert_to_meters(lat1, lon1, lat2, lon2):
    mLat1 = float(lat1) * 111.32
    mLat2 = float(lat2) * 111.32
    mLong1 = 40075 * math.cos(float(lat1)) / 360
    mLong2 = 40075 * math.cos(float(lat2)) / 360
    a = math.fabs(mLat1 - mLat2)
    b = math.fabs(mLong1 - mLong2)
    c = math.sqrt(math.pow(a,2)+math.pow(b,2))
    return c * 1000

def get_location():
    global GPGGA_buffer
    global ser
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    global gpgga_info
    print("before try")
    try:
        while True:
            print("in loop")
            received_data = (str)(ser.readline())                   #read NMEA string received
            print("data received")
            GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string
            print(f"GPGGA data available {GPGGA_data_available}")
            if (GPGGA_data_available>0):
                GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string
                NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
                GPS_Info()                                          #get time, latitude, longitude

                print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
                map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees    #create link to plot location on Google map
                print("<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n")               #press ctrl+c to plot on map and exit
                print("------------------------------------------------------------\n")
                return lat_in_degrees, long_in_degrees

    except KeyboardInterrupt:
        webbrowser.open(map_link)        #open current position information in google map
        sys.exit(0)
