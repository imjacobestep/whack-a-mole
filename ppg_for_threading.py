## IMPORTS ##
import serial
import time
from scipy import signal
import keyboard
import csv
import datetime
import numpy as np
import threading

## GLOBAL VARS ##
global_time_data = []
global_hr_data = []
avg_reaction_time = 0
mole_score = 0
mem_score1 = 0
mem_score2 = 0
mem_score3 = 0
ppg_feature = 0

## MAIN FUNCTION ##
def main_task():
    lock = threading.Lock()

    ppg = threading.Thread(target=ppg_reading, args=lock)
    game = threading.Thread(target=play_game, args=lock)
    processing = threading.Thread(target=ppg_processing, args=lock)

    ppg.start()
    game.start()
    game.join()
    processing.start()
    processing.join()

    send_to_cloud(react= avg_reaction_time, mole1=mole_score, mem1=mem_score1, mem2=mem_score2, mem3=mem_score3, ppgF=ppg_feature)

## SEND TO CLOUD ## TODO
def send_to_cloud(react, mole1, mem1, mem2, mem3, ppgF):
    #do stuff
    pass

## GAME ## TODO
def play_game(lock):
    #do stuff
    pass

## SENSOR READING ##
def ppg_reading(lock):
    global global_time_data
    global global_hr_data
    ser = serial.Serial('COM3', 57600)  #setting serial input port with comm speed
    start_time = time.time()

    while True:
        b = ser.readline()         # read a byte string
        string_n = b.decode()      # decode byte string into Unicode  
        string = string_n.rstrip() #remove \n and \r
        try:
            ppg = float(string)    # convert string to floatq
            print(ppg)
        except:
            continue
        global_time_data.append(time.time() - start_time)
        global_hr_data.append(ppg)

## DATA PROCESSING ##
def ppg_processing(lock):
    global global_time_data
    global global_hr_data

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
    for i in range(len(time_data)):
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
