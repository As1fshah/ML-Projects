import pandas as pd
import re

def preprocessing(data):

    date_pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s(?:am|pm)'
    extracted_date = re.findall(date_pattern, data)

    # This is pattern of the date : 23/05/24, 2:17 am - User_Name: User_message, we have created regular expression string for this and split function is being used here

    message_finder = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s(?:am|pm)\s-\s'
    extracted_message = re.split(message_finder, data)[1:]

    # Now we have convert the extracted information in to the dataframe

    df = pd.DataFrame({'Extracted Date': extracted_date, 'Extracted Message': extracted_message})

    df['Extracted Date'] = pd.to_datetime(df['Extracted Date'], format='%d/%m/%y, %H:%M\u202f%p')

    user_name_pattern = '([\w\W]+?):\s'
    # user_name_pattern_2 = '(.*?):\s*(.*)$'
    users_1 = []
    messages_1 = []

    for name in df['Extracted Message']:
        finder = re.split(user_name_pattern, name)

        if finder[1:]:
            users_1.append(finder[1])
            messages_1.append(finder[2])

        else:
            users_1.append('Group Notification')
            messages_1.append(name)

    df['User'] = users_1
    df['Messages'] = messages_1

    df.drop(columns=['Extracted Message'], inplace=True)

    df['Year'] = df['Extracted Date'].dt.year

    df['Month Name'] = df['Extracted Date'].dt.month_name()

    df['Month'] = df['Extracted Date'].dt.month

    df['Day'] = df['Extracted Date'].dt.day

    df['Hour'] = df['Extracted Date'].dt.hour

    df['Minute'] = df['Extracted Date'].dt.minute


    return df