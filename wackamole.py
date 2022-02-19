## Dependencies
# pip3 install adafruit-circuitpython-busdevice
# pip3 install adafruit-circuitpython-mcp3xxx

#Import libraries
import RPi.GPIO as GPIO
import adafruit_mcp3xxx.mcp3008 as MCP
# import Adafruit_MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn
import numpy as np
import heartpy as hp
from scipy.signal import resample
import matplotlib.pyplot as plt

# Hide warnings.
GPIO.setwarnings(False)

# Use BCM pin numbering
GPIO.setmode(GPIO.BCM)

## Set up variables ##

# spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI) # create the spi bus
# cs = digitalio.DigitalInOut(board.D5) # create the cs (chip select)
# mcp = MCP.MCP3008(spi, cs) # create the mcp object
# mcp = Adafruit_MCP3008.MCP3008(clk=13, cs=12, miso=6, mosi=5) #using specific import
mcp = MCP(clk=13, cs=12, miso=6, mosi=5) #using generic import
chan = AnalogIn(mcp, MCP.P0) # create an analog input channel on pin 0

# Use a list to store the pins used by the buttons
# Because we need to compare the button pressed to
#the LED number, we are going to store everything
#in a 2D list. The first value will be the LED pin.
#The second will be the BUTTON pin.
pins = [
[11, 18], # Green LED, Green button
[9, 15], # Yellow LED, Yellow button
[7, 14], # Blue LED, Blue button
[8, 4], # White LED, White button
[22,27]
]

## Functions ##

def get_ppg(record_time):
  start_time = time.time()
  time_data = []
  hr_data = []
# record data
  while time.time() - start_time < record_time:
    try:
      # hr_data.append( float( ser.readline().decode.rstrip() ) )
      hr_data.append(chan.value)
    except:
      hr_data.append(0)
    time_data.append(time.time())
# process data
  data_arr = np.array(hr_data)
  filtered = hp.remove_baseline_wander(data_arr, sample_rate=50)
  scaled = hp.scale_data(filtered)
  resampled = resample(scaled, len(scaled) * 4)
  enhanced = hp.enhance_ecg_peaks(resampled, sample_rate=50, aggregation='median', iterations=4)
  data, timer = enhanced, time_data
  wd, m = hp.process(data, sample_rate = 50.0)
  return m

## Initialise LED and button pins ##

# Iterate through the list of LED pins and set up
#each one
for i in range(5):
	GPIO.setup(pins[i][0], GPIO.OUT)

# Iterate through the list of button pins and setup each one
for i in range(5):
	GPIO.setup(pins[i][1], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# Run forever
while True:
	# Reset the score
	score = 0
	# Set the speed to 12 (1.2 seconds)
	speed = 12
	# Set number of goes per game
	runTimes = 50

	# Play the game
	for molePopup in range(runTimes):
		# Choose a random LED
		randomNumber = random.randint(0, 4) #maybe
		# Light the LED
		GPIO.output(pins[randomNumber][0],GPIO.HIGH)
		# Light the LED for (0.1 * speed) seconds, since i loops of speed running sleep(0.1)
		for i in range(speed):
			# Check if the correct button is pressed
			if GPIO.input(pins[randomNumber][1]) == True:
				# Increase score and turn off LED
				score = score + 1
				GPIO.output(pins[randomNumber][0],GPIO.LOW)
				break
			sleep(0.1)

		# Turn off the LED
		GPIO.output(pins[randomNumber][0],GPIO.LOW)

		# Increase the speed by reducing the number of times the button is checked for a press
		# speed = speed - 1

	print("Game over. You scored ", score, "out of ", runTimes)
	input("Press ENTER to replay")

