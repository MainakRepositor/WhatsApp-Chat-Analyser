"""
Streamlit WhatsApp Chat Analyzer
"""
import re
import os
import time
import warnings
import logging
import logging.config
import yaml
from typing import Dict, Any
import streamlit as st
from numpy import sum as npsum
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from processor.transformers.chat_eda import WhatsAppProcess, sorted_authors_df,\
    statistics, process_data, WhatsAppConfig
from processor.graphs.charts import pie_display_emojis, time_series_plot,\
    message_cluster, most_active_member, most_active_day,\
    max_words_used, top_media_contributor, who_shared_links,\
    sentiment_analysis, most_suitable_day, most_suitable_hour
from processor.common.configure import BANNER, TITLE, REPO_URL, FORMAT_BUTTON,\
    HIDE_STREAMLIT_STYLE, MAIN_STYLE, APPLICATION_FEATURE


st.set_option('deprecation.showPyplotGlobalUse', False)

warnings.filterwarnings(
    "ignore", message="Glyph 128584 missing from current font.")


# Initial page config
st.set_page_config(
    page_title=TITLE,
    page_icon="",
    # layout="wide",
    initial_sidebar_state="expanded",
)


# Application NAV BAR
_, n2, n3 = st.columns([4, 2, 1])
nav_area = st.empty()


nav_area.write("")


st.title(TITLE)


st.subheader("**♟ General Statistics ♟**")
st.write('''* This app is meant as for educational and demonstration purpose only.
    Try it out by `Uploading WITHOUT MEDIA whatsapp chat export` here.''')

st.sidebar.title("WhatsApp Chat Analyzer")
st.sidebar.markdown('''Analyze the chats. Unravel the mysteries behind words''')
st.sidebar.markdown(APPLICATION_FEATURE)





def add_multilingual_stopwords() -> Dict:
    """
    Function read language file stop words and covert
    them into List of STOPWORDS.
    Top languages added under stopwords folder.

    attributes
    ----------
    None

    Returns
    -------
    set: Distinct list of words
    """
    multilingul_list = []
    for file in os.listdir('configs/stopwords'):
        stopword = open('configs/stopwords/' + file, "r")
        for word in stopword:
            word = re.sub('[\n]', '', word)
            multilingul_list.append(word)
    return set(STOPWORDS).union(set(multilingul_list))
    

def generate_word_cloud(text: str, title: str) -> Any:
    """
    Function takes text as input and transform it to
    WordCloud display

    attributes
    ----------
    text (str): String of words
    title (str): title Sting

    Return
    ------
    Matplotlib figure for wordcloud
    """
    # wordcloud = WordCloud(
    #   stopwords=stopwords, background_color="white").generate(text)
    wordcloud = WordCloud(
        scale=3,
        width=500,
        height=330,
        max_words=200,
        colormap='tab20c',
        stopwords=add_multilingual_stopwords(),
        collocations=True,
        contour_color='#5d0f24',
        contour_width=3,
        font_path='Laila-Regular.ttf',
        background_color="white").generate(text)
    # Display the generated image:
    # the matplotlib way:
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(title)
    st.pyplot()


def next_page():
    """Pagination page Increment"""
    st.session_state.page += 1


def prev_page():
    """Pagination page Decrement"""
    st.session_state.page -= 1


def pagination_of_dataframe(raw_df):
    """
    Display DataFrame in Pagination format
    """
    if "page" not in st.session_state:
        st.session_state.page = 0
    col1, _, _, col2, _, col3 = st.columns(6)
    if st.session_state.page < 10:
        col3.button("Next", on_click=next_page)
    else:
        col3.write("")  # this makes the empty column show up on mobile
    if st.session_state.page > 0:
        col1.button("Previous", on_click=prev_page)
    else:
        col1.write("")  # this makes the empty column show up on mobile
    col2.write(f"Page {1+st.session_state.page} of {5}")
    start = 10 * st.session_state.page
    end = start + 10
    st.write("")
    st.dataframe(raw_df[["datetime", "name", "message"]].iloc[start:end])
    st.markdown("#")


def display_statistics(stats):
    """
    Display Chat statistics with metric format
    """
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Total Messages", stats.get('total_messages'), delta="📦 📨")
    col2.metric(
        "Total Members", stats.get('total_members'), "💃🕺")
    col3.metric(
        "Total Media", stats.get('media_message'), delta="🎞️ 📷")
    col4.metric(
        "Link shared", int(stats.get('link_shared')), delta="🖇️ 🔗")
    st.text("")
    
    st.text("")


