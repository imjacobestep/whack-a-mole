#imports
import serial
import time
from scipy import signal
import keyboard
import csv
import datetime
import numpy as np

#variables
chunk_time = 10  #length of trail in seconds, change to change recording length
ser = serial.Serial('COM3', 57600)  #setting serial input port with comm speedqqqq
readingNum = 1
currentTime = 1
#filters
def moving_average (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

def get_hr(data):
    peaks, blank = signal.find_peaks(np.array(data), distance=100)
    #print(peaks.shape())
    return len(peaks)

def get_br(data):
    peaks, blank = signal.find_peaks(np.array(data), distance=5)
    #print(peaks.shape())
    return len(peaks)

#functions
def start_recording():
    print('press Q to stop recording')
    recording = True
    time_data = []
    hr_data = []
    start_time = time.time()
    while recording:
        b = ser.readline()         # read a byte string
        string_n = b.decode()      # decode byte string into Unicode  
        string = string_n.rstrip() #remove \n and \r
        try:
            ppg = float(string)    # convert string to floatq
            print(ppg)
        except:
            continue
        time_data.append(time.time() - start_time)
        hr_data.append(ppg)
        if keyboard.is_pressed("q"):
            print("q pressed, ending loop")
            recording = False
    write_raw(hr_data, time_data)
    processing(time_data, hr_data)

def write_raw(hr_data, time_data):
    raw_file = "raw_" + str(currentTime) + '_reading_' + str(readingNum) + '.csv'
    with open(raw_file, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(['time', 'ppg reading'])
        for i in range(len(hr_data)):
            write.writerow([time_data[i], hr_data[i]])

def processing(time_data, hr_data):
    processed_file = "reading_" + str(currentTime) + '.csv'
    temp_data = []
    with open(processed_file, 'w', newline='') as f:
        start = time_data[0]
        write = csv.writer(f)
        write.writerow(['reading', 'heart rate', 'breathing rate'])
        for i in range(len(time_data)):
            if time_data[i] - start <= chunk_time:
                temp_data.append(hr_data[i])
            else:
                temp2 = moving_average(temp_data, 10)
                write.writerow([i + 1, get_hr(temp2), get_br(temp2)])

                temp_data = []
                temp_data.append(hr_data[i])
                start = time_data[i]
        print('finish processing')
        write.writerow(['end reading 1', '-', '-'])

while True:
    start_recording()
    readingNum = readingNum + 1
    input('press any key to take another recording')
    