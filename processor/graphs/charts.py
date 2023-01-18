"""
Analysis Chats are at one Place
"""
# Import support labaraies
import logging
from typing import Any
from collections import Counter
import numpy as np
import pandas as pd
import plotly.express as px
from textblob import TextBlob
import matplotlib.pyplot as plt


def message_cluster(data_frame: pd.DataFrame):
    """
    Display Message Cluster base on the message statistics

    Attributes
    ----------
    Dataframe (pandas DF)

    Retrurns
    --------
    Matplotlib Figure
    """
    new_df = pd.DataFrame(data_frame[['message']].groupby(
        by=data_frame['name']).count())
    new_df['media_count'] = data_frame[['media']].groupby(
        by=data_frame['name']).sum()
    new_df['emoji_count'] = data_frame[['emojis']].groupby(
        by=data_frame['name']).sum()
    new_df['urlcount_count'] = data_frame[['urlcount']].groupby(
        by=data_frame['name']).sum()
    new_df['letter_count'] = data_frame[['letter_count']].groupby(
        by=data_frame['name']).sum()
    new_df['words_count'] = data_frame[['word_count']].groupby(
        by=data_frame['name']).sum()
    new_df.reset_index(level=0, inplace=True)
    fig = px.scatter(
        new_df, x="message", y="words_count",
        size="letter_count", color="name",
        hover_name="emoji_count", log_x=True, size_max=60)
    return fig


def pie_display_emojis(data_frame: pd.DataFrame):
    """
    Pie chart formation for Emoji's Distrubution

    Attributes
    ----------
    Dataframe (pandas DF)

    Retrurns
    --------
    Plotly Figure (pyDash)
    """
    logging.info("WhatsApp/pie_display_emojis()")
    total_emojis_list = list(set([a for b in data_frame.emojis for a in b]))
    total_emojis_list = (a for b in data_frame.emojis for a in b)
    emoji_dict = dict(Counter(total_emojis_list))
    emoji_dict = sorted(
        emoji_dict.items(), key=lambda x: x[1], reverse=True)
    # for i in emoji_dict:
    #     print(i)
    emoji_df = pd.DataFrame(emoji_dict, columns=['emojis', 'count'])
    fig = px.pie(emoji_df, values='count', names='emojis')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def time_series_plot(data_frame: pd.DataFrame):
    """
    Time analysis w.r.t to message in chat

    Attributes
    ----------
    Dataframe (pandas DF)

    Retrurns
    --------
    Plotly Figure (pyDash)
    """
    logging.info("WhatsApp/time_series_plot()")
    z_value = data_frame['date'].value_counts()
    z_dict = z_value.to_dict()  # converts to dictionary
    data_frame['msg_count'] = data_frame['date'].map(z_dict)
    # Timeseries plot
    fig = px.line(x=data_frame['date'], y=data_frame['msg_count'])
    fig.update_layout(
        title='Analysis of number of messages using Time Series plot.',
        xaxis_title='Time Stamp',
        yaxis_title='Number of Messages')
    fig.update_xaxes(nticks=60)
    return fig


