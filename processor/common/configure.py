"""Hold Streamlit Configuration details for Application"""

# Banner Display on backend terminal
BANNER = """
Welcome to

       \\ \\        / / |         | |
        \\ \\  /\\  / /| |__   __ _| |_ ___  __ _ _ __  _ __
         \\ \\/  \\/ / | '_ \\ / _` | __/ __|/ _` | '_ \\| '_ \\
          \\  /\\  /  | | | | (_| | |_\\__ \\ (_| | |_) | |_) |
         __\\/_ \\/   |_| |_|\\__,_|\\__|___/\\__,_| .__/| .__/
        / ____| |         | |                 | |   | |
       | |    | |__   __ _| |_                |_|   |_|
       | |    | '_ \\ / _` | __|
       | |____| | | | (_| | |_
        \\_____|_| |_|\\__,_|\\__|
                |  __ \\
                | |__) | __ ___   ___ ___  ___ ___  ___  _ __
                |  ___/ '__/ _ \\ / __/ _ \\/ __/ __|/ _ \\| '__|
                | |   | | | (_) | (_|  __/\\__ \\__ \\ (_) | |
                |_|   |_|  \\___/ \\___\\___||___/___/\\___/|_|

    
    """

TITLE = "WhatsApp Chat Analyzer"

# Github button display on sidebar SETUP
REPO_URL = "https://ghbtns.com/github-btn.html?user=MainakRepositor&repo=WhatsApp-Analyzer"
FORMAT_BUTTON = 'frameborder="0" scrolling="0" width="170" height="30" title="GitHub"'

# Streamlit footer addition and remove the default streamlit features
HIDE_STREAMLIT_STYLE = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
footer:after {
    content:'copyrights © 2021 mainakc24365@gmail.com';
    visibility: visible;
    display: block;
    position: fixed;
    #background-color: red;
    padding: 1px;
    bottom: 0;
}
</style>"""

# Application Formatting for good display
PADDING = 0
MAIN_STYLE = """ <style>
    .reportview-container .main .block-container{{
        padding-top: {PADDING}rem;
        padding-right: {PADDING}rem;
        padding-left: {PADDING}rem;
        padding-bottom: {PADDING}rem;
    }} </style> """

# Application Features text for display on Sidebar
APPLICATION_FEATURE = '''
** Application Feature: **

- Individual Messenger Statistics
- Activity Cluster
- Emoji's distrubution
- Time series analysis
- Sentiment Score of Member
'''
