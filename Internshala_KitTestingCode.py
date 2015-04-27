import RPi.GPIO as GPIO
import time
import spidev
import os 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.IN)
GPIO.setup(16,GPIO.IN)
GPIO.setup(18,GPIO.IN)
GPIO.setup(22,GPIO.IN)

GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

spi = spidev.SpiDev() # Open SPI bus
spi.open(0,0) 
# Function to read SPI data from MCP3208 chip
def ReadChannel(channel): # Channel must be an integer 0-7
 	adc = spi.xfer2([1,(8+channel)<<4,0]) #send 3 bytes for initialization and channel number 
 	data = ((adc[1]&31) << 8) + adc[2] #adc[1] contains MSB 4 bits adc [2]contains LSB 8 bits
 	return data
 
# Function to convert data to voltage level,
def ConvertVolts(data,places): # rounded to specified number of decimal places
  	volts = (data * 3.3) / float(1024)
	volts = round(volts,places)
 	return volts  
# LDR connected to channel 0
light_channel = 0
# Define delay between readings
delay = 5
  	
while True:
	# Read the light sensor data
  	light_level = ReadChannel(light_channel)
  	light_volts = ConvertVolts(light_level,2)
 	# Print out results
 	print("Light: {} ({}V)".format(light_level,light_volts))
  	# Wait before repeating loop
	 time.sleep(delay)

	#code for motors forward
	GPIO.output(7,True)
	GPIO.output(11,False)
	GPIO.output(13,True)
	GPIO.output(15,False)

 	if GPIO.input(12)==False:
		#code for motors reverse
		GPIO.output(7,False)
		GPIO.output(11,True)
		GPIO.output(13,False)
		GPIO.output(15,True)
		time.sleep(2)


