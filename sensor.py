import time
import atexit
from dfadc import *  # ADC for LM35 and analog sensors
import RPi.GPIO as GPIO
import requests
import smbus2

# ThingSpeak Channel ID and Write API Key
CHANNEL_ID = '2863497'
WRITE_API_KEY = '0SBX58ZYG48RU7AP'


BMP180_ADDR = 0x77
bus = smbus2.SMBus(1)

# Cleanup GPIO on exit
atexit.register(GPIO.cleanup)
GPIO.cleanup()  # Reset GPIO in case it's busy

# Setup ADC Board for Analog Sensors
print("Sensors are now monitoring...")

try:
    # Try to detect and initialize the ADC board
    board_detect()
    if board.begin() != board.STA_OK:
        print("Board initialization failed, please check your hardware connection!")
        exit(1)
    print("Board Setup Successful")
    board.set_adc_enable()  # Enable ADC on the board

except Exception as e:
    print(f"Error during board initialization: {e}")
    exit(1)  # Exit if the board fails to initialize

# Function to Read Temperature from LM35 Sensor
def read_lm35():
    adc_value = board.get_adc_value(board.A3)
    temperature = (adc_value / 4096) * 3300 / 10.24  # Convert ADC value to Celsius
    return round(temperature, 2)

def read_bmp180_pressure():
    bus.write_byte_data(BMP180_ADDR, 0xF4, 0x34)  # Command to read pressure
    time.sleep(0.005)  # Wait for the conversion to complete
    data = bus.read_i2c_block_data(BMP180_ADDR, 0xF6, 2)  # Read pressure data
    pressure_raw = (data[0] << 8) + data[1]  # Combine the two bytes
    return pressure_raw/40  #
# Function to send data to ThingSpeak
def send_data(temperature):
    url = f'https://api.thingspeak.com/update?api_key=0SBX58ZYG48RU7AP&field1={temperature}'
    response = requests.get(url)
    if response.status_code == 200:
        print("Data sent successfully!")
    else:
        print("Failed to send data:", response.status_code)
def send_data(pressure):
    url = f'https://api.thingspeak.com/update?api_key=0SBX58ZYG48RU7AP&field1={pressure}'
    response = requests.get(url)
    if response.status_code == 200:
        print("Data sent successfully!")
    else:
        print("Failed to send data:", response.status_code)

# Main loop to read sensor values and send to ThingSpeak
try:
    print("Starting sensor readings...\n")
    while True:
        # LM35 Temperature Sensor reading
        lm35_temperature = read_lm35()
        print(f"LM35 Temperature: {lm35_temperature:.2f}°C")

        # Send temperature data to ThingSpeak
        send_data(lm35_temperature)

        time.sleep(15)  # Delay between readings (15 seconds to comply with ThingSpeak rate limits)
        
        pressure = read_bmp180_pressure()
        print(f"Pressure: {pressure:.2f} hPa")  # Print the pressure
        send_data(pressure)
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting...")

finally:
    GPIO.cleanup()  # Cleanup GPIO pins before exit
    print("Cleanup completed")
