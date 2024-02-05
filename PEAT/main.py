from gps3 import gps3
import RPi.GPIO
import random
import digitalio
import board
import busio
import adafruit_rfm9x
import time

print("hello world")

import time
import csv


def get_gps_data():
    """Get GPS data and write to CSV file."""
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
                time.sleep(1)
    finally:
        return csv_file_path
        
# def send_gps_data():
if __name__ == "__main__":
    get_gps_data()
