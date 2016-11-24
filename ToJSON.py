import json
import re
from bs4 import BeautifulSoup
import pprint
import pickle

f = open('gradesDB.txt', 'rb')
gradesDB = pickle.load(f)
f.close()
f = open('reviewsDB.txt', 'rb')
reviewsDB = pickle.load(f)
f.close()

fields=["participants", "absent", "sick", "p", "np", "-3", "00", "02", "4", "7", "10", "12"]
gdict={};
rdict={}
#print reviewsDB[278]
for i, lst in enumerate(gradesDB):
	gdict[lst[0]] = {}
	
	for j, val in enumerate(lst[1:len(lst)  ]):
		gdict[lst[0]][fields[j]] = val

for i, lst in enumerate(reviewsDB):
	rdict[lst[0]] = {}
	
	rdict[lst[0]][fields[0]] = lst[1]
	for j, val in enumerate(lst[2:len(lst)  ]):
		#print j
		#print 'rdict['+lst[0]+'][Q'+str(j)+']'+' = ' + str(val)
		rdict[lst[0]]['Q'+str(j)] = val
	#print

#print(json.dumps(rdict, indent=4))

with open('extension/gradesDB.json', 'w') as outfile:
    json.dump(gdict, outfile)

with open('extension/reviewsDB.json', 'w') as outfile:
    json.dump(rdict, outfile)
# with open('reviewsDB.json', 'w') as outfile:
#     json.dump(reviewsDB, outfile)

