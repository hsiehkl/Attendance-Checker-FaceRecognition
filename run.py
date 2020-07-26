from api_connector import update_attendence
from train import train
from predict import predict_video
import os


def main(train_path, media, sheet, date):

    models = [f for f in os.listdir('models') if not f.startswith('.')]
    if sheet+'.pkl' not in models:
        print('start training model for {}.'.format(sheet))
        train(train_path, sheet)
    else:
        print("{} model has already existed.".format(sheet))

    attendance_list  = predict(media_path, sheet+'.pkl')
    update_attendence(sheet, attendance_list, date)


if __name__ == "__main__":
    import plac; plac.call(main)
