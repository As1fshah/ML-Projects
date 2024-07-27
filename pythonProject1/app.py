import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import seaborn as sns


st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocessing(data)

    # st.dataframe(df)


    user_list = df['Users'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox('Show analysis of', user_list)

    if st.sidebar.button('Show Analysis'):

        num_messages, words, shared_media, links = helper.fetch_status(selected_user, df)

        col_1, col_2, col_3, col_4 = st.columns(4)

        with col_1:
            st.header('Total Messages',)
            st.title(num_messages)
        with col_2:
            st.header('Total Words', )
            st.title(words)

        with col_3:
            st.header('Shared Media', )
            st.title(shared_media)

        with col_4:
            st.header('Link Shared')
            st.title(links)

        if selected_user == 'Overall':
            st.title('Most Active User')
            x, new_df = helper.most_active_user(df)
            fig, ax = plt.subplots()

            col_5, col_6 = st.columns(2)

            with col_5:
                ax.bar(x.index, x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col_6:
                st.dataframe(new_df)

        # WordCloud

        st.title('Words')
        df_wc = helper.word_cloud_gen(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # Words Graph

        st.title('Words Graph')
        most_common_df = helper.most_used_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df['Words / Emojis'], most_common_df['No of Times'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)



        timeline = helper.timeline_analysis(selected_user, df)
        st.title('Monthly Stats x Messages')

        fig, ax = plt.subplots()
        ax.plot(timeline['Time'], timeline['Message'])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # Daily Stats analysis
        st.title('Daily Stats x Messages')

        daily_stats = helper.daily_stats(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(daily_stats['Date_F'], daily_stats['Message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Stats analysis
        st.title('Most Active Day x Messages')

        activity_stats = helper.activity_stats(selected_user, df)

        fig, ax = plt.subplots()
        ax.bar(activity_stats['Date'], activity_stats['count'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Busy Month

        st.title('Most Active Month x Messages')

        busy_month_df = helper.busy_month(selected_user, df)

        fig, ax = plt.subplots()
        ax.bar(busy_month_df['Month'], busy_month_df['count'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

