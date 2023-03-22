# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 17:40:25 2023

@author: George
"""

import cv2
import pytesseract
import numpy as np
from datetime import datetime

def strptime_(string):
    return datetime.strptime(string, "%d/%m/%Y %H:%M:%S")
    
def strptime_backup1(string):
    return datetime.strptime(string, "%d/%m%Y %H:%M:%S")
    
def strptime_backup2(string):
    return datetime.strptime(string, "%d%m/%Y %H:%M:%S")
    
def strptime_backup3(string):
    return datetime.strptime(string, "%d%m%Y %H:%M:%S")

def strptime(string):
    
    strps = [
        strptime_,
        strptime_backup1,
        strptime_backup2,
        strptime_backup3]
    
    for strp in strps:
        try:
            string = strp(string)
            return string
            break
        except:
            continue

def compare_images(img1,img2):
    
    im1,im2 = cv2.imread(img1,0),cv2.imread(img2,0)
    return np.array_equal(im1,im2)

def extract_datetext(img,cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'):
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    im = cv2.imread(img,0)
    
    #portion of interest
    crop = np.flip(np.transpose(im[0:140,944:964]),0)
    text_im = 255 - crop
    
    custom = r'-l eng --oem 3 --psm 6'
    
    date = pytesseract.image_to_string(text_im, lang='eng', config=custom)
    date = date.strip()
    
    return [date,strptime(date)]
    

if __name__ == '__main__':
    
    
    class Image:
        
        def __init__(self,img,bbox = ()):
            self.im = Image(img)
            self.species = 'Erpo' #could use simple NN
            self.time = self.get_time(bbox)
        
        def get_time(self,bbox):
            #assumes timestamp in top right
            return None
        
    #pytesseract location (not in path)
    #here you should download the tesseract binaries, do not use the pytesseract.exe wrapper
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'    
    
    img = cv2.imread('20201120-093425_Erpo_0001_crop_last.jpg',0)
    
    #portion of interest
    cropped_img = np.flip(np.transpose(img[0:140,944:964]),0)
    text_img = 255 - cropped_img
    cv2.imshow('img',text_img)
    
    custom_conf = r'-l eng --oem 3 --psm 6'
    
    date_str = pytesseract.image_to_string(text_img, lang='eng', config=custom_conf)
    date_str = date_str.strip()
    
    #date = strptime_backup2(date_str)
    date = strptime(date_str)