import csv
import numpy as np
import cv2
import sys
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
%matplotlib inline


images_names_list = glob.glob("/Users/hemanth/Udacity/CarND-Advanced-Lane-Lines-master/camera_cal/*.jpg")

# read images

for image_path in images_names_list:
    image = cv2.imread(image_path)
    cv2.imshow('image',image)
    cv2.waitKey(1)




# Image Distortion


# image calibration



# Find curvature
