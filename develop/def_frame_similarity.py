from import_python_library import *

def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng

def compare_images(frame, prev_frame):
    current_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    current_frame_gray_edge = cv2.Canny(current_frame_gray,100,200)
    prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)    
    prev_frame_gray_edge = cv2.Canny(prev_frame_gray,100,200)

    img1 = normalize(current_frame_gray_edge)
    img2 = normalize(prev_frame_gray_edge)
    diff = img1 - img2  
    m_norm = np.sum(abs(diff))  # Manhattan norm
    # z_norm = norm(diff.ravel(), 0)  # Zero norm
    return (m_norm)

def roi_simlarity(roi, prev_roi):
    g_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    g_prev_roi = cv2.cvtColor(prev_roi, cv2.COLOR_BGR2GRAY)

    method = cv2.TM_SQDIFF_NORMED