## run command ##
## python file.py --video videofile.mp4 
import easyocr
import numpy as np
import cv2
import argparse
import ctypes
ctypes.cdll.LoadLibrary('caffe2_nvrtc.dll')
import math 

##------INIT------##
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video")
args = vars(ap.parse_args())
videopath = args["video"]      
para = False
code_lang = 'en'
reader = easyocr.Reader(['en'])

##----start process about video----##
cap = cv2.VideoCapture(videopath) 
if (cap.isOpened()== False): 
    print("Error opening video stream or file")


fps = cap.get(cv2.CAP_PROP_FPS)
height = int(cap.get(4))
width = int(cap.get(3))
print('[INFO] height : ' + str(height) + ' , width : '+str(width))

name = videopath.split('.')[0]
print('[INFO] VIDEO NAME : ' + name)
print('[INFO] FPS : ' + str(fps))
# out = cv2.VideoWriter('new_'+name+'.avi', cv2.VideoWriter_fourcc(*'MJPG'), fps, (width,height))

print('[STATUS] READY FOR DETECT')
prev_bounds = []

while(True):
    ret, frame = cap.read()     # current frame is frame
    if ret == False:
        print('[INFO] End Of Video...')
        break

    #----------Start Detection--------
    bounds = []                   # current bound is bounds
    horizontal_list, free_list = reader.detect(frame)
    # for box in free_list:    # not use free_list
    #     x_min, y_min = box[0]
    #     x_max, y_max = box[2]
    #     center = ( (x_min+x_max)/2, (y_min+y_max)/2 )
    #     bounds.append([int(x_min), int(x_max), int(y_min), int(y_max), center])

    for box in horizontal_list:
        x_min = box[0]
        x_max = box[1]
        y_min = box[2]
        y_max = box[3]
        center = ( (x_min+x_max)/2, (y_min+y_max)/2 )
        bounds.append([int(x_min), int(x_max), int(y_min), int(y_max), center])
      #---------Detection End--------
    
    print('\n[INFO] Current frame :')
    cv2.imshow('frame', frame)
    cv2.waitKey(0)

    print('[INFO] Previous bounds ' + str(prev_bounds))
    if bounds == []:                # current frame have no text to check similarity and do recognition so move to the next frame
        print('[INFO] This current frame have no text')
        prev_bounds = bounds
        q = input('Would you like to go to next frame? [y/n] : ')       # for test
        if(q == 'y'):               # for test
            continue                       
        else:
            break
    elif prev_bounds != []:
        for c_b in bounds:
            similar = False
            for p_b in prev_bounds:
                dist = math.dist(c_b[4], p_b[4]) 
                print('[INFO] distance is {}'.format(dist))
                if dist <= 1.0:      # similar position by fine tune
                    similar = True
                    print('[INFO] Have similar position ROI, Next step is check differ')
                    print('[INFO] Center are {} and {}'.format(c_b[4], p_b[4]))
                    print('[INFO] distance is {}'.format(dist))
                    print('[INFO] Current ROI')
                    roi = frame[ c_b[2]:c_b[3], c_b[0]:c_b[1] ]
                    cv2.imshow('roi', roi)
                    cv2.waitKey(0)
                    
                    print('[INFO] Previous ROI')
                    p_roi = prev_frame[ p_b[2]:p_b[3], p_b[0]:p_b[1] ]
                    cv2.imshow('p_roi', p_roi)
                    cv2.waitKey(0)
                    # if diff == 'no dif' then b will append False, which mean skip the recognition.  if it similar then append True
            if similar == False:
                print("[INFO] Haven't similar with previous, Next step is Recognition")
                print('[INFO] Current ROI')
                c_roi = frame[ c_b[2]:c_b[3], c_b[0]:c_b[1] ]
                cv2.imshow('c_roi', c_roi)
                cv2.waitKey(0)
                    
    # else:     
    # # prev_bounds = [] so this current frame will do recognition the whole frame
    

    #----------Start Check Similarity---------
    #----------Check Similarity End---------

    #----------Start Recog---------
    print('[STATUS] Recognition')
    # use def
    #----------Recog End---------
    
    prev_bounds = bounds
    prev_frame = frame.copy()
    # Display the resulting frame
    q = input('Would you like to go to next frame? [y/n] : ')
    if(q != 'y'):
        break
    # out.write(frame)
    
# out.release()
cap.release()
cv2.destroyAllWindows()
print('[INFO] Thank you')