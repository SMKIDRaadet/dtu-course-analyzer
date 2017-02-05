import pickle
import json

# Open the large data file with all data. 
f = open("courseDic.txt", 'r')
courseDic = pickle.load(f)
f.close()

f = open("coursenumbers.txt", 'r')
courses = f.read().split(',')
f.close()

# Open the exisiting data.js and load it into a python object. 
data_file = open("extension/db/data.js", 'rw')
data_raw = data_file.read().replace("=", "").replace("var", "").replace("data", "")
data_js = json.loads(data_raw)
data_file.close()

characters = ["-3", "00", "02", "4", "7", "10", "12"]

# Now add the grades to the data file
for course in courses:
    if (data_js.has_key(course)):
        data_js[course]['grades'] = {}
        for character in characters:
            if courseDic[course].has_key('grades'):
                data_js[course]['grades'][character] = courseDic[course]['grades'][character]

# Make it a json object and write it to the javascript file
data_raw = json.dumps(data_js)
data_raw = "var data = " + data_raw
new_datafile = open("extension/db/data_new.js", 'w')
new_datafile.write(data_raw)
new_datafile.close()