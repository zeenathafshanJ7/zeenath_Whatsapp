import matplotlib.pyplot as plt
import nltk
import seaborn as sns
import streamlit as st
import helper
import preprocessor

st.sidebar.title("Whatsapp Chat Analyzer")

nltk.download('vader_lexicon')

uploaded_file = st.sidebar.file_uploader("Choose a file")

st.markdown("<h1 style='text-align: center; color: grey;'>Whatsapp Chat Analyzer</h1>",
            unsafe_allow_html=True)

if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    d = bytes_data.decode("utf-8")

    data = preprocessor.preprocess(d)



    from nltk.sentiment.vader import SentimentIntensityAnalyzer
 
    sentiments = SentimentIntensityAnalyzer()

    data["po"] = [sentiments.polarity_scores(i)["pos"] for i in data["message"]]  # Positive
    data["ne"] = [sentiments.polarity_scores(i)["neg"] for i in data["message"]]  # Negative
    data["nu"] = [sentiments.polarity_scores(i)["neu"] for i in data["message"]]  # Neutral


    def sentiment(d):
        if d["po"] >= d["ne"] and d["po"] >= d["nu"]:
            return 1
        if d["ne"] >= d["po"] and d["ne"] >= d["nu"]:
            return -1
        if d["nu"] >= d["po"] and d["nu"] >= d["ne"]:
            return 0


    data['value'] = data.apply(lambda row: sentiment(row), axis=1)


    user_list = data['user'].unique().tolist()

    user_list.sort()

    user_list.insert(0, "Overall")


    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        
        
        # active map        
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        active_month_df, month_list, month_msg_list, active_day_df, day_list, day_msg_list = helper.activity_map(
            selected_user, data)  # Using 'data' instead of 'df'
        with col1:
            # active month
            st.header('Most Active Month')
            fig, ax = plt.subplots()
            ax.bar(active_month_df['month'], active_month_df['message'])
            ax.bar(month_list[month_msg_list.index(max(month_msg_list))], max(month_msg_list), color='green',
                   label='Highest')
            ax.bar(month_list[month_msg_list.index(min(month_msg_list))], min(month_msg_list), color='red',
                   label='Lowest')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2:
            # active day
            st.header('Most Active Day')
            fig, ax = plt.subplots()
            ax.bar(active_day_df['day'], active_day_df['message'])
            ax.bar(day_list[day_msg_list.index(max(day_msg_list))], max(day_msg_list), color='green', label='Highest')
            ax.bar(day_list[day_msg_list.index(min(day_msg_list))], min(day_msg_list), color='red', label='Lowest')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        # monthly timeline summary

        col1, col2, col3 = st.columns(3)
        with col2:
            st.markdown("<h1 style='text-align: center; color: black;'>Monthly Timeline</h1>",
                        unsafe_allow_html=True)
            timeline = helper.monthly_timelines(selected_user, data)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Monthly activity map
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<h3 style='text-align: center; color: black;'>Monthly Activity map(Positive)</h3>",
                        unsafe_allow_html=True)

            busy_month = helper.month_activity_map(selected_user, data, 1)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.markdown("<h3 style='text-align: center; color: black;'>Monthly Activity map(Neutral)</h3>",
                        unsafe_allow_html=True)

            busy_month = helper.month_activity_map(selected_user, data, 0)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='grey')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col3:
            st.markdown("<h3 style='text-align: center; color: black;'>Monthly Activity map(Negative)</h3>",
                        unsafe_allow_html=True)

            busy_month = helper.month_activity_map(selected_user, data, -1)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Monthly timeline
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<h3 style='text-align: center; color: black;'>Monthly Timeline(Positive)</h3>",
                        unsafe_allow_html=True)

            timeline = helper.monthly_timeline(selected_user, data, 1)

            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.markdown("<h3 style='text-align: center; color: black;'>Monthly Timeline(Neutral)</h3>",
                        unsafe_allow_html=True)

            timeline = helper.monthly_timeline(selected_user, data, 0)

            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='grey')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col3:
             st.markdown("<h3 style='text-align: center; color: black;'>Monthly Timeline(Negative)</h3>",
                         unsafe_allow_html=True)
             timeline = helper.monthly_timeline(selected_user, data, -1)

             fig, ax = plt.subplots()
             ax.plot(timeline['time'], timeline['message'], color='red')
             plt.xticks(rotation='vertical')
             st.pyplot(fig)

        # daily timeline summary
        col1, col2, col3 = st.columns(3)
        with col2:
            st.markdown("<h1 style='text-align: center; color: black;'>Daily Timeline</h1>",
                        unsafe_allow_html=True)
            daily_timelines = helper.daily_timelines(selected_user, data)
            fig, ax = plt.subplots()
            ax.plot(daily_timelines['only_date'], daily_timelines['message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Daily activity map
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<h3 style='text-align: center; color: black;'>Daily Activity map(Positive)</h3>",
                        unsafe_allow_html=True)

            busy_day = helper.week_activity_map(selected_user, data, 1)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.markdown("<h3 style='text-align: center; color: black;'>Daily Activity map(Neutral)</h3>",
                        unsafe_allow_html=True)

            busy_day = helper.week_activity_map(selected_user, data, 0)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='grey')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col3:
            st.markdown("<h3 style='text-align: center; color: black;'>Daily Activity map(Negative)</h3>",
                        unsafe_allow_html=True)

            busy_day = helper.week_activity_map(selected_user, data, -1)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Daily timeline
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<h3 style='text-align: center; color: black;'>Daily Timeline(Positive)</h3>",
                        unsafe_allow_html=True)

            daily_timeline = helper.daily_timeline(selected_user, data, 1)

            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.markdown("<h3 style='text-align: center; color: black;'>Daily Timeline(Neutral)</h3>",
                        unsafe_allow_html=True)

            daily_timeline = helper.daily_timeline(selected_user, data, 0)

            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='grey')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col3:
            st.markdown("<h3 style='text-align: center; color: black;'>Daily Timeline(Negative)</h3>",
                        unsafe_allow_html=True)

            daily_timeline = helper.daily_timeline(selected_user, data, -1)

            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Most Active User
        if selected_user == 'Overall':
            st.title('Most Active Users')
            x, new_df = helper.most_busy_users(data)  # Using 'data' instead of 'df'
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            

       
        # WordCloud
        col1, col2, col3 = st.columns(3)
        with col2:
            st.title("Wordcloud")
            df_wc = helper.create_wordclouds(selected_user, data)  # Using 'data' instead of 'df'
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

        # WORDCLOUD......
        col1, col2, col3 = st.columns(3)
        with col1:
            try:
                # heading
                st.markdown("<h3 style='text-align: center; color: black;'>Positive WordCloud</h3>",
                            unsafe_allow_html=True)

                # Creating wordcloud of positive words
                df_wc = helper.create_wordcloud(selected_user, data, 1)
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)
            except Exception as e:
                # Log the exception or print it for debugging
                print("An error occurred:", e)
                # Display a placeholder image or error message
                st.image('error.webp')

        with col2:
            try:
                # heading
                st.markdown("<h3 style='text-align: center; color: black;'>Neutral WordCloud</h3>",
                            unsafe_allow_html=True)

                # Creating wordcloud of neutral words
                df_wc = helper.create_wordcloud(selected_user, data, 0)
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)
            except Exception as e:
                # Log the exception or print it for debugging
                print("An error occurred:", e)
                # Display a placeholder image or error message
                st.image('error.webp')

        with col3:
            try:
                # heading
                st.markdown("<h3 style='text-align: center; color: black;'>Negative WordCloud</h3>",
                            unsafe_allow_html=True)

                # Creating wordcloud of negative words
                df_wc = helper.create_wordcloud(selected_user, data, -1)
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)
            except Exception as e:
                # Log the exception or print it for debugging
                print("An error occurred:", e)
                # Display a placeholder image or error message
                st.image('error.webp')

        # most common words
        col1, col2, col3 = st.columns(3)
        with col2:
            most_common_df = helper.most_common_word(selected_user, data)

            fig, ax = plt.subplots()

            ax.barh(most_common_df[0], most_common_df[1])
            plt.xticks(rotation='vertical')

            st.title('Most common words')
            st.pyplot(fig)

        # Most common positive words
        col1, col2, col3 = st.columns(3)
        with col1:
            try:
                # Data frame of most common positive words.
                most_common_df = helper.most_common_words(selected_user, data, 1)

                # heading
                st.markdown("<h3 style='text-align: center; color: black;'>Positive Words</h3>", unsafe_allow_html=True)
                fig, ax = plt.subplots()
                ax.barh(most_common_df[0], most_common_df[1], color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            except Exception as e:
                # Log the exception or print it for debugging
                print("An error occurred:", e)
                # Display a placeholder image or error message
                st.image('error.webp')

        with col2:
            try:
                # Data frame of most common neutral words.
                most_common_df = helper.most_common_words(selected_user, data, 0)

                # heading
                st.markdown("<h3 style='text-align: center; color: black;'>Neutral Words</h3>", unsafe_allow_html=True)
                fig, ax = plt.subplots()
                ax.barh(most_common_df[0], most_common_df[1], color='grey')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            except Exception as e:
                # Log the exception or print it for debugging
                print("An error occurred:", e)
                # Display a placeholder image or error message
                st.image('error.webp')

        with col3:
            try:
                most_common_df = helper.most_common_words(selected_user, data, -1)

                # heading
                st.markdown("<h3 style='text-align: center; color: black;'>Negative Words</h3>", unsafe_allow_html=True)
                fig, ax = plt.subplots()
                ax.barh(most_common_df[0], most_common_df[1], color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            except Exception as e:
                # Log the exception or print it for debugging
                print("An error occurred:", e)
                # Display a placeholder image or error message
                st.image('error.webp')
