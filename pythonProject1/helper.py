from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import seaborn as sns

url_finder = URLExtract()
def fetch_status(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for word in df['Message']:
        words.extend(word.split())

    shared_media = df[df['Message'] == '<Media omitted>'].shape[0]

    links = []

    for link in df['Message']:
        links.extend(url_finder.find_urls(link))

    return num_messages, len(words), shared_media, len(links)


def most_active_user(df):
    x = round((df['Users'].value_counts().head(10) / df.shape[0]) * 100, 2)

    new_df = round((df['Users'].value_counts().head(10) / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'Users': 'Name', 'count': 'Percentage'})

    return x, new_df
def word_cloud_gen(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    wc = WordCloud(height=500, width=500, background_color= 'white', min_font_size=10)
    new_df_1 = df[df['Message']!='<Media omitted>']
    new_df_1 = new_df_1[new_df_1['Users'] != 'Group Notification']
    new_df_1 = new_df_1[new_df_1['Message']!='This message was deleted']


    df_wc = wc.generate(new_df_1['Message'].str.cat(sep = ' '))

    return df_wc


def most_used_words(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    new_df_1 = df[df['Message']!='<Media omitted>']
    new_df_1 = new_df_1[new_df_1['Users'] != 'Group Notification']
    new_df_1 = new_df_1[new_df_1['Message']!='This message was deleted']

    words1 = []
    for text in new_df_1['Message']:
        for word in text.lower().split():
            words1.append(word)

            # if word not in hinglish_stopwords:
            #     words1.append(word)

    from collections import Counter

    most_common_df = pd.DataFrame(Counter(words1).most_common(30)).rename(columns={0: 'Words / Emojis', 1: 'No of Times'})

    return most_common_df


# Monthly Timeline Stats
def timeline_analysis(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    df['Month No'] = df['Date'].dt.month
    timeline = df.groupby(['Year', 'Month', 'Month No']).count()['Message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + '-' + str(timeline['Year'][i]))

    timeline['Time'] = time
    # plt.bar(timeline['Time'], timeline['Message'])
    # plt.xticks(rotation='vertical')
    # plt.show()

    return timeline

# Daily Timeline Stats
def daily_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    df['Date_F'] = df['Date'].dt.date
    daily_stats = df.groupby(['Date_F']).count()['Message'].reset_index()

    return daily_stats

# Activity Timeline Stats
def activity_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    activity_df = df['Date'].dt.day_name().value_counts().reset_index()

    return activity_df

# Busy Month
def busy_month(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    busy_month_df = df['Month'].value_counts().reset_index()

    return busy_month_df



