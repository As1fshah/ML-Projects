from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd

def fetch_stats(selected_user, df):

    # 1 This will return the number of message
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    num_messages = df.shape[0]

    # ----- Ends Here -------

    # 2 This will return the number of words


    words = []

    for word in df['Messages']:
        words.extend(word.split())

    # ----- Ends Here -------



    # 3 This will return the number of words

    links = []
    iam_link_finder = URLExtract()

    for link in df['Messages']:
        urls = iam_link_finder.find_urls(link)

        links.extend(urls)

    # ----- Ends Here -------

    #4 This will return the number of shared media

    num_media = df[df['Messages'] == '<Media omitted>\n'].shape[0]
    return num_messages, len(words), len(links), num_media


def user_analysis(df):

    # 1 This will return the top 10 active user in chat
    x = df['User'].value_counts().head(10)

    # ------ Ends Here --------


    # 2 This will return the top 10 active user in chat

    y = round((df['User'].value_counts() / df.shape[0]) * 100, 2).head(10).reset_index().rename(
        columns={'User': 'Name', 'count': 'Percentages'})

    # ------ Ends here ------
    return x, y

# User analysis function ends here --------------------


def word_cloud_gen(selected_user, df):
    if selected_user!= 'Overall':
        df = df[df['User']==selected_user]

    new_df_1 = df[df['Messages'] != '<Media omitted>\n']
    new_df_1 = new_df_1[new_df_1['Messages'] != 'This message was deleted\n']
    new_df_1 = new_df_1[new_df_1['User'] != 'Group Notification']


    words = []

    for word in new_df_1['Messages']:
        word = word.lower()
        word = word.split()
        words.extend(word)



    wc = WordCloud(width= 500, height=500, min_font_size= 10, background_color='white')
    df_wc = wc.generate(' '.join(words))

    return df_wc

def most_used_words(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    new_df_1 = df[df['Messages'] != '<Media omitted>\n']
    new_df_1 = new_df_1[new_df_1['Messages'] != 'This message was deleted\n']
    new_df_1 = new_df_1[new_df_1['User'] != 'Group Notification']

    words_1 = []
    for word in new_df_1['Messages']:
        word = word.lower()
        word = word.split()
        words_1.extend(word)

    from collections import Counter
    most_used_words_df = pd.DataFrame(Counter(words_1).most_common(10)).rename(columns={0: 'Words', 1: 'Count'})



    return most_used_words_df

def timeline_analysis(selected_user, df):
    if selected_user!= 'Overall':
        df = df[df['User']==selected_user]
    
    timeline_df = df.groupby(['Year', 'Month Name', 'Month']).count()['Messages'].reset_index()
    new_date = []

    for i in range(timeline_df.shape[0]):
        new_date.append(timeline_df['Month Name'][i] + '-' + str(timeline_df['Year'][i]))

    timeline_df['New Date'] = new_date

    return timeline_df

def daily_timeline(selected_user, df):
    if selected_user!= 'Overall':
        df = df[df['User']==selected_user]
    
    df['Date'] = df['Extracted Date'].dt.date
    daily_timeline_df = df.groupby('Date').count()['Messages'].reset_index()
    

    return daily_timeline_df


def busy_day(selected_user, df):
    if selected_user!= 'Overall':
        df = df[df['User']==selected_user]
    
    df['Day Name'] = df['Extracted Date'].dt.day_name() 
    busy_day_df = df['Day Name'].value_counts()

    return busy_day_df


def busy_month(selected_user, df):
    if selected_user!= 'Overall':
        df = df[df['User']==selected_user]
    
    busy_month_df = df['Month Name'].value_counts()

    return busy_month_df


def hour_map(selected_user, df):
    if selected_user!= 'Overall':
        df = df[df['User']==selected_user]
    
    period = []

    for hour in df[['Month Name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        
        elif hour == 00:
            period.append(str(hour) + '-' + str(hour+1))
        
        else:
            period.append(str(hour) + '-' + str(hour+1))
    
    df['Period'] = period

    return df

