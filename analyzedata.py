import json
import re
from bs4 import BeautifulSoup
import pprint
import pickle
import collections
import sys
import operator
from Prepender import *

pp = pprint.PrettyPrinter(indent=4)


def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

f = open('courseDic.txt', 'rb')
courseDic = pickle.load(f)
f.close()


tmp=len(courseDic)
scoringLst={}
scoringLst['quality']=[]
scoringLst['workscore']=[]
keysToRemove=[]

tmpc=0

def ScoreQ(lst, index, key, course):
	try: 
		global scoringLst
		global tmpc
		tmpc+=1
		A_lst=['A'+str(i) for i in range(index,index+5)]
		ex_lst=[lst[k] for k in A_lst if k in lst]
		#print "scoring " + course
		n=0
		for val in ex_lst:
			n+=val
		if n>-5:		
			score = 0
			for i, val in enumerate(ex_lst):
				score += val * (len(ex_lst) - i - 1)
			score = float(score)/float(n)
		else:
			return False
		scoringLst[key].append([course, score])

		return score
	except ZeroDivisionError:
		print "Division by zero, omitting " + key + " for " + course
		return False


ppLst=[]
outDic={}
avgLst=[]

keysToSave=['avg', 'passpercent']
for course, categorydb in courseDic.iteritems():
	print course
	hasKeys=0
	if 'review' in categorydb:
			print 'Review found'
	if 'grades' in categorydb:
			print 'Grades found'
	for category, sheet in categorydb.iteritems():
		outDic[course]={}
		hasKeys=1

		
		if category=='review':
			quality = ScoreQ(sheet, 35, 'quality', course)
			workscore = ScoreQ(sheet, 25, 'workscore', course)
			#print 'quality: ' + str(quality)
			#print 'workscore: ' + str(workscore)
		if category=='grades':
			for key in keysToSave:
				if key in sheet:
					if key=="avg":
						avgLst.append([course, sheet[key]])
					outDic[course][key]=sheet[key]
			if 'passpercent' in sheet:

				ppLst.append([course, sheet['passpercent']])
				#ppDic[sheet['passpercent']] = course
			else: 
				print "no passpercent for " + course
	if hasKeys==0:
		print "Flagging " + course + " for removal"
		keysToRemove.append(course)

	print 
for k in keysToRemove: del courseDic[k]



def normalizeLst(lst, name, insert=True):
	new_list = list(lst)
	new_list.sort(key=lambda sublist: sublist[0], reverse=True)
	new_list.sort(key=lambda sublist: sublist[1])
	counter = 0
	normDic={}
	for i, val in enumerate(new_list): 
		perc = round( float(i)/float(len(new_list)-1) * 100, 1)
		if insert:
			outDic[val[0]][name] = perc
		normDic[val[0]]=perc
		#print course + ": " + str(perc)
	return normDic
	#print str(course) + ": " + avg
normalizeLst(scoringLst['quality'], 'qualityscore')
pp.pprint(scoringLst['workscore'])
normWork = normalizeLst(scoringLst['workscore'], 'workscore')

#Lazying
normPP=normalizeLst(ppLst, 'pp')
normalizeLst(avgLst, "avgp")

scoringLst['lazyscore']=[]
for course, ppPerc  in normPP.iteritems():
	try:
		lazyPerc=(float(ppPerc) + float(normWork[course]))/float(2)
		scoringLst['lazyscore'].append([course, lazyPerc])
	except: 
		print "Warning: No avg for " + str(course) + " maybe no avg and/or work found for course"
pp.pprint(scoringLst['lazyscore'])
normLazy = normalizeLst(scoringLst['lazyscore'], 'lazyscore')

#pp.pprint(outDic)
f = open('courseDicAnalyzed.txt', 'wb')
pickle.dump(courseDic, f)
f.close()

extFilename='extension/db/data.js'
with open(extFilename, 'w') as outfile:
    json.dump(outDic, outfile)

with PrependToFile(extFilename) as f:
	f.write_line('var data = ')


pp.pprint(outDic)

#pp.pprint(scoringLst['quality'])


new_list = list(scoringLst['quality'])
new_list.sort(key=lambda sublist: sublist[0], reverse=True)
new_list.sort(key=lambda sublist: sublist[1])
pp.pprint(new_list)