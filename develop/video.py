from import_python_library import *
from def_init import *
from def_frame_similarity import *

##------ INIT ------##
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

videopath = args["video"]    
overlay = args["position"]      # above, below, text position
code_color = (0,0,255)          # default color : red
s = 30                          # default font size 
language = args["language"]     # video language
translanguage = args["translanguage"]     
font = ImageFont.truetype('angsau_0.ttf', s)
# para = False                  # default is False
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
prev_bounds = []
frist = True
prev_frame = 0
n_m = 100
print = True

print('[INFO] READY FOR DETECT AND RECOGNIZE \n')
print('[INFO] THE LIST OF FOUND SENTENSES :')

while(cap.isOpened()):
  ret, frame = cap.read() 
  if ret == False:
    print('[INFO] End Of Video...')
    break

  #----- frame similarity ------
  if(not frist):
    n_m = compare_images(frame, prev_frame)
  # if Manhattan norm(n_m) < 100 go to overlay process 
  # if Manhattan norm(n_m) >= 100 go to detect process 

  if(n_m >= 100):
    #------ detect --------
    bounds = []
    horizontal_list, free_list = reader.detect(frame)
    for box in horizontal_list:
      x_min = box[0]
      x_max = box[1]
      y_min = box[2]
      y_max = box[3]
      center = ( (x_min+x_max)/2, (y_min+y_max)/2 )
      bounds.append([int(x_min), int(x_max), int(y_min), int(y_max), center, 'vtext', False, '', 0, 0, 'code_lang'])

    if bounds == []:   
      prev_bounds = bounds
      pass

    #----- text center similarity ------
    # similarity = []
    if(prev_bounds != []):
      for index in range(len(bounds)):
        c_b = bounds[index]
        # similar = False
        for i in range(len(prev_bounds)):
          p_b = prev_bounds[i]
          dist = math.dist(c_b[4], p_b[4])      # distance
          if dist <= 6.0:                       # similar position by fine tune
            #----- similarity ROI -----
            c_roi = frame[ c_b[2]:c_b[3], c_b[0]:c_b[1] ]
            p_roi = prev_frame[ p_b[2]:p_b[3], p_b[0]:p_b[1] ]
            n_m_roi = compare_images(c_roi, p_roi)
            if(n_m_roi < 100):
              # similar = True
              bounds[index][5] = i
              bounds[index][6] = p_b[6] #vtext
              bounds[index][7] = p_b[7] #tran_text
              bounds[index][8] = p_b[8] #text_width
              bounds[index][9] = p_b[9] #text_height
              bounds[index][10] = p_b[10] #code_lang
            # else:
            #   bounds[index][5] = -1
          # else:
          #   bounds[index][5] = -1
        # similarity.append(similar)       
    # else:  # do the recognition process
      # for i in range(len(bounds)):
        # similarity.append(False)
        # bounds[i][5] = -1

    # 1 array
    # bounds = 0x_min, 1x_max, 2y_min, 3y_max, 4center, 
    # 5# of similar prev frame or false, 6vtext, 7trantext(from prev or recognition), 
    # 8text_width, 9text_height, 10code_lang

    # # of similar prev frame if False mean did the recognize

    #------- recognition -----
    sentrans = []
    for i in range(len(bounds)):
      c_b = bounds[i]
      if(c_b[5] == False):   # similarity = False, so need to recognize and translate
        # need to display because we found the new word.
        # if(lang == 'mult'): # use tesseract  and get src lang too for print
        print = True
        c_roi = frame[ c_b[2]:c_b[3], c_b[0]:c_b[1] ]
        c_rec = reader.recognize(c_roi)
        text = c_rec[1] 
        if(text == ''):  
            continue
        text = text.lower()
        trans = translator.translate(text, lang_src=code_lang, lang_tgt=code_translang)
        text_width, text_height = font.getsize(trans)
        bounds[i][6] = text
        bounds[i][7] = trans
        bounds[i][8] = text_width
        bounds[i][9] = text_height
        bounds[i][10] = code_lang
        
    if(print):
      print = False
      #   totalsec = int(i//fps)
      #   min = str(totalsec//60)  calculate again
      #   sec = str(totalsec%60)
      file = open("text.txt", "a")
      L = ["Current video time is ", hour, ':', min, ':', sec, "\n"]
      file.writelines(L)
      for i in range(len(bounds)):
        # L = [ bounds[i][6], " {", code_lang, "} : ", bounds[i][7] ] 
        # file.writelines(L) 
        file.close()
        
    prev_frame = frame.copy()
    frist = False

  # #------ overlay ------
  # for item in sentrans:
  #   text, code_lang, trans, startX, startY, endX, endY, text_width, text_height = item[:]
  #   #transparent
  #   if overlay == 'above':
  #     X=startX; Y = startY - 5; Xwidth = startX+text_width; Yheight = startY-text_height; a = 0.7 
  #     blk = np.zeros(frame.shape, np.uint8)
  #   elif overlay == 'under':
  #     X = startX; Y = endY+text_height; Xwidth = X+text_width; Yheight = Y-text_height; a = 0.7
  #     blk = np.zeros(frame.shape, np.uint8)
  #   else:
  #     X = startX ;Y = startY; Xwidth = endX; Yheight = endY; a = 1
  #     blk = np.zeros(frame.shape, np.uint8)
    
  #   cv2.rectangle(blk, (int(X), int(Y)), (int(Xwidth), int(Yheight)), (255, 255, 255), cv2.FILLED)
  #   frame = cv2.addWeighted(frame, 1, blk, a, gamma=0);

  #   #rectangle
  #   frame = cv2.rectangle(frame, (int(startX), int(startY)), (int(endX), int(endY)),code_color, 1)
    
  #   #text
  #   img_pil = Image.fromarray(frame)
  #   draw = ImageDraw.Draw(img_pil)
  #   if overlay == 'above' or overlay == 'under':
  #     Y = Y-text_height
  #   else:
  #     X = startX + (endX-startX)/2 - (text_width/2)
  #     Y = Y+(text_height/2)
  #   draw.text((X, Y), trans, font = font, fill = code_color)  # position, text, font, (b, g, r, a)
  #   frame = np.array(img_pil)
  
  prev_bounds = bounds  # after did overlay 
  
  out.write(frame)
    
     
out.release()
cap.release()
cv2.destroyAllWindows()
print('[INFO] Thank you')