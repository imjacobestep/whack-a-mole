#imports
import serial
import time
import signal
import keyboard
import csv
import datetime
import numpy as np

#variables
chunk_time = 10  #length of trail in seconds, change to change recording length
ser = serial.Serial('COM3', 57600)  #setting serial input port with comm speed

#filters
def moving_average (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

def get_hr(data):
    peaks = signal.find_peaks(data, distance=100)
    return len(peaks)

def get_br(data):
    peaks = signal.find_peaks(data, distance=5)
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
            ppg = float(string)    # convert string to float
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
    raw_file = "ppg_raw_" + str(datetime.datetime.now()) + '.csv'
    with open('raw_file', 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(['time', 'ppg reading'])
        for i in range(len(hr_data)):
            write.writerow([time_data[i], hr_data[i]])

def processing(time_data, hr_data):
    processed_file = "ppg_reading_" + str(datetime.datetime.now()) + '.csv'
    temp_data = []
    with open(processed_file, 'w', newline='') as f:
        start = time_data[0]
        write = csv.writer(f)
        write.writerow(['reading', 'heart rate', 'breathing rate'])
        for i in range(len(time_data)):
            if time_data[i] - start <= 20:
                temp_data.append(moving_average(hr_data[i]))
            else:
                write.writerow([i + 1, get_hr(temp_data), get_br(temp_data)])

                temp_data = []
                temp_data.append(hr_data[i])
                start = time_data[i]
        print('finish processing')

while True:
    start_recording()
    input('press any key to take another recording')
    