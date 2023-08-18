# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 18:16:03 2023

Write as text file, the start time of each video using extract text
For failed videos it will be performed manually

@author: George
"""

import os
import datetime
import numpy as np
import extract_text as text
import datetime_strf as strf

def extract_endpoints(vid,ffm_path = None,output_dir = None):
    """
    Parameters
    ----------
    vid : avi file type ToxMate (path)
    requirements : ffmpeg recent version > 2020 (assumed in current directory)
    
    Returns
    -------
    outputnames, saves two images format:
        '{}_first.jpg'.formate(vid)
        '{}_last.jpg'.formate(vid)
    """
    if not ffm_path:
        ffm_path = r'{}\ffmpeg.exe'.format(os.getcwd())
    if not output_dir:
        output_dir = os.getcwd()
    
    output_first = r'{}\{}_first.jpg'.format(output_dir,vid.split('\\')[-1].split('.')[0])
    output_last = r'{}\{}_last.jpg'.format(output_dir,vid.split('\\')[-1].split('.')[0])
    
    os.system('{} -y -i {} -vframes 1 {}'.format(ffm_path,vid,output_first))
    #os.system('{} -y -i {} -vf "select=eq(n\,0)" -q:v 2 {}'.format(ffm_path,vid,output_first))
    os.system('{} -y -sseof -3 -i {} -vsync 0 -q:v 2 -update true {}'.format(ffm_path,vid,output_last))
    
    return [output_first,output_last]

def write_starttime(start,output_dir = None):
    if not output_dir:
        output_dir = os.getcwd()
    output = r'{}\start.txt'.format(output_dir)
    textfile = open(output,"w")
    textfile.write(start)
    textfile.close()
    

if __name__ == '__main__':
    
    #go throuhg all txm files to attempt to generate start time
    for i in range(10):
        
        Tox = 760 + i
        root = r'I:\TXM{}-PC'.format(Tox)
        dirs = [d for d in os.listdir(root) if os.path.isdir(r'{}\{}'.format(root,d))]
        
        for d in dirs:
            
            #get first avi file and find start if necessary
            output_dir = r'{}\{}'.format(root,d)
            if os.path.isfile(r'{}\start.txt'.format(output_dir)): continue
            
            #extract start datetime to text file
            try: 
                files = [f for f in os.listdir(r'{}\{}'.format(root,d))]
                avifile = [f for f in files if 'Gammarus_0001.avi' in f][0]
                avifile = r'{}\{}\{}'.format(root,d,avifile)
            except:
                continue
            
            #extract first image from video - run from ImageText dir for ffmpeg path
            [start,end] = extract_endpoints(avifile)
            starttime = text.extract_datetext(start)[-1]
            write_starttime(starttime.strftime('%d/%m/%Y %H:%M:%S'),output_dir)
            
            #remove unecessary images
            os.remove(start)
            os.remove(end)