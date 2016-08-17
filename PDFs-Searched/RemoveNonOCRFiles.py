import os, fnmatch, csv, re

match_string = '*.pdf'
not_match = '*_ocr*'
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, match_string) and not(fnmatch.fnmatch(file, not_match)):
      os.remove(file)
