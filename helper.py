
from urlextract import URLExtract
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