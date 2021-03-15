# -*- coding: utf-8 -*-
from .import_lib import *
from .utils import *
class RT_ATRT():
	def __init__(self, video, position, language, translanguage, output_path):
		s = 20                          # default font size 
		self.language = language     # video language
		self.translanguage = translanguage
		self.output_path = output_path

		############ Parameter #############
		self.videopath = video
		self.overlay = position      # above, below, text position
		self.frame_similarity_threshold = 0.05
		self.roi_similarity_threshold = 0.98
		self.roi_distance_threshold = 6.0
		self.multi_input_language = self.language
		self.font = ImageFont.truetype('angsau_0.ttf', s)
		# para = False                  # default is False
		if( (len(language) == 1 and 'auto detect' not in language) or ( len(language) == 2 and ('english' in language)) ):
			self.code_lang, self.reader = lang(self.language)
		else:  #multiple
			self.config = tesseract_config(self.language)
			self.reader = easyocr.Reader(['en']) 
		self.code_translang = translang(self.translanguage)
		self.code_color = (0,0,255)          # default color : red

		self.cap = cv2.VideoCapture(self.videopath)
		self.vdo_name = os.path.basename(self.videopath).split(".")[0]
		self.out_text_file = open(self.output_path + str(self.vdo_name) + "_text.txt", "a", encoding="utf-8")
		# try:
		self.extract_video_audio(self.videopath)
		self.cap.isOpened()
		self.fps = self.cap.get(cv2.CAP_PROP_FPS)
		self.output_vdo_writer = self.create_vdo_output_writer()
		
		self.process_vdo()
		self.add_video_audio(self.vdo_name)
		# except Exception as e: print(e)

	def extract_video_audio(self, path):
		clip = VideoFileClip(path)
		clip.audio.write_audiofile(self.output_path + str(self.vdo_name) + "_audio.mp3")

	def add_video_audio(self):
		newclip = VideoFileClip(self.output_path + self.vdo_name + '.mp4')
		newaudio = AudioFileClip(self.output_path + str(self.vdo_name) + "_audio.mp3")
		final = newclip.set_audio(newaudio)
		final.write_videofile(self.output_path + 'processed_' + self.vdo_name + '.mp4')

	def create_vdo_output_writer(self):
		height = int(self.cap.get(4))
		width = int(self.cap.get(3))
		vdo_writer = cv2.VideoWriter(self.output_path +self.vdo_name+'.mp4', 0x7634706d, self.fps, (width,height))
		# cv2.VideoWriter_fourcc(*'MP4V')  mp4
		# cv2.cv.CV_FOURCC(*'XVID')  avi
		return vdo_writer

	def process_vdo(self):
		prev_bounds = []
		is_first_frame = True
		prev_frame = 0
		n_m = 1
		frame_idx = 1

		while(self.cap.isOpened()):
			bounds = []
			ret, frame = self.cap.read()
			if ret == False:
				print('[INFO] End Of Video...')
				break
			# frame skip
			print(frame_idx)
			if((frame_idx-1) % 6 != 0):
				start_while = time.time()
				print('skip')
				# go to overlays
				result = prev_bounds
			else:
				start_while = time.time()
				if is_first_frame:
					bounds = self.text_detection(frame)
					# if bounds == []:
					# 	result = bounds
					# else:
					if bounds != []:
						result = self.recognition(bounds, frame)
						self.write_new_text_to_txt(result, frame_idx * (1.0 / self.fps))
					is_first_frame = False
				else:
					
					if(self.is_frame_similar(prev_frame, frame)):
						## Go for Overlay
						# self.draw_result(frame, bounds)     # Just fixed
						result = prev_bounds
					else:
						## Go for Detect text
						bounds = self.text_detection(frame)
						# if bounds == []:
						# 	result = bounds
						# else:
						if bounds != []:
							## Overlay_similarity_roi
							if prev_bounds != []:
								bounds = self.overlay_similarity_roi(bounds, prev_bounds, frame, prev_frame)
							result = self.recognition(bounds, frame)
							self.write_new_text_to_txt(result, frame_idx * (1.0 / self.fps))

			if bounds == []:
				output_frame = frame
			else:
				output_frame = self.draw_result(frame, result)
			self.output_vdo_writer.write(output_frame)

			### BOBO Sent progess to flask
				
			prev_frame = frame
			prev_bounds = result
			frame_idx += 1
			end_while = time.time()
			print('time per frame ', end_while -start_while)
		
		self.output_vdo_writer.release()
		# cap.release()
		cv2.destroyAllWindows()
		print('[INFO] Thank you')
	
	def recognition(self, bounds, frame):
		if(self.is_multi_language()):
			## Tesseract
			result = self.tesseract_recognition(bounds, frame)
		else:
			## easy_ocr
			result = self.easy_ocr_recognition(bounds, frame)
		return result
	
	def is_multi_language(self):
		return False

	def is_frame_similar(self, prev_frame, frame):
		# if Manhattan norm(n_m) < frame_similarity_threshold go to overlay process 
		# if Manhattan norm(n_m) >= frame_similarity_threshold go to detect process 
		n_m = compare_images(frame, prev_frame)
		print('compare_images ', n_m)
		# print(n_m)
		if n_m > self.frame_similarity_threshold:
			return False
		else:
			return True
	
	def is_roi_similar(self, roi, prev_roi):
		# Template matching 
		g_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
		g_prev_roi = cv2.cvtColor(prev_roi, cv2.COLOR_BGR2GRAY)

		res = cv2.matchTemplate(g_roi,g_prev_roi,cv2.TM_CCOEFF_NORMED)
		loc = np.where( res >= self.roi_similarity_threshold)
		l  = [pt for pt in zip(*loc[::-1])] 
		return (len(l) == 1) 

	def text_detection(self, frame):
		bounds = []
    	#------ detect --------
		horizontal_list, free_list = self.reader.detect(frame)
		# print('free_list\n', free_list)
		# for box in free_list:
		# 	x_min = max(min(box[0][0],box[1][0],box[2][0],box[3][0],), 0)
		# 	x_max = max(max(box[0][0],box[1][0],box[2][0],box[3][0],), 0)
		# 	y_min = max(min(box[0][1],box[1][1],box[2][1],box[3][1],), 0)
		# 	y_max = max(max(box[0][1],box[1][1],box[2][1],box[3][1],), 0)
		# 	center = ( (x_min+x_max)/2, (y_min+y_max)/2 )
		# 	x = [int(x_min), int(x_max), int(y_min), int(y_max), center, -1, 'vtext',  'trantext', 0, 0, 'code_lang'])
		# 	print(x)
			# bounds.append([int(x_min), int(x_max), int(y_min), int(y_max), center, -1, 'vtext',  'trantext', 0, 0, 'code_lang'])
		for box in horizontal_list:
			x_min = max(box[0], 0)
			x_max = max(box[1], 0)
			y_min = max(box[2], 0)
			y_max = max(box[3], 0)
			center = ( (x_min+x_max)/2, (y_min+y_max)/2 )
			bounds.append([int(x_min), int(x_max), int(y_min), int(y_max), center, -1, 'vtext',  'trantext', 0, 0, 'code_lang'])
		return bounds

	def overlay_similarity_roi(self, bounds, prev_bounds, frame, prev_frame):
		for bound_idx in range(len(bounds)):
			bound = bounds[bound_idx]
			for prev_bound_idx in range(len(prev_bounds)):
				prev_bound = prev_bounds[prev_bound_idx]
				dist = math.dist(bound[4], prev_bound[4])      # distance
				# must use width and heigth for criteria as well
				if dist <= self.roi_distance_threshold:                       # similar position by fine tune
					roi = frame[ min(bound[2], prev_bound[2]):max(bound[3], prev_bound[3]), min(bound[0], prev_bound[0]):max(bound[1], prev_bound[1]) ]
					prev_roi = prev_frame[ min(bound[2], prev_bound[2]):max(bound[3], prev_bound[3]), min(bound[0], prev_bound[0]):max(bound[1], prev_bound[1]) ]
					if(self.is_roi_similar(roi, prev_roi)):
						## Overlay Similar_roi
						bounds[bound_idx][5] = prev_bound_idx
						bounds[bound_idx][6] = prev_bound[6] #vtext
						bounds[bound_idx][7] = prev_bound[7] #tran_text
						bounds[bound_idx][8] = prev_bound[8] #text_width
						bounds[bound_idx][9] = prev_bound[9] #text_height
						bounds[bound_idx][10] = prev_bound[10] #code_lang
		return bounds

    #------- recognition -----
	def easy_ocr_recognition(self, bounds, frame):
		delete_index = []
		for index in range(len(bounds)):
			c_b = bounds[index]
			if(c_b[5] == -1):   # similarity = -1, so need to recognize and translate
				c_roi = frame[ c_b[2]:c_b[3], c_b[0]:c_b[1] ]
				# print('{} {} {} {}'.format(c_b[2],c_b[3], c_b[0],c_b[1]))
				# c_roi_gray = cv2.cvtColor(c_roi, cv2.COLOR_BGR2GRAY)
				c_rec = self.reader.recognize(c_roi)
				text = c_rec[0][1] 
				if(text == '' or text.isnumeric()):
					delete_index.append(c_b)
					continue
				text = text.lower()
				detect_result = translator.detect(text)
				if detect_result[0] not in [self.code_lang]:
					detect_result = 'en'
				trans = translator.translate(text, lang_src=self.code_lang, lang_tgt=self.code_translang)
				text_width, text_height = self.font.getsize(trans)
				bounds[index][6] = text
				bounds[index][7] = trans
				bounds[index][8] = text_width
				bounds[index][9] = text_height
				bounds[index][10] = detect_result  #self.code_lang
		for delete in delete_index:
			bounds.remove(delete)
		return bounds

	def tesseract_recognition(self, bounds, frame):
		delete_index = []
		for index in range(len(bounds)):
			c_b = bounds[index]
			if(c_b[5] == -1):   # similarity = -1, so need to recognize and translate
				c_roi = frame[ c_b[2]:c_b[3], c_b[0]:c_b[1] ]
				c_roi_rgb = cv2.cvtColor(c_roi, cv2.COLOR_BGR2RGB)
				text = pytesseract.image_to_string(c_roi_rgb, config = self.config)
				if(text == '' or text.isnumeric()):
					delete_index.append(c_b)
					continue
				text = text.lower()
				detect_result = translator.detect(text)
				trans = translator.translate(text, lang_src=self.code_lang, lang_tgt=self.code_translang)
				text_width, text_height = self.font.getsize(trans)
				bounds[index][6] = text
				bounds[index][7] = trans
				bounds[index][8] = text_width
				bounds[index][9] = text_height
				bounds[index][10] = detect_result
		for delete in delete_index:
			bounds.remove(delete)
		return bounds


	def write_new_text_to_txt(self, result, vdo_time_sec):
		conversion = datetime.timedelta(seconds=vdo_time_sec)
		converted_time = str(conversion)
		recognize = [item[5] for item in result]
		if(-1 in recognize):
			L = ["\nCurrent video time is ", converted_time, "\n"]
			self.out_text_file = open(self.output_path + str(self.vdo_name) + "_text.txt", "a", encoding="utf-8")
			self.out_text_file.writelines(L)
			for i in range(len(result)):
				if(result[i][5] == -1):
					L = [ result[i][6] + " {" + str(result[i][10]) + "} : " + result[i][7] + "\n"]
					self.out_text_file.writelines(L)
					# print(result[i][6])
			self.out_text_file.close()
		
	def draw_result(self, frame, result):
		output_frame = frame
		for r in result:
			startX, endX, startY, endY, position, number_prev_frame, ori_text,  tran_text, text_width, text_height, code_lang = r[:]
			#---- transparent
			if self.overlay == 'above':
				X=startX; Y = startY - 5; Xwidth = startX+text_width; Yheight = startY-text_height; a = 0.7
				if(Yheight >= self.cap.get(4)):
					X = startX ;Y = startY; Xwidth = endX; Yheight = endY; a = 1
			elif self.overlay == 'under':
				X = startX; Y = endY+text_height; Xwidth = X+text_width; Yheight = Y-text_height; a = 0.7
				if(Y >= self.cap.get(4)):
					X = startX ;Y = startY; Xwidth = endX; Yheight = endY; a = 1
			else:
				X = startX ;Y = startY; Xwidth = endX; Yheight = endY; a = 1
		
			blk = np.zeros(frame.shape, np.uint8)
		
			cv2.rectangle(blk, (int(X), int(Y)), (int(Xwidth), int(Yheight)), (255, 255, 255), cv2.FILLED)
			output_frame = cv2.addWeighted(output_frame, 1, blk, a, gamma=0)

			#---- rectangle
			output_frame = cv2.rectangle(output_frame, (int(startX), int(startY)), (int(endX), int(endY)),self.code_color, 1)
		
			#---- text
			img_pil = Image.fromarray(output_frame)
			draw = ImageDraw.Draw(img_pil)
			if self.overlay == 'above' or self.overlay == 'under':
				Y = Y-text_height
			else:
				X = startX + (endX-startX)/2 - (text_width/2)
				Y = Y+(text_height/2)
			draw.text((X, Y), tran_text, font = self.font, fill = self.code_color)  # position, text, font, (b, g, r, a)
			output_frame = np.array(img_pil)
		return output_frame