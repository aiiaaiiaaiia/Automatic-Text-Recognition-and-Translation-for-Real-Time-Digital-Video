import easyocr
import PIL
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import cv2
import argparse
from google_trans_new import google_translator  
translator = google_translator() 
import ctypes
ctypes.cdll.LoadLibrary('caffe2_nvrtc.dll')

import math 
import sys
from scipy.linalg import norm
from scipy import average
from matplotlib import pyplot as plt

import datetime

from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip

from pafy import new

import pytesseract

import time
import os