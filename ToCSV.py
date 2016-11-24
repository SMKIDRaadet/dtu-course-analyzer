import re
from bs4 import BeautifulSoup
import pprint
import pickle

f = open('gradesDB.txt', 'rb')
gradesDB = pickle.load(f)
f.close()

import csv

myfile = open("gradesDB.csv", 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerow(gradesDB)



f = open('reviewsDB.txt', 'rb')
reviewsDB = pickle.load(f)
f.close()

myfile = open("reviewsDB.csv", 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerow(reviewsDB)