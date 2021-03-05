## run command ##
## python file.py --video videofile.mp4 

from import_lib import *
# from utils import *

def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng

def compare_images(img1, img2):
    img1 = normalize(current_frame_gray_edge)
    img2 = normalize(prev_frame_gray_edge)
    diff = img1 - img2  
    m_norm = np.sum(abs(diff))  # Manhattan norm
    # z_norm = norm(diff.ravel(), 0)  # Zero norm
    return (m_norm)

##------INIT------##
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video")
args = vars(ap.parse_args())
videopath = args["video"]      

##----start process about video----##
cap = cv2.VideoCapture(videopath) 
if (cap.isOpened()== False): 
    print("Error opening video stream or file")


fps = cap.get(cv2.CAP_PROP_FPS)
height = int(cap.get(4))
width = int(cap.get(3))
print('[INFO] height : ' + str(height) + ' , width : '+str(width))

name = videopath.split('.')[0]
# print('[INFO] VIDEO NAME : ' + name)
# print('[INFO] FPS : ' + str(fps))
# out = cv2.VideoWriter('new_'+name+'.avi', cv2.VideoWriter_fourcc(*'MJPG'), fps, (width,height))

# print('[STATUS] READY')
prev_frame = 0
i = 1  # frame number 

while(True):
    ret, frame = cap.read()     # current frame is frame
    # if ret == False:
        # print('[STATUS] End Of Video...')
        # break
    if(i >= 240 ):       # for test
        # print('[INFO] Current frame : ' + str(i))
        # print('[INFO] Comparing frame : {} and {}'.format(i-1, i))

        # current_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # current_frame_gray_edge = cv2.Canny(current_frame_gray,100,200)
        # # cv2.imwrite("./develop/compare3_edge//" + str(i) + '_frame.png' ,current_frame_gray_edge)
        # prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY) 
        # prev_frame_gray_edge = cv2.Canny(prev_frame_gray,100,200)
        
        # pixel = current_frame_gray_edge.size
        
        # first method
        # (score, diff) = structural_similarity(current_frame_gray, prev_frame_gray, full=True)
        # diff = (diff * 255).astype("uint8")
        # cv2.imwrite("./develop/compare//" + str(i-1) + '_' + str(i) +'_diff.png' ,diff)
        # print('[INFO] Different : {}\n'.format(score))

        #second method
        # cfrane_hash = imagehash.average_hash(frame)
        # pframe_hash = imagehash.average_hash(prev_frame)
        # print('[INFO] Different : {}\n'.format(hash - otherhash))

        #third method
        # n_m, n_0 = compare_images(current_frame_gray_edge, prev_frame_gray_edge)
        # n_m = compare_images(current_frame_gray_edge, prev_frame_gray_edge)
        # print("Manhattan norm: " + str(n_m) + " / per pixel: " + str(n_m/pixel))
        # print("Zero norm: "+ str(n_0)+ " / per pixel: " + str(n_0*1.0/pixel))
        
        cv2.imwrite("./jpjp//" + str(i) + '_frame.png' ,frame)
        # cv2.imshow('frame', frame)
        # cv2.waitKey(0)

        #----------Start Check Similarity---------
        #----------Check Similarity End---------

        
        # Display the resulting frame
        # q = input('Would you like to go to next frame? [y/n] : ')
        # if(q != 'y'):
        #     break
        # out.write(frame)
    if (i == 300):  # for test
        break

    # prev_frame = frame.copy()
    i += 1

# out.release()
cap.release()
cv2.destroyAllWindows()
print('[INFO] Thank you')