def plot_data(data_string):
    """
    Common Bar chat Function for plotting data

    Attributes
    ----------
    Dataframe (pandas DF)

    Retrurns
    --------
    Matplotlib Figure
    """
    logging.info("WhatsApp/plot_data()")
    fig, ax_value = plt.subplots()
    # Save the chart so we can loop through the bars below.
    bars = ax_value.bar(
        x=np.arange(data_string.get('x_value')),
        height=data_string.get('y_value'),
        tick_label=data_string.get('tick_label'),
        color="#686868"
    )
    # Axis formatting.
    ax_value.spines['top'].set_visible(False)
    ax_value.spines['right'].set_visible(False)
    ax_value.spines['left'].set_visible(False)
    ax_value.spines['bottom'].set_color('#686868')
    ax_value.tick_params(bottom=False, left=False)
    ax_value.tick_params(axis='x', labelrotation=90)
    ax_value.set_axisbelow(True)
    ax_value.yaxis.grid(True, color='#EEEEEE')
    ax_value.xaxis.grid(False)
    # Grab the color of the bars so we can make the
    # text the same color.
    # bar_color = bars[0].get_facecolor()
    # Add text annotations to the top of the bars.
    # Note, you'll have to adjust this slightly (the 0.3)
    # with different data.
    for bar_value in bars:
        ax_value.text(
            bar_value.get_x() + bar_value.get_width() / 2,
            bar_value.get_height(),
            round(bar_value.get_height(), 1),
            horizontalalignment='center',
            color='green',  # bar_color
            # weight='bold'
        )
    ax_value.set_xlabel(
        data_string.get('x_label'), labelpad=15, color='#333333')
    ax_value.set_ylabel(
        data_string.get('y_label'), labelpad=15, color='#333333')
    ax_value.set_title(
        data_string.get('title'), pad=15, color='#333333')
    return fig


def max_words_used(data_frame: pd.DataFrame):
    """
    Maximum words used in sentence in group chat

    Attributes
    ----------
    Dataframe (pandas DF)

    Retrurns
    --------
    Matplotlib Figure
    """
    logging.info("WhatsApp/max_words_used()")
    # Counting number of letters in each message
    # data_frame['letters'] = data_frame['message'].apply(
    #   lambda s: len(s))
    # # Counting number of word's in each message
    # data_frame['words'] = data_frame['message'].apply(
    #   lambda s: len(s.split(' ')))
    # # np.sum(data_frame['words'])
    max_words = data_frame[['name', 'word_count']].groupby('name').sum()
    m_w = max_words.sort_values('word_count', ascending=False).head(10)
    return plot_data({
            'x_value': m_w.size,
            'y_value': m_w.word_count,
            'tick_label': m_w.index,
            'x_label': 'Name of Group Member',
            'y_label': 'Number of Words in Group Chat',
            'title': 'Analysis of members who has used\
                more words in his/her messages'
        })


def most_active_member(data_frame: pd.DataFrame):
    """
    Most active memeber as per number of messages in group

    Attributes
    ----------
    Dataframe (pandas DF)

    Retrurns
    --------
    Matplotlib Figure
    """
    logging.info("WhatsApp/most_active_member()")
    # Mostly Active Author in the Group
    mostly_active = data_frame['name'].value_counts()
    # Top 10 peoples that are mostly active in our Group
    m_a = mostly_active.head(10)
    return plot_data({
            'x_value': m_a.size,
            'y_value': m_a,
            'tick_label': m_a.index,
            'x_label': 'Name of Group Member',
            'y_label': 'Number of Group Messages',
            'title': 'Mostly Active member in Group (based on messages)'
        })


def most_active_day(data_frame: pd.DataFrame):
    """
    Most active day in Group as per messages numbers

    Attributes
    ----------
    Dataframe (pandas DF)

    Retrurns
    --------
    Matplotlib Figure
    """
    logging.info("WhatsApp/most_active_day()")
    active_day = data_frame['day'].value_counts()
    a_d = active_day.head(10)
    return plot_data({
            'x_value': a_d.size,
            'y_value': a_d,
            'tick_label': a_d.index,
            'x_label': 'Name of Group Member',
            'y_label': 'Number of Group Messages',
            'title': 'Most active day of Week in the Group'
        })


def top_media_contributor(data_frame: pd.DataFrame):
    """
    Top 10 members who shared media's in group

    Attributes
    ----------
    Dataframe (pandas DF)

    Retrurns
    --------
    Matplotlib Figure
    """
    logging.info("WhatsApp/top_media_contributor()")
    # Top-10 Media Contributor of Group
    max_media = data_frame[['name', 'media']].groupby('name').sum()
    m_m = max_media.sort_values(
        'media', ascending=False).head(10)
    return plot_data({
            'x_value': m_m.size,
            'y_value': m_m.media,
            'tick_label': m_m.index,
            'x_label': 'Name of Group Member',
            'y_label': 'Number of Media Shared in Group',
            'title': 'Analysis of Top-10 Media shared in Group'
        })


