## IMPORTS ##
import serial
import time
from scipy import signal
import numpy as np
import threading
from rpi_lcd import LCD
import random
import RPi.GPIO as GPIO
import pyodbc
import sys

## SETUP ##
GPIO.setwarnings(False) #hide warnings
GPIO.setmode(GPIO.BCM) #use BCM pin numbering

## GLOBAL VARS ##
global_time_data = []
global_hr_data = []
avg_reaction_time = 0
mole_score = 0
mem_score1 = 0
mem_score2 = 0
mem_score3 = 0
ppg_feature = 0
lcd = LCD()

## REPLAY ##
def replay():
    global global_time_data
    global global_hr_data
    global avg_reaction_time
    global mole_score
    global mem_score1
    global mem_score2
    global mem_score3
    global ppg_feature

    global_time_data = []
    global_hr_data = []
    avg_reaction_time = 0
    mole_score = 0
    mem_score1 = 0
    mem_score2 = 0
    mem_score3 = 0
    ppg_feature = 0

    main_task()

## WAIT FUNCTION ##
def wait(s):
    start = time.time()
    while time.time()-start < s:
        pass

## MAIN FUNCTION ##
def main_task():
    user_id = input("input userID: ")
    lock = threading.Lock()

    ppg = threading.Thread(target=ppg_reading, args=(lock,))
    game = threading.Thread(target=play_game, args=(lock,))
    processing = threading.Thread(target=ppg_processing, args=(lock,))

    ppg.start()
    game.start()
    game.join()
    processing.start()
    processing.join()

    send_to_cloud(userID= user_id, react= avg_reaction_time, mole1=mole_score, mem1=mem_score1, mem2=mem_score2, mem3=mem_score3, ppgF=ppg_feature)

## SEND TO CLOUD ## TODO
def send_to_cloud(userID, react, mole1, mem1, mem2, mem3, ppgF):
    print("uploading...")
    server = 'whack-a-mole.database.windows.net'
    database = 'sessions_db'
    username = 'whackamole'
    password = 'password123!'
    driver = '/usr/lib/arm-linux-gnueabihf/odbc/libtdsodbc.so'
    connection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password + ';TDS_Version=8.0')

    cursor = connection.cursor()

    query = (
        "INSERT INTO sessions(user_id, avg_reaction, mole_score, mem_1_score, mem_2_score, mem_3_score, hr_data)"
        "VALUES(?,?,?,?,?,?,?)"
    )

    queryVals = (userID, react, mole1, mem1, mem2, mem3, ppgF)
    cursor.execute(query, queryVals)
    connection.commit()
    print("upload finished")

