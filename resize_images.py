import cv2 as cv
import numpy as np
from PIL import Image
import os
import time
import os
import concurrent.futures

#used for resizing, it will resize the image maintaining aspect ratio
# to the smallest dimension, my images were 5000 by 1000, so it gets shrunk to
# 40 px tall and an unknown width.
size = (1920, 40)

# only run on files with this file extension.
ext = '.jpeg'

# folder to run on.
path = os.getcwd()

startTime = 0

def get_boundaries(name, debug=False):
    # crop out unecessary whitespace
    src = cv.imread(cv.samples.findFile(name),1)
    src_gray = cv.blur(src, (3,3))
    threshold = 100
    leftmost = src.shape[1]
    rightmost = 0
    canny_output = cv.Canny(src_gray, threshold, threshold * 2)
    contours, _ = cv.findContours(canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    offset = int(src.shape[1]*0.03)
    # Get the mass centers
    mc = [None]*len(contours)
    for i in range(len(contours)):
        # Get the moment
        moment = cv.moments(contours[i])
        # add 1e-5 to avoid division by zero
        mc[i] = (moment['m10'] / (moment['m00'] + 1e-5), moment['m01'] / (moment['m00'] + 1e-5))
    # Draw contours
    #minarea = 1000
    for i, j in enumerate(contours):
        val = int(mc[i][0])
        area = cv.contourArea(contours[i])
        #val = int(i[0][0][0])
        if leftmost > val and val > offset:# and area > minarea:
           leftmost = val
        if rightmost < val and val < src.shape[1]-offset:# and area > minarea:
            rightmost = val
        if debug >= 2:
            print('val: ',end='')
            print(val, end = '')
            print(' '.join(['Number', str(i), 'lm', str(leftmost),
                            'rm', str(rightmost)]))
    leftmost -= offset
    rightmost += offset
    # Calculate the area with the moments 00 and compare with the result of the OpenCV function
    if debug >= 3:
        for i in range(len(contours)):
            print(' * Contour[{0}]. Area: {1}. Length: {2}.'.format(i, cv.contourArea(contours[i]), cv.arcLength(contours[i], True), contours[i]))
        
    return leftmost, 0, rightmost, src.shape[0]

def run_on(path, debug=False):
    global startTime
    startTime = int(time.time())
    op = []
    count = 0
    namelist = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if ext in name:
                namelist.append(name)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for name, result in zip(namelist, executor.map(get_boundaries, namelist)):
            if debug >= 1: print('Time Elapsed:',
                                  str(int(time.time())-startTime),
                                 'secs. Image:', count, 'Name:', name)
            shrink_and_crop(name, result, size, debug)
            count+=1
    print('Done in {} seconds!'.format(str(int(time.time())-startTime)))

def shrink_and_crop(name, cropbox, maxsize, debug=False):
    im = Image.open(name)
    if debug >= 2: print(im, cropbox)
    try:
        im = im.crop(cropbox)
        if im.size[1] > maxsize[1]:
            im.thumbnail(maxsize)
        if debug >= 2: print(im)
        im.save(name)
        #im.save('did it work1.jpg')
    except ValueError:
        print('Did not run on:',name)

run_on(path, debug=1)
