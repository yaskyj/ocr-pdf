from time import time
import pyocr, io, re, os, fnmatch, csv
import pyocr.builders
import pypdfocr
import PyPDF2
from sys import platform

start_time = time()
tool = pyocr.get_available_tools()[0]
lang = tool.get_available_languages()[0]

results_file = [['DocumentName', 'WordsFound']]
file_list = []
search_words = ['adult', 'alcohol', 'apparel', 'beer', 'campaign', 'candidate', 'casino', 'celebration', 'chair', 'church', 'cigar', 'clinic', 'club', 'college', 'computer', 'court', 'dance', 'dentist', 'dinero', 'doctor', 'donation', 'entertain', 'escort', 'exotic', 'flower', 'gamble', 'gambling', 'game', 'gaming', 'gift', 'hospital', 'hotline', 'jail', 'jewel', 'lawyer', 'liquor', 'luxury', 'membership', 'monitor', 'music', 'party', 'poker', 'recreation', 'recruit', 'reward', 'school', 'server', 'television', 'university', 'vacation', 'visa', 'welfare', 'wine']
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

  all_text = re.sub(r'([^\s\w]|_)+', '', " ".join(final_text)).lower()

  for word in search_words:
    if word in all_text:
      found_words.append(word)
  if len(found_words) > 0:
    results_file.append([the_file, " ".join(found_words)])
  else:
    results_file.append([the_file, "Nothing was found"])
  print "File read:",round(time()-t0,3),"s"
  print "Total script time elapsed:",round((time()-start_time)/60,2),"m\n"
ocr_output = 'OCROutput' + str(time()) + '.csv'
with open(ocr_output, 'wb') as csv_file:
  wr = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  for i in results_file:
    wr.writerow(i)

match_string = '*_ocr*'
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, match_string):
      destination = './PDFs-Searched/' + file
      os.rename(file, destination)
      print file
      print destination

match_string = '*.pdf'
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, match_string):
      os.remove(file)
      print file

print "Script End:",round((time()-start_time)/60,2),"m"

if platform == "darwin":
  os.system('say "scanning is complete"')
else:
  import subprocess
  subprocess.call(['speech-dispatcher'])        #start speech dispatcher
  subprocess.call(['spd-say', '"your process has finished"'])