#Import libraries
import RPi.GPIO as GPIO
import random
from time import sleep

# Hide warnings.
GPIO.setwarnings(False)

# Use BCM pin numbering
GPIO.setmode(GPIO.BCM)

## Set up variables ##

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

