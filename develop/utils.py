from import_lib import *

############### LANGUAGE ################
def lang(language):
    if language == 'detect':
        code_lang = 'all'
        reader = easyocr.Reader(['en']) 
    elif language == 'english':
        code_lang = 'en'
        reader = easyocr.Reader(['en'])
    elif language == 'chinese':
        code_lang = 'zh-cn'
        reader = easyocr.Reader(['ch_sim', 'en'])
    elif language == 'french':
        code_lang = 'fr'
        reader = easyocr.Reader(['fr', 'en'])
    elif language == 'thai':
        code_lang = 'th'
        reader = easyocr.Reader(['th', 'en'])
    elif language == 'italian':
        code_lang = 'it'
        reader = easyocr.Reader(['it', 'en'])
    elif language == 'japanese':
        code_lang = 'ja'
        reader = easyocr.Reader(['ja', 'en'])
    elif language == 'korean':  
        code_lang = 'ko'
        reader = easyocr.Reader(['ko', 'en'])
    elif language == 'german':
        code_lang = 'de'
        reader = easyocr.Reader(['de', 'en'])
    else:  #spanish
        code_lang = 'es'
        reader = easyocr.Reader(['es', 'en'])
    return code_lang, reader

def translang(translanguage):
  if translanguage == 'thai':
    code_translang = 'th'
  else: 
    code_translang = 'en'
  return code_translang

##################### IMAGE ######################

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
    return True

##################### LINK ######################
def video_link_url(url):
    video = new(url)
    # https://www.youtube.com/watch?v=KuncL9Fb_D0
    # https://www.youtube.com/watch?v=DKYATp0M9f8
    best = video.getbest(preftype='mp4')
    # print(best.resolution, best.extension)
    best.download()

    # bestaudio = video.getbestaudio() 
    # bestaudio.download()
    return True

# video_link_url('https://www.youtube.com/watch?v=AORfC4tELco')