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
    code_lang = []
    if 'auto' in language:
        config = ("-l eng+chi_sim+fra+tha+ita+jpn+kor+deu+spa --oem 3 --psm 6")
    else:
        for i in range(len(language)):
            lang = language[i]
            if lang == 'english':
                config += 'eng'
                code_lang.append(lang)
            elif lang == 'chinese':
                config += 'chi_sim'
                code_lang.append(lang)
            elif lang == 'french':
                config += 'fra'
                code_lang.append(lang)
            elif lang == 'thai':
                config += 'tha'
                code_lang.append(lang)
            elif lang == 'italian':
                config += 'ita'
                code_lang.append(lang)
            elif lang == 'japanese':
                config += 'jpn'
                code_lang.append(lang)
            elif lang == 'korean':  
                config += 'kor'
                code_lang.append(lang)
            elif lang == 'german':
                config += 'deu'
                code_lang.append(lang)
            elif lang == 'spanish':
                config += 'spa'
                code_lang.append(lang)
            if i != (len(language)-1):
                config += '+'
        config += ' --oem 3 --psm 6'
    return (config, code_lang)
        
def translang(translanguage):
  if translanguage == 'thai':
    code_translang = 'th'
  else: 
    code_translang = 'en'
  return code_translang

##################### IMAGE ######################
def compare_images(frame, prev_frame):
    current_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    current_frame_gray_edge = cv2.Canny(current_frame_gray,100,200)
    prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)    
    prev_frame_gray_edge = cv2.Canny(prev_frame_gray,100,200)

    ssim_value = ssim(current_frame_gray_edge, prev_frame_gray_edge)    
    return (ssim_value)

##################### LINK ######################
def video_link_url(url):
    video = new(url)
    best = video.getbest(preftype='mp4')
    # print(best.resolution, best.extension)
    best.download()
    # bestaudio = video.getbestaudio() 
    # bestaudio.download()

