import cv2, time
import face_recognition
from sklearn import svm
import pickle
import time
from collections import defaultdict


def predict(input_path, model_path):
    
    media_format = input_path.split('.')[1]

    attendance_list = []
    if media_format in ['png', 'jpg', 'jpeg']:
        attendance_list = predict_pic(input_path, model_path)
    elif media_format == 'mp4':
        attendance_list = predict_video(input_path, model_path)
    else:
        print("Please provide media in png, jpg, jpeg or mp4 format.")

    return attendance_list


def predict_video(input_path, model_path):

    model = pickle.load(open('models/' + model_path, 'rb'))
    raw_data_path = 'raw_data/' + input_path

    video_capture = cv2.VideoCapture(raw_data_path)
    process_this_frame = True
    name_dict = defaultdict(int)

    start = time.time()
    print('Start processing video.')
    while True:
        # Take every frame
        ret, frame = video_capture.read()

        # Bail out when the video file ends
        if not ret:
            break 

        # Process every frame only one time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            # Loop in every faces detected
            for face_encoding in face_encodings:
                name = 'Unknown'
                #use the classifier to predict the name
                name = model.predict([face_encoding])[0]
                name_dict[name] += 1

            # To be sure that we process every frame only one time
        process_this_frame = not process_this_frame

    final_name_list = []
    wrongly_recognized_list = []
    for name, count in name_dict.items():
        print (f"{name}:{count}")
        if count/max(name_dict.values()) >= 0.1:
            final_name_list.append(name)
        else:
            wrongly_recognized_list.append(name)
    print('surely attended students are {}'.format(','.join(final_name_list)))
    if len(wrongly_recognized_list) != 0:
        print('Ops,{} have very low appearance rate, maybe s/he is someone else'.format(','.join(set(wrongly_recognized_list))))
    print('running time is {}'.format(time.time()-start))

    return final_name_list


def predict_pic(input_path, model_path):

    model = pickle.load(open('models/' + model_path, 'rb'))
    raw_data_path = 'raw_data/' + input_path

    image = face_recognition.load_image_file(raw_data_path)
    face_encodings_image = face_recognition.face_encodings(image)
    start = time.time()
    # Initialize an array for the name of the detected users
    face_names_image = []
    # Loop in every faces detected
    for face_encoding in face_encodings_image:
        #use the classifier to predict the name
        name_image = model.predict([face_encoding])[0]
        face_names_image.append(name_image)

    duplicate = []
    for name in face_names_image:
        if (face_names_image.count(name) > 1) and (name not in duplicate):
            duplicate.append(name)
            print('Ops! Someone looks too similar to {} and was wrongly recognized'.format(name))
    print('{}% of faces are recognized duplicatedly'.format(100-(len(set(face_names_image))/len(face_names_image))*100))
    print('running time is {}'.format(time.time()-start))

    return list(set(face_names_image))