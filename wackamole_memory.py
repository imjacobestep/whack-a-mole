#Import libraries
import RPi.GPIO as GPIO
import random
from time import sleep
from time import time

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
	# Record start time
	# Reset the score
	score = 0
	# Set the speed to 12 (1.2 seconds)
	speed = 10
	# Set number of goes per game
	runTimes = 5

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
		sleep(0.2)

		# Increase the speed by reducing the number of times the button is checked for a press
		# speed = speed - 1

	print("Game over. You scored ", score, "out of ", runTimes)
	input("Press ENTER to play memory game")

    #Setup first game
	score_1 = 0
	solution_1 = []
	results_1 = []
	randomNumber1_1 = random.randint(0, 4)
	randomNumber1_2 = random.randint(0, 4)
	randomNumber1_3 = random.randint(0, 4)

	solution_1.append(randomNumber1_1)
	solution_1.append(randomNumber1_2)
	solution_1.append(randomNumber1_3)

	#Display first game
	print("Practice Round")
	GPIO.output(pins[randomNumber1_1][0], GPIO.HIGH)
	sleep(1)
	GPIO.output(pins[randomNumber1_1][0], GPIO.LOW)
	sleep(1)
	GPIO.output(pins[randomNumber1_2][0], GPIO.HIGH)
	sleep(1)
	GPIO.output(pins[randomNumber1_2][0], GPIO.LOW)
	sleep(1)
	GPIO.output(pins[randomNumber1_3][0], GPIO.HIGH)
	sleep(1)
	GPIO.output(pins[randomNumber1_3][0], GPIO.LOW)
	sleep(1)

	count = 0
	while count<3:
		if GPIO.input(pins[0][1]) == True:
			results_1.append(0)
			count = count + 1
			print(count)
			sleep(0.45)
		elif GPIO.input(pins[1][1]) == True:
			results_1.append(1)
			count = count + 1
			print(count)
			sleep(0.45)
		elif GPIO.input(pins[2][1]) == True:
			results_1.append(2)
			count = count + 1
			print(count)
			sleep(0.45)
		elif GPIO.input(pins[3][1]) == True:
			results_1.append(3)
			count = count + 1
			print(count)
			sleep(0.45)
		elif GPIO.input(pins[4][1]) == True:
			results_1.append(4)
			count = count + 1
			print(count)
			sleep(0.45)

	print("solution:", solution_1)
	print("results:", results_1)

	#Grading Results to get Score
	if results_1[0] == solution_1 [0]:
		score_1 = score_1 +1

	if results_1[1] == solution_1 [1]:
		score_1 = score_1 +1

	if results_1[2] == solution_1 [2]:
		score_1 = score_1 +1

	print("score:", score_1)

	input("Press ENTER to play round 1")

	# Setup second game
	score_2 = 0
	solution_2 = []
	results_2 = []
	randomNumber2_1 = random.randint(0, 4)
	randomNumber2_2 = random.randint(0, 4)
	randomNumber2_3 = random.randint(0, 4)

	solution_2.append(randomNumber2_1)
	solution_2.append(randomNumber2_2)
	solution_2.append(randomNumber2_3)

	# Display second game
	print("Round 1")
	GPIO.output(pins[randomNumber2_1][0], GPIO.HIGH)
	sleep(1)
	GPIO.output(pins[randomNumber2_1][0], GPIO.LOW)
	sleep(1)
	GPIO.output(pins[randomNumber2_2][0], GPIO.HIGH)
	sleep(1)
	GPIO.output(pins[randomNumber2_2][0], GPIO.LOW)
	sleep(1)
	GPIO.output(pins[randomNumber2_3][0], GPIO.HIGH)
	sleep(1)
	GPIO.output(pins[randomNumber2_3][0], GPIO.LOW)
	sleep(1)

	count = 0
	while count < 3:
		if GPIO.input(pins[0][1]) == True:
			results_2.append(0)
			count = count + 1
			print(count)
			sleep(0.45)
		elif GPIO.input(pins[1][1]) == True:
			results_2.append(1)
			count = count + 1
			print(count)
			sleep(0.45)
		elif GPIO.input(pins[2][1]) == True:
			results_2.append(2)
			count = count + 1
			print(count)
			sleep(0.45)
		elif GPIO.input(pins[3][1]) == True:
			results_2.append(3)
			count = count + 1
			print(count)
			sleep(0.45)
		elif GPIO.input(pins[4][1]) == True:
			results_2.append(4)
			count = count + 1
			print(count)
			sleep(0.45)

	print("solution:", solution_2)
	print("results:", results_2)

	# Grading Results to get Score
	if results_2[0] == solution_2[0]:
		score_2 = score_2 + 1

	if results_2[1] == solution_2[1]:
		score_2 = score_2 + 1

	if results_2[2] == solution_2[2]:
		score_2 = score_2 + 1

	print("score:", score_2)

	input("Press ENTER to play round 2")

	# Setup third game
	score_3 = 0
	solution_3 = []
	results_3 = []
	randomNumber3_1 = random.randint(0, 4)
	randomNumber3_2 = random.randint(0, 4)
	randomNumber3_3 = random.randint(0, 4)
	randomNumber3_4 = random.randint(0, 4)

	solution_3.append(randomNumber3_1)
	solution_3.append(randomNumber3_2)
	solution_3.append(randomNumber3_3)
	solution_3.append(randomNumber3_4)

	# Display third game
	print("Round 2")
	GPIO.output(pins[randomNumber3_1][0], GPIO.HIGH)
	sleep(1)
	GPIO.output(pins[randomNumber3_1][0], GPIO.LOW)
	sleep(1)
	GPIO.output(pins[randomNumber3_2][0], GPIO.HIGH)
	sleep(1)
	GPIO.output(pins[randomNumber3_2][0], GPIO.LOW)
	sleep(1)
	GPIO.output(pins[randomNumber3_3][0], GPIO.HIGH)
	sleep(1)
	GPIO.output(pins[randomNumber3_3][0], GPIO.LOW)
	sleep(1)
	GPIO.output(pins[randomNumber3_4][0], GPIO.HIGH)
	sleep(1)
	GPIO.output(pins[randomNumber3_4][0], GPIO.LOW)
	sleep(1)

	count = 0
	while count < 4:
		if GPIO.input(pins[0][1]) == True:
			results_3.append(0)
			count = count + 1
			print(count)
			sleep(0.45)
		elif GPIO.input(pins[1][1]) == True:
			results_3.append(1)
			count = count + 1
			print(count)
			sleep(0.45)
		elif GPIO.input(pins[2][1]) == True:
			results_3.append(2)
			count = count + 1
			print(count)
			sleep(0.45)
		elif GPIO.input(pins[3][1]) == True:
			results_3.append(3)
			count = count + 1
			print(count)
			sleep(0.45)
		elif GPIO.input(pins[4][1]) == True:
			results_3.append(4)
			count = count + 1
			print(count)
			sleep(0.45)

	print("solution:", solution_3)
	print("results:", results_3)

	# Grading Results to get Score
	if results_3[0] == solution_3[0]:
		score_3 = score_3 + 1

	if results_3[1] == solution_3[1]:
		score_3 = score_3 + 1

	if results_3[2] == solution_3[2]:
		score_3 = score_3 + 1

	if results_3[3] == solution_3[3]:
		score_3 = score_3 + 1

	print("score:", score_3)

	# Setup final game
	score_4 = 0
	solution_4 = []
	results_4 = []
	randomNumber4_1 = random.randint(0, 4)
	randomNumber4_2 = random.randint(0, 4)
	randomNumber4_3 = random.randint(0, 4)
	randomNumber4_4 = random.randint(0, 4)
	randomNumber4_5 = random.randint(0, 4)

	solution_4.append(randomNumber4_1)
	solution_4.append(randomNumber4_2)
	solution_4.append(randomNumber4_3)
	solution_4.append(randomNumber4_4)
	solution_4.append(randomNumber4_5)

	# Display third game
	print("Round 3")
	GPIO.output(pins[randomNumber4_1][0], GPIO.HIGH)
	sleep(1)
	GPIO.output(pins[randomNumber4_1][0], GPIO.LOW)
	sleep(1)
	GPIO.output(pins[randomNumber4_2][0], GPIO.HIGH)
	sleep(1)
	GPIO.output(pins[randomNumber4_2][0], GPIO.LOW)
	sleep(1)
	GPIO.output(pins[randomNumber4_3][0], GPIO.HIGH)
	sleep(1)
	GPIO.output(pins[randomNumber4_3][0], GPIO.LOW)
	sleep(1)
	GPIO.output(pins[randomNumber4_4][0], GPIO.HIGH)
	sleep(1)
	GPIO.output(pins[randomNumber4_4][0], GPIO.LOW)
	sleep(1)
	GPIO.output(pins[randomNumber4_5][0], GPIO.HIGH)
	sleep(1)
	GPIO.output(pins[randomNumber4_5][0], GPIO.LOW)
	sleep(1)

	count = 0
	while count < 5:
		if GPIO.input(pins[0][1]) == True:
			results_4.append(0)
			count = count + 1
			print(count)
			sleep(0.45)
		elif GPIO.input(pins[1][1]) == True:
			results_4.append(1)
			count = count + 1
			print(count)
			sleep(0.45)
		elif GPIO.input(pins[2][1]) == True:
			results_4.append(2)
			count = count + 1
			print(count)
			sleep(0.45)
		elif GPIO.input(pins[3][1]) == True:
			results_4.append(3)
			count = count + 1
			print(count)
			sleep(0.45)
		elif GPIO.input(pins[4][1]) == True:
			results_4.append(4)
			count = count + 1
			print(count)
			sleep(0.45)

	print("solution:", solution_4)
	print("results:", results_4)

	# Grading Results to get Score
	if results_4[0] == solution_4[0]:
		score_4 = score_4 + 1

	if results_4[1] == solution_4[1]:
		score_4 = score_4 + 1

	if results_4[2] == solution_4[2]:
		score_4 = score_4 + 1

	if results_4[3] == solution_4[3]:
		score_4 = score_4 + 1

	if results_4[4] == solution_4[4]:
		score_4 = score_4 + 1

	print("score:", score_4)

	input("Press ENTER to re-start the test")



