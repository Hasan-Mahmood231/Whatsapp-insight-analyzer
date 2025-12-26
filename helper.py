
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


extract = URLExtract()
def fetch_stats(selected_user,df):
    #group level analyses
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_message = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
        # 1. fetch number of messages 
        
    #fetch number of media
    num_media = df[df['message'].str.contains('<Media omitted>', na=False)].shape[0]

    #fetch url
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))


    return num_message,len(words),num_media,len(links)


#function to fetch most active user.
def fetch_active_user(df):
    # Ensure you are returning the value_counts, which is a Series
    x =  df['user'].value_counts().head()
    user_df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns = {'index':'name','user':'percent'})

    return x,user_df

#wordcloud 
# def create_wordcloud(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     wc = WordCloud(width = 500,height = 500,min_font_size = 10,background_color = 'white')
#     df_wc = wc.generate(df['message'].str.cat(sep=' '))
#     return df_wc
def create_wordcloud(selected_user, df):
    # 1. Filter by user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # 2. IMPORTANT: Remove "<Media omitted>" messages
    # This creates a temporary dataframe without the media placeholder
    temp = df[df['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != '<Media omitted>'] # Just in case the newline varies

    # 3. Create the WordCloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    
    # Generate from the filtered 'temp' dataframe
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    
    return df_wc

def most_common_words(selected_user,df):
    f = open('stop_words.txt','r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'group_notification']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df

#EMOJI ANALYSIS.
def emoji_hepler(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []

    # Use .astype(str) to avoid errors if there are empty or numerical messages
    for message in df['message'].astype(str):
        # This list comprehension checks each character using the new library method
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df



#timeline for montly messages.
def monthly_timline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

#weekly activity map
def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()