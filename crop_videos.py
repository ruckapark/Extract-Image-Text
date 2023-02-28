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
    
    output_first = r'{}\{}_first.jpg'.format(output_dir,vid.split('\\')[-1].split('.')[0])
    output_last = r'{}\{}_last.jpg'.format(output_dir,vid.split('\\')[-1].split('.')[0])
    
    os.system('{} -y -i {} -vframes 1 {}'.format(ffm_path,vid,output_first))
    #os.system('{} -y -i {} -vf "select=eq(n\,0)" -q:v 2 {}'.format(ffm_path,vid,output_first))
    os.system('{} -y -sseof -3 -i {} -vsync 0 -q:v 2 -update true {}'.format(ffm_path,vid,output_last))
    
    return [output_first,output_last]

def extract_image(vid,output,timestamp = None,ffm_path = 'None',output_dir = 'None'):
    
    if ffm_path == 'None':
        ffm_path = r'{}\ffmpeg.exe'.format(os.getcwd())
    if output_dir == 'None':
        output_dir = os.getcwd()
        
    output = r'{}\{}'.format(output_dir,output.split('\\')[-1])
    
    if timestamp:
        os.system('{} -y -ss {} -i {} -frames:v 1 -q:v 2 {}'.format(ffm_path,timestamp,vid,output))
    else:
        os.system('{} -y -i {} -vframes 1 {}'.format(ffm_path,vid,output))
        
    return output


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
        
    output = r'{}\{}_crop.avi'.format(output_dir,vid.split('\\')[-1].split('.')[0])
    
    crop_time = end - start
    crop_time = strf.strfdelta(crop_time)
    
    os.system('{} -y -i {} -acodec copy -vcodec copy -copyts -ss 00:00:00 -t {} {}'.format(ffm_path,vid,crop_time,output))
    
    return output

def check_samevid(path1,path2,ffm_path = None):
    """ 
    Logic:
    determine smaller file
    find length of smaller file
    extract first and (almost) last image from file
    extract equivalents from larger file
    open with cv and check if there are the same
    """
    size1 = os.path.getsize(path1)
    if os.path.getsize(path2) > size1:
        file = path1
    else:
        file = path2
    
    start,end = extract_endpoints(file)
    start = get_datetime(start)
    end = get_datetime(end)
    delta = end - start - datetime.timedelta(seconds = 2)    #give lag error
    delta = strf.strfdelta(delta)
    
    in1,out1 = extract_image(path1,'in1.jpg'),extract_image(path1,'out1.jpg',timestamp = delta)
    in2,out2 = extract_image(path2,'in2.jpg'),extract_image(path2,'out2.jpg',timestamp = delta)
    start = text.compare_images(in1,in2)
    end = text.compare_images(out1,out2)
    
    for f in [in1,out1,in2,out2]: os.remove(f)
    
    if start and end:
        return True
    else:
        return False
    
def get_datetime(im):
    return text.extract_datetext(im)[-1]

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