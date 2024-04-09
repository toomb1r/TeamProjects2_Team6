'''
GPS Interfacing with Raspberry Pi using Pyhton
http://www.electronicwings.com
'''
import serial               #import serial pacakge
import math

gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/ttyAMA0")              #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0
home = []

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

    if nmea_latitude == "" or nmea_longitude == "":
        long_in_degrees = 0
        lat_in_degrees = 0
        return

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
    position = "%.8f" %(position)
    return position

def convert_to_meters(lat1, lon1, lat2, lon2):
    midLat = float(lat1) + float(lat2) / 2
    mLat = 111132.954 - 559.822 * math.cos( 2.0 * midLat ) + 1.175 * math.cos( 4.0 * midLat)
    mLon = (math.pi/180 ) * 6367449 * math.cos( midLat )
    dLat = math.fabs(float(lat1) - float(lat2))
    dLon = math.fabs(float(lon1) - float(lon2))
    c = math.sqrt(math.pow(dLat * mLat,2) + math.pow(dLon * mLon,2))
    return c

def get_location():
    global GPGGA_buffer
    global ser
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    global gpgga_info
    ser.reset_input_buffer()

    while True:
        received_data = (str)(ser.readline())                   #read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string
        if (GPGGA_data_available>0):
            GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string
            NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
            GPS_Info()                                          #get time, latitude, longitude
            return lat_in_degrees, long_in_degrees

def readHome():
    """Sets the bot's home coordinates from a read in string.
    Uses a file to get the latitude and longitude data for the Home.
    Sets the latitude and longitude data to the global home variable.

    Args:
        None

    Returns:
        None
    """

    global home
    with open("home.txt","r") as file:
        home = file.readlines()
    print(f"Home: {home}")

def setHome():
    """Sets the bot's home coordinates.
    Gathers GPS coordinates from the current location.
    Saves the GPS coordinates to the global home variable.

    Args:
        None

    Returns:
        None
    """

    global home
    with open("home.txt","w") as file:
        file.write("")
        file.close()

    if len(home) > 0:
        home.pop()

    lat, lon = get_location()
    if lat == 0 and lon == 0:
        print("Error: Couldnt gather GPS data")
        return

    home = [lat.strip(), lon.strip()]
    print(f"Home: {home}\n")
    with open("home.txt","a") as file:
        file.write(f"{lat}\n")
        file.write(lon)
        file.close()

def check_distances(distances):
    distance = 0
    for i in range(0, len(distances)-1):
        distance = distance + convert_to_meters(distances[i][0], distances[i][1], distances[i+1][0], distances[i+1][1])
    return distance
