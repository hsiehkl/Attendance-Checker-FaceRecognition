from api_connector import update_attendence
from train import train
from predict import predict
import os


def main(train_path, media, sheet, date):
    """Check attendance based on face recognition.

    Parameters
    ----------
    train_path : str
        The folder path of the training dataset in train_dir
    
    media : str
        The media(an image or a video) for checking attendance in the raw_data folder
        
    sheet : str
        A sheet name specified in the google_sheets.json file

    date : str
        The date of attantence
    """


    models = [f for f in os.listdir('models') if not f.startswith('.')]
    if sheet+'.pkl' not in models:
        print('start training model for {}.'.format(sheet))
        train(train_path, sheet)
    else:
        print("{} model has already existed.".format(sheet))

    attendance_list = predict(media, sheet+'.pkl')
    update_attendence(sheet, attendance_list, date)


if __name__ == "__main__":
    import plac; plac.call(main)

# Example:
# python3 run.py "BIPM2019-bigdata" "class(12).png" "BIPM2019_bigdata" "7/26"