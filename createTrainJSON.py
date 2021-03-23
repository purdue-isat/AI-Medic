import os
import numpy as np
import json
from PIL import Image

def createJSONDataset():
	dictionary = []

	ImagesPath = os.path.join(os.getcwd(),'images')
	CaptionsPath = os.path.join(os.getcwd(),'captions')

	file_count = len(next(os.walk(ImagesPath))[2])
	for file_index in range(0,file_count):
		dict_entry = {}
		captions = []
		img_path = os.path.join(ImagesPath,str(file_index+1).zfill(5)+'.jpg')
		txt_path = os.path.join(CaptionsPath,str(file_index+1).zfill(5)+'.txt')
		text_file = open(txt_path,"r")		
		captions.append(text_file.read())
		dict_entry["file_path"] = img_path
		dict_entry["captions"] = captions
		dictionary.append(dict_entry)
		text_file.close()
		#print("finished folder " + str(folder_index+1))
	with open('data.json', 'w') as f:
	    json.dump(dictionary, f)

print("")
print("--Saving database into a JSON file--")
createJSONDataset()
print("")
print("--Finished saving into JSON--")
#createJSONDataset(0)