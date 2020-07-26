import gspread
import pandas as pd
import json

def read_gsheet(sheet_name):
    gc = gspread.service_account(filename="cred/credentials.json")
    # read json
    with open("google_sheets.json", 'r') as google_sheets:
        sheets = google_sheets.read()
    # parse url
    url = json.loads(sheets)[sheet_name]
    sh = gc.open_by_url(url)
    worksheet = sh.get_worksheet(0)
    return worksheet

def update(worksheet, name_list, date):

    list_of_lists = worksheet.get_all_values()
    headers = list_of_lists[0]
    df = pd.DataFrame(list_of_lists[1:], columns=headers)

    row = None
    column = None

    try:
        column = df.columns.get_loc(date) + 1
    except:
        column = df.shape[1] + 1
        worksheet.update_cell(1, column, date)

    for name in name_list:

        if name.lower() in df['Name'].str.lower().values:
            row = df[df['Name'].str.lower()==name.lower()].index[0] + 2
            worksheet.update_cell(row, column, 'O')
            print(name, 'attended the class.')
        else:
            print('We cannot find this person in the attendance list.')
            
def update_attendence(sheet_name, name_list, date):

    if name_list != []:
        worksheet = read_gsheet(sheet_name)
        update(worksheet, name_list, date)
        print('Finish updating attendence.')
    else:
        print('There is no any attendee.')

# update_attendence('BIPM2019_bigdata', ['hsin-Ting', 'theresia', 'yuxin'], '7/23')