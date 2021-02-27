# -*- coding: utf-8 -*-
from import_lib import *
from utils import *

class RT_ATRT():
	def __init__(self):
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
		s = 30                          # default font size 
		language = args["language"]     # video language
		translanguage = args["translanguage"]

		############ Parameter #############
		self.videopath = args["video"]
		self.overlay = args["position"]      # above, below, text position
		self.frame_similarity_threshold = 100
		self.roi_distance_threshold = 6.0
		self.multi_input_language = language
		self.font = ImageFont.truetype('angsau_0.ttf', s)
		# para = False                  # default is False
		self.code_lang, self.reader = lang(language)
		self.code_translang = translang(translanguage)
		self.code_color = (0,0,255)          # default color : red


		self.cap = cv2.VideoCapture(self.videopath)
		self.vdo_name = self.videopath.split('.')[0]
		# try:
		self.cap.isOpened()
		self.fps = self.cap.get(cv2.CAP_PROP_FPS)
		self.output_vdo_writer = self.create_vdo_output_writer()
		
		self.process_vdo()
		# except Exception as e: print(e)

	def create_vdo_output_writer(self):
		height = int(self.cap.get(4))
		width = int(self.cap.get(3))
		vdo_writer = cv2.VideoWriter('new_'+self.vdo_name+'.avi', cv2.VideoWriter_fourcc(*'MJPG'), self.fps, (width,height))
		return vdo_writer

	def process_vdo(self):
		prev_bounds = []
		is_first_frame = True
		prev_frame = 0
		n_m = 100
		print_text = True
		frame_idx = 1

		while(self.cap.isOpened()):
			bounds = []
			ret, frame = self.cap.read()
			if ret == False:
				print('[INFO] End Of Video...')
				break
			
			if is_first_frame:
				bounds = self.text_detection(frame)
				if bounds == []:
					result = bounds
				else:
					result = self.recognition(bounds, frame)
					self.write_new_text_to_txt(result, frame_idx * (1.0 / self.fps))
				is_first_frame = False
			else:
				if(self.is_frame_similar(prev_frame, frame)):
					## Go for Overlay
					self.overlay_text()
				else:
					## Go for Detect text
					bounds = self.text_detection(frame)
					if bounds == []:
						result = bounds
					else:
						## Overlay_similarity_roi
						bounds = self.overlay_similarity_roi(bounds, prev_bounds, frame, prev_frame)
						result = self.recognition(bounds, frame)
						self.write_new_text_to_txt(result, frame_idx * (1.0 / self.fps))
						
						
			output_frame = self.draw_result(frame, result)
			self.output_vdo_writer.write(output_frame)

			### BOBO Sent progess to flask
				
			prev_frame = frame
			prev_bounds = bounds
			frame_idx += 1
			print(frame_idx)
		
		out.release()
		cap.release()
		cv2.destroyAllWindows()
		print('[INFO] Thank you')
	
	def recognition(self, bounds, frame):
		if(self.is_multi_language()):
			## Tesseract
			## BOBO AIII
			pass
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
		print(n_m)
		if n_m >= self.frame_similarity_threshold:
			return False
		else:
			print("frame is similar")
			return True
	
	def is_roi_similar(self, roi, prev_roi):
		return False

	def text_detection(self, frame):
		bounds = []
    	#------ detect --------
		horizontal_list, free_list = self.reader.detect(frame)
		for box in horizontal_list:
			x_min = box[0]
			x_max = box[1]
			y_min = box[2]
			y_max = box[3]
			center = ( (x_min+x_max)/2, (y_min+y_max)/2 )
			bounds.append([int(x_min), int(x_max), int(y_min), int(y_max), center, -1, 'vtext',  'trantext', 0, 0, 'code_lang'])
		return bounds

	def overlay_similarity_roi(self, bounds, prev_bounds, frame, prev_frame):
		for bound_idx in range(len(bounds)):
			bound = bounds[bound_idx]
			for prev_bound_idx in range(len(prev_bounds)):
				prev_bound = prev_bounds[prev_bound_idx]
				dist = math.dist(bound[4], prev_bound[4])      # distance

				if dist <= self.roi_distance_threshold:                       # similar position by fine tune
					roi = frame[ bound[2]:bound[3], bound[0]:bound[1] ]
					prev_roi = prev_frame[ prev_bound[2]:prev_bound[3], prev_bound[0]:prev_bound[1] ]

					if(self.is_roi_similar(roi, prev_roi)):
						## Overlay Similar_roi
						bounds[index][5] = prev_bound_idx
						bounds[index][6] = prev_bound[6] #vtext
						bounds[index][7] = prev_bound[7] #tran_text
						bounds[index][8] = prev_bound[8] #text_width
						bounds[index][9] = prev_bound[9] #text_height
						bounds[index][10] = prev_bound[10] #code_lang
		return bounds

    #------- recognition -----
	def easy_ocr_recognition(self, bounds, frame):
		for index in range(len(bounds)):
			c_b = bounds[index]
			if(c_b[5] == -1):   # similarity = -1, so need to recognize and translate
				print_text = True
				c_roi = frame[ c_b[2]:c_b[3], c_b[0]:c_b[1] ]
				c_rec = self.reader.recognize(c_roi)
				text = c_rec[0][1] 
				text = text.lower()
				trans = translator.translate(text, lang_src=self.code_lang, lang_tgt=self.code_translang)
				text_width, text_height = self.font.getsize(trans)
				bounds[index][6] = text
				bounds[index][7] = trans
				bounds[index][8] = text_width
				bounds[index][9] = text_height
				bounds[index][10] = self.code_lang
		return bounds

	def write_new_text_to_txt(self, result, vdo_time_sec):
		conversion = datetime.timedelta(seconds=vdo_time_sec)
		converted_time = str(conversion)
		print(converted_time)
		file = open("text.txt", "a")
		L = ["Current video time is ", converted_time, "\n"]
		file.writelines(L)
		for i in range(len(result)):
			if(result[i][6] == ''):
				continue
			L = (result[i][6] + " {" + str(self.code_lang) + "} : " + result[i][7] + '\n').encode("utf8") 
			print(L)
			## BOBO dont forget implement this dunction after tesseract added
			file.writelines(str(L))
			print(result[i])
		file.close()
		
	
	def draw_result(self, frame, result):
		output_frame = frame
		for r in result:
			startX, endX, startY, endY, position, number_prev_frame, ori_text,  tran_text, text_width, text_height, code_lang = r[:]
			#---- transparent
			if self.overlay == 'above':
				X=startX; Y = startY - 5; Xwidth = startX+text_width; Yheight = startY-text_height; a = 0.7
			elif self.overlay == 'under':
				X = startX; Y = endY+text_height; Xwidth = X+text_width; Yheight = Y-text_height; a = 0.7
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

def main():
	rt_atrt = RT_ATRT()

if __name__ == "__main__":
    main()