import streamlit as st
import pandas as pd
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title('WhatsApp Chat Analysis')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocessing(data)
    # st.dataframe(df)


    user_list= df['User'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0,'Overall')


    selected_user = st.sidebar.selectbox('Show Analysis Of ',user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, links, num_media = helper.fetch_stats(selected_user, df)


        col_1, col_2 = st.columns(2)

        with col_1:
            st.header('Total Messages')
            st.title(num_messages)

        with col_2:
            st.header('Total Words')
            st.title(words)

        col_3, col_4 = st.columns(2)

        with col_3:
            st.header("Shared Links")
            st.title(links)

        with col_4:
            st.header('Shared Media')
            st.title(num_media)

        x, y = helper.user_analysis(df)

        col_5, col_6 = st.columns(2)

        # with col_5:
        st.header('Most Active Person')

        fig, ax = plt.subplots()
        sns.barplot(x = x.index, y = x.values, palette='viridis')
        plt.xticks(rotation = 'vertical')

        st.pyplot(fig)


        # This will generate the dataframe of most active user list with percentage
        # with col_6:
        st.header('Message Contribution')
        st.dataframe(y)

        # ------- Ends here --------------------


        # col_7, col_8 = st.columns(2)

        # with col_7:
        most_used_words_df = helper.most_used_words(selected_user, df)
        st.header('Most Used Words')
        fig, ax = plt.subplots()
        sns.barplot(data =  most_used_words_df,
                        x='Count',
                        y='Words',
                        palette='magma')
        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        # with col_8:

        st.header('Word Cloud')
        df_wc = helper.word_cloud_gen(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        plt.axis('off')
        st.pyplot(fig)

        st.header('Timeline Analysis')
        timeline_df = helper.timeline_analysis(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(timeline_df['New Date'],timeline_df['Messages'])
        plt.xlabel('Date')
        plt.ylabel('Number of Messages')
        plt.xticks(rotation = 'vertical')
        # plt.axis('off')
        st.pyplot(fig)


        st.header('Daily Analysis')
        daily_analysis_df = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(daily_analysis_df['Date'],daily_analysis_df['Messages'])
        plt.xlabel('Date')
        plt.ylabel('Number of Messages')
        plt.xticks(rotation = 'vertical')
        # plt.axis('off')
        st.pyplot(fig)


        st.header('Busiest Day')
        busy_day_df = helper.busy_day(selected_user, df)
        fig, ax = plt.subplots()
        sns.barplot(x = busy_day_df.index, 
                    y = busy_day_df.values, 
                    palette='magma')
        plt.xlabel('Day')
        plt.ylabel('Number of Messages')
        plt.xticks(rotation = 'vertical')
        # plt.axis('off')
        st.pyplot(fig)

        st.header('Busiest Month')
        busy_month_df = helper.busy_month(selected_user, df)
        fig, ax = plt.subplots()
        sns.barplot(x = busy_month_df.index, 
                    y = busy_month_df.values, 
                    palette='deep')
        plt.xlabel('Month')
        plt.ylabel('Number of Messages')
        plt.xticks(rotation = 'vertical')
        # plt.axis('off')
        st.pyplot(fig)


        st.header('Activity Map')
        hour_map_df = helper.hour_map(selected_user, df)
        # fig, ax = plt.subplots()
        # plt.figure(figsize = (20,6))
        sns.heatmap(hour_map_df.pivot_table(index ='Day Name', columns = 'Period', values = 'Messages', aggfunc= 'count').fillna(0))
        # plt.axis('off')
        st.pyplot(fig)





