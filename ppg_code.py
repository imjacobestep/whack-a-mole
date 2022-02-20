#Using heartPy

#imports
import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import heartpy as hp
from scipy.signal import resample
import keyboard

#variables
file_name = 'hr.txt'  #name of output file
record_time = 10  #length of trail in seconds, change to change recording length
ser = serial.Serial('COM3', 57600)  #setting serial input port with comm speed
#qtime.sleep(3)

def start_recording():
    # start_time = time.time()
    recording = True
    time_data = []
    hr_data = []
    while recording:
        b = ser.readline()         # read a byte string
        string_n = b.decode()      # decode byte string into Unicode  
        string = string_n.rstrip() #remove \n and \r
        try:
            ppg = float(string)    # convert string to float
            print(ppg)
            #print(string)
        except:
            continue
        #time_current = time.time() - start_time  #record time elapsed since start
        time_data.append(time.time())
        hr_data.append(ppg)
        if keyboard.is_pressed("q"):
            print("q pressed, ending loop")
            recording = False
    #print("time_data length: " + str(len(time_data)) + ", hr_data length: " + str(len(hr_data)))
    return processing(time_data, hr_data)

def print_results(results):
    print('RESULTS:')
    for a in range(len(results)):
        print("    READING # " + str(a) + " --------------------------------")
        m = results[a]
        for measure in m.keys():
            print('%s: %f' %(measure, m[measure]))


def process(hr_data, time_data):
    #do something
    sample_rate = 50
    data_arr = np.array(hr_data)
    filtered = hp.remove_baseline_wander(data_arr, sample_rate)
    scaled = hp.scale_data(filtered)
    resampled = resample(scaled, len(scaled) * 4)
    enhanced = hp.enhance_ecg_peaks(resampled, sample_rate=50, aggregation='median', iterations=4)
    data, timer = enhanced, time_data
    wd, m = hp.process(data, sample_rate = 50.0)
    print(len(m))
    return m

def processing(time_data, hr_data):
    print('begin processing')
    data = []
    temp_hr = []
    temp_time = []
    
    start = time_data[0]
    
    for i in range(len(time_data)):
        if time_data[i] - start <= 10:
            temp_hr.append(hr_data[i])
            temp_time.append(time_data[i])
        else:
            #print("time_data length: " + str(len(temp_time)) + ", hr_data length: " + str(len(temp_hr)))
            data.append(process(temp_hr, temp_time))
            temp_hr = []
            temp_hr.append(hr_data[i])
            temp_time = []
            temp_time.append(time_data[i])
            start = time_data[i]
    print('finish processing')
    return data

results = start_recording()
print_results(results)
    