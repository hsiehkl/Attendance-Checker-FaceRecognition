# AttendanceChecker

This is a small service for checking attendance in Goolge sheet based on recognizing people showing in a given image or video.

The service was developed under the contex of the Enterprise Architectures for Big Data course from the M.Sc. in Business Intelligence & process Management offered by the Berlin School of Economics and Law. 3 students worked together to achieve these results, during the course of the summer semester 2020. Full detail about the project was shown in the [presentaiton](https://github.com/hsiehkl/Attendance-Checker-FaceRecognition/blob/master/UAttented.pdf). (Note: Some pages were modified or hidden due to data privacy.)

Package Requirements: ```face_recognition```, ```dlib```, ```gspread```

## Setup

For using the service, there are some preliminary setups needed to be finished.

#### I. Google API Authentication
(Reference: [gspread](https://gspread.readthedocs.io/en/latest/oauth2.html))

To access spreadsheets via Google Sheets API we need to authenticate and authorize the application.

##### step 1: Enable API Access
* Head to [Google Developers Console](https://console.developers.google.com/project) and create a new project (or select the one you already have).
* In the box labeled “Search for APIs and Services”, search for “Google Drive API” and enable it.
* In the box labeled “Search for APIs and Services”, search for “Google Sheets API” and enable it.

##### step 2: Create a Service Account
* Go to “APIs & Services > Credentials” and choose “Create credentials > Service account key”.
* Fill out service account details.
* Set up service account permissions by selecting the role as Project > Editor.
* Select "ADD KEY" and create a new key as JSON format. (A JSON file should be automatically downloaded.)

##### step 3: Set up environment
* Move JSON file to ```cred``` folder.
* Rename the JSON File to ```credentials.json```
* Open ```credentials.json```, find the value of client_email and copy it.
* Open your Google Sheets, click Share button and add this email into user group.

##### step 4: Link your google sheets
* Open ```google_sheets.json``` file in the repository.
* Specify diffrent google sheets' link and give each of them a key.
```
{
   "BIPM2019_bigdata":"https://docs.google.com/spreadsheets/***sharing",
   "BIPM2019_TWSM":"https://docs.google.com/spreadsheets/***sharing"
}
```

#### II. Place Training Photos

For training a model of the own use case, some photos are needed to be in place.

##### step 1: Gather photos
* Gather photos of the people in the attendance list. (The more the photos, the higher the accuracy.)
##### step 2: Structure photos
* Put your photos in the ```train_dir``` folder with the following structure.
```
     Structure:
        <train_dir>/
        ├── <BIPM2019_bigdata>/
        │   ├── <student1>/
        │       ├── <student1-1>.jpeg
        │       ├── <student1-2>.jpeg
        │   ├── <student2>/
        │       ├── <student2-1>.jpeg
        │       ├── <student2-2>.jpeg
        │       ...
        ├── <BIPM2019_TWSM>/
        │   ├── <student1>/
        │       ├── <student1-1>.jpeg
        │       ├── <student1-2>.jpeg
        │   ├── <student2>/
        │       ├── <student2-1>.jpeg
        │       ├── <student2-2>.jpeg
        │       ...
        └── ...
```

## Usage

Once you have gone through the setup steps, you are free to start the service now!

##### step 1: Provide a media
* Place am image or a video that you want to generate an attendance in the ```raw_data``` folder.

##### step 2: Run the command
```python run.py -TRAIN_FOLDER_PATH -MEDIA -GOOGLE_SHEET -DATE```
```
TRAIN_FOLDER_PATH :
    The folder of the training dataset in train_dir
MEDIA :
    The media(an image or a video) for attendance checking in the raw_data folder
GOOGLE_SHEET :
    A key specified in the google_sheets.json file which will help us to find the corresponding path of a Google sheet.
    This key will be also used for naming the prediction model.
DATE :
    The date of attantence
```
example:
```python run.py BIPM2019-bigdata course1.mp4 BIPM2019_bigdata 7/27```

## Note
* We do not train a new model every time if we detect that there is already an existing model. We name the pretrained model with the key in ```google_sheets.json```. If you want to retrain a new model, please delete the old one.
