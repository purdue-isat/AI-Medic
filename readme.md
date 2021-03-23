# AI-Medic


## Dataset
- You can either create the dataset following the steps [here](https://github.com/purdue-isat/AI-Medic/wiki/DAISI-DATASET), or you can download the dataset [here](https://drive.google.com/file/d/1K7DYFFLTpSk43YEOTOdGN8egcBe8qr6o/view?usp=sharing).
- Change the `captions` and `images` path in `createTrainJSON.py` and run:
 
        $ python createTrainJSON.py
    
- This will create `data.json`  that describes the training set.
- Run the following command to create two files `DAISI.json` and `DAISI.h5`

        $ python prepro.py --input_json "path_to_data.json" --num_val 1000 --num_test 1000 --images_root "path_to_images" --word_count_threshold 5 --output_json "output_path_DAISI.json" --output_h5 "output_path_DAISI.h5"

## Training
- Download the VGG16 pretrained weights from [here](https://drive.google.com/file/d/1kI9zM2aREgpF1ylRRazlSqhIjuIukxfS/view?usp=sharing) and plaxe them in `model` folder
- To train the model, run:

        $ th train.lua -input_h5 "path to DAISI.h5" -input_json "path to DAISI.json" -checkpoint_path "path to checkpoints" -id X
`id` is a reference number(int), in case you want to train multiple models.
