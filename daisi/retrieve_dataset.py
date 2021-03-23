import requests
import numpy as np
import json
import os
import contextlib
from distutils.dir_util import copy_tree

def getImages(POST_directory):
    fixer = 'https://www.thumbroll'

    os.chdir(POST_directory)
    # get all the generated subfolders from saving the Fiddler jsons
    for directory in (next(os.walk('.'))[1]):

        print("%%%%%%%%%%%Working on directory: "+ directory)
        current_directory = os.path.join(POST_directory,directory)

        with open(os.path.join(current_directory,'images.json')) as json_file:

            data = json.load(json_file)

            # iterate through the procedures
            for procedure_index in range(0,len(data['results'])):
                print("Working on procedure: "+ data['results'][procedure_index]['projectName'])

                # save the name of the procedure to a text file
                file1 = open(os.path.join(current_directory,'projectNames.txt'),'a+')
                file1.write(data['results'][procedure_index]['projectName']+'\n')
                file1.close()

                # create a directory for each procedure
                fp = os.path.join(current_directory,str(procedure_index+1).zfill(3))
                if not os.path.exists(fp):
                    os.mkdir(fp)

                #get the image urls
                images = data['results'][procedure_index]['tempImages']

                for image_index in range(len(images)):
                    final_file_path = os.path.join(fp,str(image_index+1).zfill(3)+'.jpg')

                    with open(final_file_path,'wb') as handle:
                        url = images[image_index]['url']
                        new_url = url
                        if(len(url) > 153):
                            new_url = fixer+url[57:]

                        print(new_url)
                        response = requests.get(new_url, stream=True)

                        if not response.ok:
			                print(response)

                        for block in response.iter_content(1024):
			                if not block:
			                    break

			                handle.write(block)

def getTextDescriptions(POST_directory):

    os.chdir(POST_directory)
    # get all the generated subfolders from saving the Fiddler jsons
    for directory in (next(os.walk('.'))[1]):

        print("%%%%%%%%%%%Working on directory: "+ directory)
        current_directory = os.path.join(POST_directory,directory)

        caption_file_paths = []
        for count, filename in enumerate(sorted(os.listdir(current_directory)), start=1):
            if filename.endswith(".json") and filename[0] != 'i':
                caption_file_paths.append(os.path.join(current_directory,filename))

        for procedure_index in range(0,len(caption_file_paths)):
            folder_path = os.path.join(current_directory,str(procedure_index+1).zfill(3))

            with open(caption_file_paths[procedure_index]) as json_file:
                textDescriptions = json.load(json_file)

                for description_index in range(len(textDescriptions['results'])):
					text_path = os.path.join(folder_path,str(description_index+1).zfill(3)+'.txt')
					text_file = open(text_path,"w")
					text_file.write(textDescriptions['results'][description_index]['description'])
					text_file.close()

def createFinalDataset(POST_directory, DAISIDirectory):

    os.chdir(POST_directory)

    if(not os.path.exists(DAISIDirectory)):
        os.mkdir(DAISIDirectory)

    procedures = []
    folder_count = 1

    # get all the generated subfolders from saving the Fiddler jsons
    for directory in (next(os.walk('.'))[1]):
        print("%%%%%%%%%%%Working on directory: "+ directory)
        current_directory = os.path.join(POST_directory,directory)

        text_file = open(os.path.join(current_directory,'projectNames.txt'),"r")
        specialty_counter = 1
        for line in text_file.readlines():
            print(line[:-1])
            add = True
            for name_index in range(len(procedures)):
				if procedures[name_index] == line[:-1]:
					add = False
					print("repeated")
					break
            if add is True:
				procedures.append(line[:-1])
				originalDirectory = os.path.join(current_directory,str(specialty_counter).zfill(3))
				targetDirectrory = os.path.join(DAISIDirectory,str(folder_count).zfill(3))
				if not os.path.exists(targetDirectrory):
				    os.mkdir(targetDirectrory)
				copy_tree(originalDirectory,targetDirectrory)
				folder_count += 1
            specialty_counter += 1
        text_file.close()

def main():
    POST_directory = os.path.join(os.getcwd(),'Log_of_POSTs')
    DAISIDirectory = os.path.join(os.getcwd(),'DAISI')

    getImages(POST_directory)
    getTextDescriptions(POST_directory)
    createFinalDataset(POST_directory,DAISIDirectory)

if __name__ == '__main__':
    main()
