import easyocr
import PIL
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import cv2
import argparse
from google_trans_new import google_translator  
translator = google_translator()  
# from translate import Translator
import ctypes
ctypes.cdll.LoadLibrary('caffe2_nvrtc.dll')

##------INIT------##
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
    code_lang = easyocr.Reader(['it', 'en'])
    reader = reader_it
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

##------INIT------##
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video")
ap.add_argument("-p", "--position", type=str,
	help="position to overlay the text")
ap.add_argument("-l", "--language", type=str,
	help="the input languages")
ap.add_argument("-t", "--translanguage", type=str,
	help="the translate language")
args = vars(ap.parse_args())

videopath = args["video"]       # 'NBC Nightly News.mp4'
overlay = args["position"]      # 'above'
code_color = (0,0,255)          # red
s = 30                          # font_size 
language = args["language"]     # 'english'
translanguage = args["translanguage"]     
font = ImageFont.truetype('angsau_0.ttf', s)
para = True
code_lang, reader = lang(language)
code_translang = translang(translanguage)

##----start process about video----##
cap = cv2.VideoCapture(videopath) 
if (cap.isOpened()== False): 
    print("Error opening video stream or file")
ret, frame = cap.read()
previous_frame = frame

fps = cap.get(cv2.CAP_PROP_FPS)
height = int(cap.get(4))
width = int(cap.get(3))
name = videopath.split('.')[0]
print('[INFO] VIDEO NAME : ' + name)
print('[INFO] FPS : ' + str(fps))
out = cv2.VideoWriter('new_'+name+'.avi', cv2.VideoWriter_fourcc(*'MJPG'), fps, (width,height))
vocab = []

print('[INFO] READY FOR DETECT AND RECOGNIZE \n')
print('[INFO] THE LIST OF FOUND SENTENSES :')
# same = 'y'
prev_bounds = []

while(cap.isOpened()):
  if ret == False:
    print('[INFO] End Of Video...')
    break

  #------ detect --------
  bounds = []
  horizontal_list, free_list = reader.detect(frame)
  for bound in free_list:
    x_min, y_min = bound[0]
    x_max, y_max = bound[2]
    bounds.append([int(x_min), int(x_max), int(y_min), int(y_max)])

  for bound in horizontal_list:
    x_min = box[0]
    x_max = box[1]
    y_min = box[2]
    y_max = box[3]
    bounds.append([int(x_min), int(x_max), int(y_min), int(y_max)])

  for b in bound:
    if b in prev_bounds:
      #------ tracking ------- 
      roi = frame[int(y_min) : int(y_max), int(x_min) : int(x_max)]
    

  prev_bounds = bounds

  ######################################################### previous_frame = frame.copy()
  ######################################################### ret, frame = cap.read()
  

 #------- recognition -----
  # if():
    bounds = reader.readtext(frame, paragraph=para)
    sentrans = []
    for bound in bounds:
      text = bound[1] 
      # prob = bound[2]
      if(text == ''):  #or (len(text) <= 7 and prob < 0.15)
        continue
      text = text.lower()
      startX, startY = bound[0][0]
      endX, endY = bound[0][2]

      trans = translator.translate(text, lang_src=code_lang, lang_tgt=code_translang)
      if (text not in vocab):
        # if same =='y':
        #   vocab = []
        #   totalsec = int(i//fps)
        #   min = str(totalsec//60)
        #   sec = str(totalsec%60)
        #   print('[INFO] VIDEO TIME : ' + min+'.'+sec)
        print("Original Text : {}  ({})  =  {}".format(text, code_lang , trans))
        vocab.append(text)
      #   same = 'n'
      # else:
      #   same = 'y'
      text_width, text_height = font.getsize(trans)
      sentrans.append([text, code_lang, trans, startX, startY, endX, endY, text_width, text_height])

  #------ overlay ------
  for item in sentrans:
    text, code_lang, trans, startX, startY, endX, endY, text_width, text_height = item[:]
    #transparent
    if overlay == 'above':
      X=startX; Y = startY - 5; Xwidth = startX+text_width; Yheight = startY-text_height; a = 0.7 
      blk = np.zeros(frame.shape, np.uint8)
    elif overlay == 'under':
      X = startX; Y = endY+text_height; Xwidth = X+text_width; Yheight = Y-text_height; a = 0.7
      blk = np.zeros(frame.shape, np.uint8)
    else:
      X = startX ;Y = startY; Xwidth = endX; Yheight = endY; a = 1
      blk = np.zeros(frame.shape, np.uint8)
    
    cv2.rectangle(blk, (int(X), int(Y)), (int(Xwidth), int(Yheight)), (255, 255, 255), cv2.FILLED)
    frame = cv2.addWeighted(frame, 1, blk, a, gamma=0);

    #rectangle
    frame = cv2.rectangle(frame, (int(startX), int(startY)), (int(endX), int(endY)),code_color, 1)
    
    #text
    img_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(img_pil)
    if overlay == 'above' or overlay == 'under':
      Y = Y-text_height
    else:
      X = startX + (endX-startX)/2 - (text_width/2)
      Y = Y+(text_height/2)
    draw.text((X, Y), trans, font = font, fill = code_color)  # position, text, font, (b, g, r, a)
    frame = np.array(img_pil)

    out.write(frame)
    
     
out.release()
cap.release()
cv2.destroyAllWindows()
print('[INFO] Thank you')