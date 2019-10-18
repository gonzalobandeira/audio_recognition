# Audio Recognition 

The following program is able to detect several audios and classify them in real-time. 

The program is made out of three stages:
 1. Recording stage: there is a built-in recorder that lets you easily record the sounds you want to include in the program. 
 2. Dataset creation and model testing: with the sound dataset created in the previous step, this stage is in charge of creating a useful database and trainnig ML and Deep Learning models in order to afterwards classify correctly. 
 3. Live recording UI: a live recorder is used to show on screen the detected sound by using the previous trained models. 
 


## Usage
From the project folder: 
 * To run the recorder: 
         
         python recorder/recorder_gui.py
        
 * To create the dataset from recorded sounds: 
        
        python model_desgin/dataset_making.py
        
 * To train models or generate a production model: 
 
        python model_design/main_models.py
        
 * To run the live-gui: 
 
        python main_ui/main_ui_live.py
        
        
## Requirements

Install the requirement with the following command: 

        pip install -r requirements.txt




