import os
import shutil
import random

DAISI_path = os.path.join(os.getcwd(),'DAISI')
train_path = os.path.join(os.getcwd(),"Train")
test_path = os.path.join(os.getcwd(),"Test")
train_images_path = os.path.join(train_path,"images")
train_captions_path = os.path.join(train_path,"captions")
test_images_path = os.path.join(test_path,"images")
test_captions_path = os.path.join(test_path,"captions")
intra_test_sampling = 0.5 # Define the portion of the dataset that you want to use when using intra procedure
intra_procedure = True # Specify whether you want to

def copyAndRename(folder_path,image_file,new_file_name_counter,isTest):
    images_path = ""
    captions_path = ""
    if(isTest):
        images_path = test_images_path
        captions_path = test_captions_path
    else:
        images_path = train_images_path
        captions_path = train_captions_path

    image_original_file_path = os.path.join(folder_path,image_file)
    text_original_file_path = image_original_file_path[:-3]+'txt'
    shutil.copy(image_original_file_path,images_path)
    shutil.copy(text_original_file_path,captions_path)
    image_new_file_path = os.path.join(images_path,str(new_file_name_counter).zfill(5)+'.jpg')
    text_new_file_path = os.path.join(captions_path,str(new_file_name_counter).zfill(5)+'.txt')
    os.rename(os.path.join(images_path,image_file), image_new_file_path)
    os.rename(os.path.join(captions_path,image_file[:-3]+'txt'), text_new_file_path)

def main():
    os.chdir(DAISI_path)
    test_sampling = 1.0

    if(intra_procedure):
        test_sampling = intra_test_sampling
    very_n_images = int(1.0/test_sampling)

    if(not os.path.exists(train_path)):
        os.mkdir(train_path)
        os.mkdir(test_path)
        os.mkdir(train_images_path)
        os.mkdir(train_captions_path)
        os.mkdir(test_images_path)
        os.mkdir(test_captions_path)

    listing = os.listdir(DAISI_path)

    procedures_for_test = round(float(len(listing))/10.0,0) # Use ten percent of the total procedures as testing

    test_list = random.sample(listing, int(procedures_for_test))

    train_list = []

    for element in listing:
        if element not in test_list:
            train_list.append(element)

    new_test_file_name = 1
    new_train_file_name = 1

    for folder in test_list:
        folder_path = os.path.join(DAISI_path,folder)
        folder_listing = os.listdir(folder_path)

        text_files = []
        image_file = []

        for element in folder_listing:
            if element.endswith('.txt'):
                text_files.append(element)
            else:
                image_file.append(element)

        for element_index in range(0,len(image_file)):
            if(element_index%very_n_images == 0):
                copyAndRename(folder_path,image_file[element_index],new_test_file_name,1)
                new_test_file_name += 1
            else:
                copyAndRename(folder_path,image_file[element_index],new_train_file_name,0)
                new_train_file_name += 1


    for folder in train_list:
        folder_path = os.path.join(DAISI_path,folder)
        folder_listing = os.listdir(folder_path)

        text_files = []
        image_file = []

        for element in folder_listing:
            if element.endswith('.txt'):
                text_files.append(element)
            else:
                image_file.append(element)

        for element_index in range(0,len(image_file)):
            copyAndRename(folder_path,image_file[element_index],new_train_file_name,0)
            new_train_file_name += 1

if __name__ == '__main__':
    main()
