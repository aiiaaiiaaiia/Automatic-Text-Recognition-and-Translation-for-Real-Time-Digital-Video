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

import math 
import sys
from scipy.linalg import norm
from scipy import average
from matplotlib import pyplot as plt
# from skimage.measure import compare_ssim
# from skimage.metrics import structural_similarity
# import imagehash

# from scipy.misc import imread
