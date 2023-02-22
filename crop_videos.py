# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 17:17:17 2023

Crop video automatically using timestamp function

@author: George
"""

#imports
import os
import datetime
import numpy as np
import extract_text as text
import datetime_strf as strf

def extract_endpoints(vid,ffm_path = 'None',output_dir = 'None'):
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
    if ffm_path == 'None':
        ffm_path = r'{}\ffmpeg.exe'.format(os.getcwd())
    if output_dir == 'None':
        output_dir = os.getcwd()
    
    output_first = r'{}\{}_first.jpg'.format(output_dir,vid.split('.')[0])
    output_last = r'{}\{}_last.jpg'.format(output_dir,vid.split('.')[0])
    
    os.system('{} -y -i {} -vf "select=eq(n\,0)" -q:v 2 {}'.format(ffm_path,vid,output_first))
    os.system('{} -y -sseof -3 -i {} -vsync 0 -q:v 2 -update true {}'.format(ffm_path,vid,output_last))
    
    return [output_first,output_last]


def crop_vid(vid,start,end,ffm_path = 'None',output_dir = 'None'):
    """
    end - start must be shorter than the original video!
    if not this will raise ffmpeg error
    
    Parameters
    ----------
    vid : .avi / .mp4
        Video to be cropped.
    start : datetime
        beginning of video timestamp.
    end : datetime
        desired end of video timestamp.

    Returns
    -------
    Name of newly saved file cropped
    """   
    
    if ffm_path == 'None':
        ffm_path = r'{}\ffmpeg.exe'.format(os.getcwd())
    if output_dir == 'None':
        output_dir = os.getcwd()
        
    output = r'{}\{}_crop.avi'.format(output_dir,vid.split('.')[0])
    
    crop_time = end - start
    crop_time = strf.strfdelta(crop_time)
    
    os.system('{} -y -i {} -acodec copy -vcodec copy -copyts -ss 00:00:00 -t {} {}'.format(ffm_path,vid,crop_time,output))
    
    return output

if __name__ == '__main__':
    
    #videopath
    vid = 'originalvid.avi'
    
    #extract first and last frame using ffmpeg
    [start,end] = extract_endpoints(vid)
    
    starttime,endtime = text.extract_datetext(start)[-1],text.extract_datetext(end)[-1]
    
    #define extraction point to be in the middle
    pivot = starttime + datetime.timedelta(minutes=1)
    
    #find timedeltas
    time_start2pivot = pivot - starttime
    time_pivot2end = endtime - pivot
    
    #find desired endpoint after pivot point
    timedelta_mins = 2
    endtime_ = pivot + datetime.timedelta(minutes = timedelta_mins)
    
    #use ffmpeg to crop to new shorter version of video
    if endtime_ < endtime:
        output = crop_vid(vid,starttime,endtime_)
    else:
        print('No need to crop, video short enough!')
        output = None
    
    #delete original video and rename new video (lol)