from import_python_library import *

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