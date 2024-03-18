import serial
import pynmea2  # You may need to install this library using: pip install pynmea2

# Define the serial port and baud rate
serial_port = '/dev/ttyS0'  # Replace with the correct serial port (e.g., '/dev/ttyAMA0' for older Raspberry Pi models)
baud_rate = 9600  # Match the baud rate with the configuration of your GPS module

# Create a serial object
ser = serial.Serial(serial_port, baud_rate, timeout=1)

try:
    while True:
        # Read a line from the serial port
        sentence = ser.readline().decode('utf-8')
        
        # Check if the sentence is a valid NMEA sentence
        if sentence.startswith('$'):
            try:
                # Parse the NMEA sentence
                data = pynmea2.parse(sentence)
                
                # Print the parsed data
                print(data)
                
                # Example: Print the latitude and longitude
                if isinstance(data, pynmea2.RMC):
                    print(f"Latitude: {data.latitude}, Longitude: {data.longitude}")
                    
            except pynmea2.ParseError as e:
                print(f"Parse error: {e}")
                
except KeyboardInterrupt:
    # Close the serial port when Ctrl+C is pressed
    ser.close()
