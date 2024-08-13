import streamlit as st
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

extract = URLExtract()


# -1 => Negative
# 0 => Neutral
# 1 => Positive

def fetch_stats(selected_user, data):

    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]
        
    num_messages = data.shape[0]
 
    words = []
    for message in data['message']:
        words.extend(message.split())

    num_media_messages = data[data['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in data['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def activity_map(selected_user, data):
    if selected_user != 'Overall':  # Corrected typo 'OverAll' to 'Overall'
        data = data[data['user'] == selected_user]

    active_month_df = data.groupby('month')['message'].count().reset_index()
    month_list = active_month_df['month'].tolist()
    month_msg_list = active_month_df['message'].tolist()

    active_day_df = data.groupby('day')['message'].count().reset_index()
    day_list = active_day_df['day'].tolist()
    day_msg_list = active_day_df['message'].tolist()

    return active_month_df, month_list, month_msg_list, active_day_df, day_list, day_msg_list

def monthly_timelines(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    timeline = data.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def week_activity_map(selected_user, df, k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value'] == k]
    return df['day_name'].value_counts()


def month_activity_map(selected_user, df, k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value'] == k]
    return df['month'].value_counts()

def daily_timelines(selected_user, data):

    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    daily_timelines = data.groupby('only_date').count()['message'].reset_index()

    return daily_timelines


def activity_heatmap(selected_user, df, k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value'] == k]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap


def daily_timeline(selected_user, df, k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value'] == k]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def most_busy_users(data):
    x = data['user'].value_counts().head()
    df = round((data['user'].value_counts() / data.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df


def monthly_timeline(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value']==-k]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def percentage(df,k):
    df = round((df['user'][df['value']==k].value_counts() / df[df['value']==k].shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return df

def create_wordclouds(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def create_wordcloud(selected_user, df, k):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')

    temp['message'] = temp['message'].apply(remove_stop_words)
    temp['message'] = temp['message'][temp['value'] == k]

    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc
def most_common_word(selected_user, data):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    temp = data[data['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df



def most_common_words(selected_user, df, k):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
    for message in temp['message'][temp['value'] == k]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df= pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
