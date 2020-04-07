# VideoSubFinder_ocr_path

I wanted to rip hardcoded subtitles from movies and turn them into to an SRT file so that I can select the subtitle and look up words I don't know.

I saw there were four parts to this problem.

1. I needed a program that could get me screen grabs of each subtitle as well as the time info for said subtitle.

    I used VideoSubFinder https://sourceforge.net/projects/videosubfinder/

2. I needed a program to clean up the screen grabs.
    
    I wrote one

3. I needed a program to OCR the screen grabs.
    
    I used tesseract https://github.com/tesseract-ocr/tesseract

4. I needed a program to build the SRT from the results of OCR.
    
    I wrote one


What is this even?
This is my solution to this problem.

Video Sub Finder is a program written by Simeon Kosnitsky. It takes screengrabs of subtitles and saves them with a name consisting of the time the subtitle first appears and the time it disappears. This is the solution i used for steps 1 and 2.

Tesseract is an Open Source OCR engine owned by google. This is part of the solution i used for step 3.

resize_images.py was written by me This is the solution I used for step 2.

build_subs.py was written by me. This is the solution I used for steps 3 and 4.


How to use these scripts?

Video Sub Finder will create a folder called TXTimages, put both scripts in this folder.

After you have generated the TXTimages then run resize_images.py, after that's done run build_subs.py
Running them in either idle or CMD is best as you can see their output.

Change the variables at the top of each script to suit your liking, I have left them on the settings i found most useful.
In resize_images.py 

I apologise in advance to the poor soul who tries to read or use this code, I wrote it when I was tired and a little bit drunk.
These scripts have the added feature of turning your computer into a heater for the duration of their use.

Install dependencies

    run pip install numpy PIL opencv-python pytesseract

Dependencies:
* python 3
* opencv
* pytesseract
* PIL
* Numpy
