from time import time
# from wand.image import Image
from PIL import Image as PI
import pyocr, io, re, os, fnmatch, csv
import pyocr.builders
import pypdfocr
import PyPDF2
from sys import platform

start_time = time()
tool = pyocr.get_available_tools()[0]
lang = tool.get_available_languages()[0]

results_file = [['DocumentName', 'WordsFound']] #, 'Text'
file_list = []
search_words = ['adult', 'alcoh', 'alcohol', 'apparel', 'beer', 'campaign', 'candidat', 'cantina', 'capital', 'casino', 'celebra', 'chair', 'church', 'cigar', 'clinic', 'cloth', 'club', 'college', 'comput', 'contribu', 'court', 'credit', 'danc', 'dentist', 'dinero', 'dinner', 'doctor', 'donation', 'entertain', 'escort', 'exotic', 'favor', 'festiv', 'fiest', 'fine', 'flower', 'gambl', 'game', 'gaming', 'gift', 'govern', 'home', 'hospit', 'hotel', 'hotline', 'hous', 'jail', 'jewel', 'lawyer', 'liqu', 'liquor', 'lunch', 'luxur', 'membership', 'monitor', 'music', 'party', 'poker', 'polic', 'politic', 'recreation', 'recruit', 'representa', 'restaur', 'reward', 'school', 'server', 'social', 'sport', 'taver', 'tele', 'theater', 'theatre', 'university', 'vacati', 'visa', 'welfare', 'wine']
count = 0

path = os.getcwd()

t0 = time()
print "Start renaming files"
for filename in os.listdir("."):
  if fnmatch.fnmatch(filename, "*.pdf"):
    os.rename(os.path.join(path, filename), os.path.join(path, filename.replace(' ', '_')))
print "Renaming files complete:",round(time()-t0,3),"s"

for filename in os.listdir("."):
  if fnmatch.fnmatch(filename, "*.pdf"):
    file_list.append(str(filename))


for the_file in file_list:
  t0 = time()
  print the_file
  count += 1
  print count

  os.system("pypdfocr " + the_file)
  print "Complete OCR on ",the_file,round((time()-t0)/60,2),"m"
  print "Total script time elapsed:",round((time()-start_time)/60,2),"m\n"


file_list = []
count = 0
for filename in os.listdir("."):
  if fnmatch.fnmatch(filename, "*ocr.pdf"):
    file_list.append(str(filename))

for the_file in file_list:
  t0 = time()
  print the_file
  count += 1
  print count
  final_text = []
  found_words = []
  all_text = ''

  pdfFileObj = open(the_file, 'rb')
  pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
  for i in range(0,pdfReader.numPages):
    pageObj = pdfReader.getPage(i)
    final_text.append(pageObj.extractText())

  # all_text = re.sub(r'\W+', '', " ".join(final_text)).lower()

  all_text = re.sub(r'([^\s\w]|_)+', '', " ".join(final_text)).lower()

  for word in search_words:
    if word in all_text:
      found_words.append(word)
  if len(found_words) > 0:
    results_file.append([the_file, " ".join(found_words)])#, all_text
  else:
    results_file.append([the_file, "Nothing was found"])#, all_text
  print "File read:",round(time()-t0,3),"s"
  print "Total script time elapsed:",round((time()-start_time)/60,2),"m\n"
ocr_output = 'OCROutput' + str(time()) + '.csv'
with open(ocr_output, 'wb') as csv_file:
  wr = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  for i in results_file:
    wr.writerow(i)
os.system("sublime " + ocr_output)

print "Script End:",round((time()-start_time)/60,2),"m"

if platform == "darwin":
  os.system('say "scanning is complete"')
else:
  import subprocess
  subprocess.call(['speech-dispatcher'])        #start speech dispatcher
  subprocess.call(['spd-say', '"your process has finished"'])
  
################################ ALL PREVIOUS CODE #################################
#   t0 = time()
#   print "Images loaded:",round(time()-t0,3),"s"
#   req_image = []
#   final_text = []
#   found_words = []
#   all_text = ''

#   print the_file
#   count += 1
#   print count

#   t0 = time()
#   print "Load images"
#   image_pdf = Image(filename="./" + the_file, resolution=300)
#   image_jpeg = image_pdf.convert('jpeg')
#   print "Images loaded:",round(time()-t0,3),"s"

#   t0 = time()
#   print "Creating blobs"
#   for img in image_jpeg.sequence:
#     img_page = Image(image=img)
#     req_image.append(img_page.make_blob('jpeg'))
#   print "Blobs created:",round(time()-t0,3),"s"

#   t0 = time()
#   print "Using Tessaract"
#   for img in req_image: 
#     txt = tool.image_to_string(
#       PI.open(io.BytesIO(img)),
#       lang=lang,
#       builder=pyocr.builders.TextBuilder()
#     )
#     final_text.append(txt)
#   print "Tessaract projected:",round(time()-t0,3),"s"

#   # text_file = open("Output.txt", "w")
#   # re.sub(r'\W+', '', " ".join(final_text))

#   # text_file.write(re.sub(r'([^\s\w]|_)+', '', " ".join(final_text)).lower())
#   # text_file.write(re.sub(r'\W+', '', " ".join(final_text)).lower())
#   # text_file.close()
#   all_text = re.sub(r'\W+', '', " ".join(final_text)).lower()

#   for word in search_words:
#     if word in all_text:
#       found_words.append(word)
#   if len(found_words) > 0:
#     results_file.append([the_file, " ".join(found_words), all_text])#
#   else:
#     results_file.append([the_file, "Nothing was found", all_text])#
#   print "Total script time elapsed:",round((time()-start_time)/60,2),"m\n"
# # os.system("sublime Output.txt")
# # print " ".join(final_text)
# ocr_output = 'OCROutput' + str(time()) + '.csv'
# with open(ocr_output, 'wb') as csv_file:
#   wr = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#   for i in results_file:
#     wr.writerow(i)
# os.system("sublime " + ocr_output)