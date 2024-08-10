# Frame Rate

import cv2 

def init_FrameRate():
    frameRateCalculation = 1
    frequency = cv2.getTickFrequency()
    
    return frequency

def calculateFrameRate(t_start, t_end, frequency):
    timePeriod = (t_end - t_start)/frequency
    frameRate = 1/timePeriod
    
    return frameRate
    