def chart_display(data_frame):
    """
    Combine Charts display function
    """
    st.markdown("----")
    st.header("🔘 Most Active Member")
    st.info("🔋 Member comparision based on the number of messages\
        he/she posted in group chat")
    st.pyplot(most_active_member(data_frame))

    st.markdown("----")
    st.header("🔘  Most Active Day")
    st.info("🔋 Member comparision based on the number of messages\
        he/she posted in group chat whatsapp.r.t Day")
    st.pyplot(most_active_day(data_frame))

    st.markdown("----")
    st.header("🔘 Who uses more words in sentences")
    st.info("🔋 Member uses more number of sentences during the conversation")
    st.pyplot(max_words_used(data_frame))

    st.markdown("----")
    st.header("🔘 Who shares Links in group most? ")
    st.info("🔋 Members who shares internet links of information with others")
    st.pyplot(who_shared_links(data_frame))

    
    st.markdown("----")
    st.header("🔘 Most Active Day ")
    st.info("🔋 Member who active for suitable Day")
    st.pyplot(most_suitable_day(data_frame))

    st.markdown("----")
    st.header("🔘 Most Active Hour")
    st.info("🔋 Member who active during suitable hours")
    st.pyplot(most_suitable_hour(data_frame))

    st.markdown("----")
    st.header("🔘 Member activity Cluster")
    st.info("🔋 Cluster hover about the total messages, Emoji's, Links, Words\
        and Letter by individual member")
    st.write(message_cluster(data_frame))

    st.markdown("----")
    st.header("🔘 Over the Time Analysis ")
    st.info("🔋 Group activity over the time whatsapp.r.t to\
        number of messages")
    st.write(time_series_plot(data_frame))

    st.markdown("----")
    st.header("🔘 Curious about Emoji's ?")
    st.info("🔋 The most use Emoji's in converstion is show with\
        larger sector")
    pie_display = pie_display_emojis(data_frame)
    st.plotly_chart(pie_display)


def file_process(data, config):
    """
    Regex passed message format frocessing function
    """
    # reading source configuration
    source_config = WhatsAppConfig(**config['whatsapp'])
    whatsapp = WhatsAppProcess(source_config)
    message = whatsapp.apply_regex(data)
    raw_df = process_data(message)
    data_frame = whatsapp.get_dataframe(raw_df)
    stats = statistics(raw_df, data_frame)

    st.markdown(f'# {stats.get("group_name")}')

    st.markdown("----")

    # Pagination of dataframe Display
    pagination_of_dataframe(raw_df)

    # Display Statistics
    display_statistics(stats)

    # Formation of Word Cloud Dataframe
    cloud_df = whatsapp.cloud_data(raw_df)

    # Frequently used word and word Cloud display for
    #   Indidvidual member and statitics
    st.header("🔘 Frequently used words")
    sorted_authors = sorted_authors_df(cloud_df)
    select_author = []
    select_author.append(st.selectbox('', sorted_authors))
    dummy_df = cloud_df[cloud_df['name'] == select_author[0]]
    text = " ".join(review for review in dummy_df.message)

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Posted Messages",
        dummy_df[dummy_df['name'] == select_author[0]].shape[0])
    col2.metric(
        "Emoji's Shared", sum(
            data_frame[data_frame.name.str.contains(
                select_author[0][-5:])].emojis.str.len()))
    col3.metric("Link Shared", int(
        data_frame[data_frame.name == select_author[0]].urlcount.sum()))
    col4.metric("Total Words", int(
        data_frame[data_frame.name == select_author[0]].word_count.sum()))
    user_df = data_frame[data_frame.name.str.contains(
        select_author[0][-5:])]
    average = round(npsum(user_df.word_count)/user_df.shape[0], 2)
    col5.metric("Average words/Message", average)

    if len(text) != 0:
        generate_word_cloud(
            text, "Word Cloud for individual Words")
    else:
        generate_word_cloud(
            "NOWORD", "Word Cloud for individual Words")

    st.markdown("----")
    st.header("🔘 Words and Phrases frequently used in Chat")
    st.info("🔋 Frequently used words or phrases by all members in group chat.\
        Most dicussion occurs around below words or used frequently.")
    text = " ".join(review for review in cloud_df.message)
    generate_word_cloud(
        text, "Word Cloud for Chat words")
    
    st.markdown("----")
    st.header("🔘 Who has Positive Sentiment? ")
    st.info("🔋 Member sentiment analysis score base on the words used in\
        messages. Sentiment Score above 0.5 to 1 is consider as Positive.\
        Pure English words and Phrases is ideal for calcalation")
    st.pyplot(sentiment_analysis(cloud_df))

    # DataFrame processing w.r.t Day hour and Date
    whatsapp.day_analysis(data_frame)

    # Calling Combine chart function
    chart_display(data_frame)
    
    

    st.markdown("----")
    st.header("🔘 Top-10 Media Contributor ")
    st.info("🔋 Comparision of members who contributes more number of Images,\
        Video or Documents")
    st.pyplot(top_media_contributor(raw_df))

    

    # Footer Message for Tree Plantation
    st.markdown("----")
    


def main():
    """
    Function will process the txt data and process into
    Pandas Dataframe items
    """
    # Parsing YAML file
    config = 'configs/app_configuration.yml'
    config = yaml.safe_load(open(config))
    # configure logging
    log_config = config['logging']
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(__name__)
    logger.info("Welcome to WhatsApp Chat Analyzer")

    c1, c2 = st.columns([3, 1])
    # Uploaded file processing function
    uploaded_file = c1.file_uploader(
        "Choose a TXT file only",
        type=['txt'],
        accept_multiple_files=False)
        

    if uploaded_file is not None:
        # Convert txt string to utf-8 Encoding
        data = uploaded_file.getvalue().decode("utf-8")
        # Compatible iOS and Android regex search
        st.markdown("The Genesis chatter of the group:")
        file_process(data, config)
        
    
    
        

if __name__ == "__main__":
    print(BANNER)
    main()
