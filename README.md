# Read numbers from image

Quick example of reading simple text from image with timestamp with **tesseract**

## Use

- OpenCV used in example rather than pillow
- Pytesseract pip install with --user option for administrator
- Seperate install of tesseract used when pointing to exe (unecessary to add to PATH)
- tesseract install : https://github.com/UB-Mannheim/tesseract/wiki

## FFMPEG commands

Extract 5 minute video from original video (from other drive)
- I:\ffmpeg\ffmpeg.exe -i 20210430-174053_Gammarus_0001.avi -acodec copy -vcodec copy -copyts -ss 00:00:00 -t 00:05:00 originalvid.avi

The first frame may not be necessary, as it should be possible to crop from the end of the video backwards.
For a complete use of ffmpeg, I will extract the first and last frame, and crop relative to the beginning point.

Extract first frame from video
- ffmpeg -i input -vf "select=eq(n\,0)" -q:v 2 output_start.jpg

Extract Last frame from video
- ffmpeg -sseof -3 -i file -vsync 0 -q:v 31 -update true out.jpg