def who_shared_links(data_frame: pd.DataFrame):
    """
    Top 10 members Who shared maximum links in Group

    Attributes
    ----------
    Dataframe (pandas DF)

    Retrurns
    --------
    Matplotlib Figure
    """
    logging.info("WhatsApp/who_shared_links()")
    # Member who has shared max numbers of link in Group
    max_words = data_frame[['name', 'urlcount']].groupby('name').sum()
    m_w = max_words.sort_values('urlcount', ascending=False).head(10)
    return plot_data({
            'x_value': m_w.size,
            'y_value': m_w.urlcount,
            'tick_label': m_w.index,
            'x_label': 'Name of Group Member',
            'y_label': 'Number of Links Shared in Group',
            'title': 'Analysis of members who has\
                shared max no. of links in Group'
        })


def time_when_group_active(data_frame: pd.DataFrame):
    """
    Most Messages Analsyis w.r.t to Time

    Attributes
    ----------
    Dataframe (pandas DF)

    Retrurns
    --------
    Matplotlib Figure
    """
    logging.info("WhatsApp/time_when_group_active()")
    # Time whenever the group was highly active
    active_time = data_frame.datetime.dt.time.value_counts().head(10)
    return plot_data({
            'x_value': active_time.size,
            'y_value': active_time.values,
            'tick_label': active_time.index,
            'x_label': 'Time',
            'y_label': 'Number of Messages',
            'title': 'Analysis of time when group was highly active'
        })


def most_suitable_hour(data_frame: pd.DataFrame):
    """
    Most Messages Analsyis w.r.t to Hour

    Attributes
    ----------
    Dataframe (pandas DF)

    Retrurns
    --------
    Matplotlib Figure
    """
    logging.info("WhatsApp/most_suitable_hour()")
    # Time whenever the group was highly active
    active_hour = data_frame.datetime.dt.hour.value_counts().head(20)
    return plot_data({
            'x_value': active_hour.size,
            'y_value': active_hour.values,
            'tick_label': active_hour.index,
            'x_label': 'Hour',
            'y_label': 'Number of Messages',
            'title': 'Analysis of hour when group was highly active'
        })


def most_suitable_day(data_frame: pd.DataFrame):
    """
    Most Messages Analsyis w.r.t to Day

    Attributes
    ----------
    Dataframe (pandas DF)

    Retrurns
    --------
    Matplotlib Figure
    """
    logging.info("WhatsApp/most_suitable_day()")
    # Time whenever the group was highly active
    active_day = data_frame.datetime.dt.day.value_counts().head(20)
    return plot_data({
            'x_value': active_day.size,
            'y_value':  active_day.values,
            'tick_label': active_day.index,
            'x_label': 'Day',
            'y_label': 'Number of Messages',
            'title': 'Analysis of Day when group was highly active'
        })


def sentiment_analysis(cloud_df: pd.DataFrame):
    """
    Sentiment analysis score

    Attributes
    ----------
    Dataframe (pandas DF)

    Retrurns
    --------
    Matplotlib Figure
    """
    cloud_df['sentiment'] = cloud_df.message.apply(
        lambda text: TextBlob(text).sentiment.polarity)
    sentiment = cloud_df[['name', 'sentiment']].groupby('name').mean()
    s_a = sentiment.sort_values('sentiment', ascending=False).head(10)
    return plot_data({
            'x_value': s_a.size,
            'y_value': s_a.sentiment,
            'tick_label': s_a.index,
            'x_label': 'Name of Group Member',
            'y_label': 'Positive Sentiment in Group',
            'title': 'Analysis of members having higher\
                score in Positive Sentiment'
        })