from .import_lib import *

############### LANGUAGE ################
def lang(language):
    if 'english' in language:
        code_lang = 'en'
        reader = easyocr.Reader(['en'])
    elif 'chinese' in language:
        code_lang = 'zh-cn'
        reader = easyocr.Reader(['ch_sim', 'en'])
    elif 'french' in language:
        code_lang = 'fr'
        reader = easyocr.Reader(['fr', 'en'])
    elif 'thai' in language:
        code_lang = 'th'
        reader = easyocr.Reader(['th', 'en'])
    elif 'italian' in language:
        code_lang = 'it'
        reader = easyocr.Reader(['it', 'en'])
    elif 'japanese' in language:
        code_lang = 'ja'
        reader = easyocr.Reader(['ja', 'en'])
    elif 'korean' in language:  
        code_lang = 'ko'
        reader = easyocr.Reader(['ko', 'en'])
    elif 'german' in language:
        code_lang = 'de'
        reader = easyocr.Reader(['de', 'en'])
    else:  #spanish
        code_lang = 'es'
        reader = easyocr.Reader(['es', 'en'])
    return code_lang, reader

def tesseract_config(language):
    config = '-l '
    if 'auto' in language:
        config = ("-l eng+chi_sim+fra+tha+ita+jpn+kor+deu+spa --oem 3 --psm 6")
    else:
        for i in range(len(language)):
            lang = language[i]
            if lang == 'english':
                config += 'eng'
            if lang == 'chinese':
                config += 'chi_sim'
            if lang == 'french':
                config += 'fra'
            if lang == 'thai':
                config += 'tha'
            if lang == 'italian':
                config += 'ita'
            if lang == 'japanese':
                config += 'jpn'
            if lang == 'korean':  
                config += 'kor'
            if lang == 'german':
                config += 'deu'
            if lang == 'spanish':
                config += 'spa'
            if i != len(language):
                config += '+'
        config += ' --oem 3 --psm 6'
    return (config)
        
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

##################### LINK ######################
def video_link_url(url):
    video = new(url)
    best = video.getbest(preftype='mp4')
    # print(best.resolution, best.extension)
    best.download()
    # bestaudio = video.getbestaudio() 
    # bestaudio.download()