## GAME ## TODO
def play_game(lock):
    global avg_reaction_time
    global mole_score
    global mem_score1
    global mem_score2
    global mem_score3
    global lcd

    pins = [[11, 18],[9, 15],[7, 14],[8, 4],[22,27]] #LED, Button format; Green, Yellow, Blue, White order

    for i in range(5): #setup LED pins
        GPIO.setup(pins[i][0], GPIO.OUT)
        GPIO.output(pins[i][0],GPIO.LOW)
    for i in range(5): #setup button pins
        GPIO.setup(pins[i][1], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    input("Press ENTER to play")

    ######################
    ## Wack-a-mole Game ##
    ######################

    reaction_times = []
    runTimes = 50
    score = 0
    score_1 = 0
    score_2 = 0
    score_3 = 0
    score_4 = 0
    for molePopup in range(runTimes):
        speed = random.randint(4, 12) # randomise speed
        randomNumber = random.randint(0, 4) # choose random LED
        GPIO.output(pins[randomNumber][0],GPIO.HIGH) # light LED
        light_time = time.time()
        for i in range(speed):
			# Check if the correct button is pressed
            if GPIO.input(pins[randomNumber][1]) == True:
                reaction_time = time.time() - light_time
                reaction_times.append(reaction_time)
                score = score + 1
				# lcd.text(str(score), 2)
                GPIO.output(pins[randomNumber][0],GPIO.LOW)
                break
            wait(0.1)
        GPIO.output(pins[randomNumber][0],GPIO.LOW) # turn off LED
        wait(0.2) # + speed by - num of times button is checked for press, speed=speed-1
    lock.acquire()
    avg_reaction_time = np.mean(reaction_times)
    mole_score = score
    lock.release()
    print("Average Reaction Time:", avg_reaction_time)
    print("Game over. You scored ", score, "out of ", runTimes)
    wait(2)
    input("Press ENTER to play memory game")

    #################
    ## Memory Game ##
    #################

    # practice round
    results_1 = []
    randomNumber1_1 = random.randint(0, 4)
    randomNumber1_2 = random.randint(0, 4)
    randomNumber1_3 = random.randint(0, 4)
    solution_1 = [randomNumber1_1, randomNumber1_2, randomNumber1_3]
    print("Practice Round")
    GPIO.output(pins[randomNumber1_1][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber1_1][0], GPIO.LOW)
    wait(1)
    GPIO.output(pins[randomNumber1_2][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber1_2][0], GPIO.LOW)
    wait(1)
    GPIO.output(pins[randomNumber1_3][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber1_3][0], GPIO.LOW)
    wait(1)

    count = 0
    while count<3:
        if GPIO.input(pins[0][1]) == True:
            results_1.append(0)
            count = count + 1
            print(count)
            wait(0.45)
        elif GPIO.input(pins[1][1]) == True:
            results_1.append(1)
            count = count + 1
            print(count)
            wait(0.45)
        elif GPIO.input(pins[2][1]) == True:
            results_1.append(2)
            count = count + 1
            print(count)
            wait(0.45)
        elif GPIO.input(pins[3][1]) == True:
            results_1.append(3)
            count = count + 1
            print(count)
            wait(0.45)
        elif GPIO.input(pins[4][1]) == True:
            results_1.append(4)
            count = count + 1
            print(count)
            wait(0.45)
    print("solution:", solution_1)
    print("results:", results_1)
    if results_1[0] == solution_1 [0]:
        score_1 = score_1 +1
    if results_1[1] == solution_1 [1]:
        score_1 = score_1 +1
    if results_1[2] == solution_1 [2]:
        score_1 = score_1 +1
    print("score:", score_1)
	# lcd.text("Score:",1)
	# lcd.text(str(score_1),2)
    wait(2)
	# lcd.text("Press ENTER to", 1)
	# lcd.text("play round 1", 2)
    input("Press ENTER to play round 1")

    # round 1
    score_2 = 0
    results_2 = []
    randomNumber2_1 = random.randint(0, 4)
    randomNumber2_2 = random.randint(0, 4)
    randomNumber2_3 = random.randint(0, 4)
    solution_2 = [randomNumber2_1, randomNumber2_2, randomNumber2_3]
    print("Round 1") #display round 1
    # lcd.clear()
    # lcd.text("Round 1", 1)
    GPIO.output(pins[randomNumber2_1][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber2_1][0], GPIO.LOW)
    wait(1)
    GPIO.output(pins[randomNumber2_2][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber2_2][0], GPIO.LOW)
    wait(1)
    GPIO.output(pins[randomNumber2_3][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber2_3][0], GPIO.LOW)

    count = 0
    while count < 3:
        if GPIO.input(pins[0][1]) == True:
            results_2.append(0)
            count = count + 1
            print(count)
            wait(0.45)
        elif GPIO.input(pins[1][1]) == True:
            results_2.append(1)
            count = count + 1
            print(count)
            wait(0.45)
        elif GPIO.input(pins[2][1]) == True:
            results_2.append(2)
            count = count + 1
            print(count)
            wait(0.45)
        elif GPIO.input(pins[3][1]) == True:
            results_2.append(3)
            count = count + 1
            print(count)
            wait(0.45)
        elif GPIO.input(pins[4][1]) == True:
            results_2.append(4)
            count = count + 1
            print(count)
            wait(0.45)

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
    # lcd.text("Score:", 1)
    # lcd.text(str(score_2), 2)
    wait(2)
    # lcd.text("Press ENTER to", 1)
    # lcd.text("play round 2", 2)
    input("Press ENTER to play round 2")

    # round 2
    score_3 = 0
    results_3 = []
    randomNumber3_1 = random.randint(0, 4)
    randomNumber3_2 = random.randint(0, 4)
    randomNumber3_3 = random.randint(0, 4)
    randomNumber3_4 = random.randint(0, 4)
    randomNumber3_5 = random.randint(0, 4)
    
    solution_3 = [randomNumber3_1, randomNumber3_2, randomNumber3_3, randomNumber3_4, randomNumber3_5]
    # lcd.clear()
    # lcd.text("Round 2", 1)
    print("Round 2")
    GPIO.output(pins[randomNumber3_1][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber3_1][0], GPIO.LOW)
    wait(1)
    GPIO.output(pins[randomNumber3_2][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber3_2][0], GPIO.LOW)
    wait(1)
    GPIO.output(pins[randomNumber3_3][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber3_3][0], GPIO.LOW)
    wait(1)
    GPIO.output(pins[randomNumber3_4][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber3_4][0], GPIO.LOW)
    wait(1)
    GPIO.output(pins[randomNumber3_5][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber3_5][0], GPIO.LOW)

    count = 0
    while count < 5:
        if GPIO.input(pins[0][1]) == True:
            results_3.append(0)
            count = count + 1
            print(count)
            wait(0.45)
        elif GPIO.input(pins[1][1]) == True:
            results_3.append(1)
            count = count + 1
            print(count)
            wait(0.45)
        elif GPIO.input(pins[2][1]) == True:
            results_3.append(2)
            count = count + 1
            print(count)
            wait(0.45)
        elif GPIO.input(pins[3][1]) == True:
            results_3.append(3)
            count = count + 1
            print(count)
            wait(0.45)
        elif GPIO.input(pins[4][1]) == True:
            results_3.append(4)
            count = count + 1
            print(count)
            wait(0.45)

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

    if results_3[4] == solution_3[4]:
        score_3 = score_3 + 1
    #
    # lcd.text("Score:", 1)
    # lcd.text(str(score_3), 2)
    wait(2)

    # lcd.text("Press ENTER to", 1)
    # lcd.text("play round 3", 2)

    input("Press ENTER to play round 3")

    print("score:", score_3)

    # Setup final game
    score_4 = 0
    results_4 = []
    randomNumber4_1 = random.randint(0, 4)
    randomNumber4_2 = random.randint(0, 4)
    randomNumber4_3 = random.randint(0, 4)
    randomNumber4_4 = random.randint(0, 4)
    randomNumber4_5 = random.randint(0, 4)
    randomNumber4_6 = random.randint(0, 4)
    randomNumber4_7 = random.randint(0, 4)
    randomNumber4_8 = random.randint(0, 4)
    
    solution_4 = [randomNumber4_1, randomNumber4_2, randomNumber4_3, randomNumber4_4, randomNumber4_5, randomNumber4_6, randomNumber4_7, randomNumber4_8]

    # Display third game
    # lcd.clear()
    # lcd.text("Round 3", 1)
    print("Round 3")
    GPIO.output(pins[randomNumber4_1][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber4_1][0], GPIO.LOW)
    wait(1)
    GPIO.output(pins[randomNumber4_2][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber4_2][0], GPIO.LOW)
    wait(1)
    GPIO.output(pins[randomNumber4_3][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber4_3][0], GPIO.LOW)
    wait(1)
    GPIO.output(pins[randomNumber4_4][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber4_4][0], GPIO.LOW)
    wait(1)
    GPIO.output(pins[randomNumber4_5][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber4_5][0], GPIO.LOW)
    wait(1)
    GPIO.output(pins[randomNumber4_6][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber4_6][0], GPIO.LOW)
    wait(1)
    GPIO.output(pins[randomNumber4_7][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber4_7][0], GPIO.LOW)
    wait(1)
    GPIO.output(pins[randomNumber4_8][0], GPIO.HIGH)
    wait(1)
    GPIO.output(pins[randomNumber4_8][0], GPIO.LOW)
    wait(1)

    count = 0
    while count < 8:
        if GPIO.input(pins[0][1]) == True:
            results_4.append(0)
            count = count + 1
            print(count)
            wait(0.45)
        elif GPIO.input(pins[1][1]) == True:
            results_4.append(1)
            count = count + 1
            print(count)
            wait(0.45)
        elif GPIO.input(pins[2][1]) == True:
            results_4.append(2)
            count = count + 1
            print(count)
            wait(0.45)
        elif GPIO.input(pins[3][1]) == True:
            results_4.append(3)
            count = count + 1
            print(count)
            wait(0.45)
        elif GPIO.input(pins[4][1]) == True:
            results_4.append(4)
            count = count + 1
            print(count)
            wait(0.45)

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
    if results_4[5] == solution_4[5]:
        score_4 = score_4 + 1
    if results_4[6] == solution_4[6]:
        score_4 = score_4 + 1
    if results_4[7] == solution_4[7]:
        score_4 = score_4 + 1
    print("score:", score_4)

    # lcd.text("Score:", 1)
    # lcd.text(str(score_4), 2)

    lock.acquire()
    mem_score1 = score_2
    mem_score2 = score_3
    mem_score3 = score_4
    lock.release()    

## SENSOR READING ##
def ppg_reading(lock):
    global global_time_data
    global global_hr_data
    ser = serial.Serial('/dev/ttyACM0', 57600)  #setting serial input port with comm speed
    start_time = time.time()

    while True:
        b = ser.readline()         # read a byte string
        string_n = b.decode()      # decode byte string into Unicode  
        string = string_n.rstrip() #remove \n and \r
        try:
            ppg = float(string)    # convert string to floatq
            #print(ppg)
        except:
            continue
        global_time_data.append(time.time() - start_time)
        global_hr_data.append(ppg)

## DATA PROCESSING ##
def ppg_processing(lock):
    global global_time_data
    global global_hr_data
    global ppg_feature

    heart_rates = []

    lock.acquire()
    time_data = global_time_data
    hr_data = global_hr_data
    lock.release()

    #do filter
    weights = np.repeat(1.0, 10)/10
    filtered_hr = np.convolve(hr_data, weights, 'valid')

    #cut into chunks
    temp_data = []
    start = time_data[0]
    for i in range(len(filtered_hr)-1):
        if time_data[i] - start <= 20:
            temp_data.append(filtered_hr[i])
        else:
            #get peaks, add to hr_peaks
            peaks, _ = signal.find_peaks(np.array(temp_data), distance=5)
            heart_rates.append(len(peaks)*3)

            #new temp
            temp_data = []
            temp_data.append(filtered_hr[i])
            start = time_data[i]

    #feature extraction on new list of BPMs
    hr_array = np.array(heart_rates)
    ppg_feature = np.std(a=hr_array)

if __name__ == "__main__":
    main_task()
    while input("Press ENTER to play again: "):
        replay()