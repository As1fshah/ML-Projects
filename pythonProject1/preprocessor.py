import pandas as pd
import re

def preprocessing(data):
    message_pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s[a-z][a-z]\s-'

    messages = re.split(message_pattern, data)[1:]
    date_pattern = "\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}"

    text_date = re.findall(date_pattern, data)

    df = pd.DataFrame({
        'Date': text_date,
        'Text': messages
    })

    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y, %H:%M')

    name_pattern = '^(.*?):\s*(.*?)$'

    user = []
    messages = []

    for message in df['Text']:
        finder = re.match(name_pattern, message)
        if finder:
            username = finder.group(1)
            message = finder.group(2)
            user.append(username)
            messages.append(message)

        else:
            user.append('Group Notification')
            messages.append(message)

    df['Users'] = user
    df['Message'] = messages
    df.drop(columns=['Text'], inplace=True)

    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day
    # df.drop(columns=['Date'], inplace=True)
    df = df[['Date','Day', 'Month', 'Year', 'Users', 'Message']]
    return df


