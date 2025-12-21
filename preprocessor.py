import re
import pandas as pd

def preprocess(data):
    # --- 1. PATTERN MATCHING ---
    # Pattern for WhatsApp date formats (handles 12hr with AM/PM and 24hr)
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:[Aa][Mm]|[Pp][Mm])?\s-\s'

    # Split data into messages and capture the dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # If the first pattern fails (Android/Iphone differences), try the 24h fallback
    if not messages:
        pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
        messages = re.split(pattern, data)[1:]
        dates = re.findall(pattern, data)

    # Create the initial DataFrame
    df = pd.DataFrame({'raw_content': messages, 'message_date': dates})
    
    # --- 2. DATE CLEANING ---
    # Remove the separator ' - ' and convert to Python datetime objects
    df['message_date'] = df['message_date'].str.replace(' - ', '', regex=False)
    df['date'] = pd.to_datetime(df['message_date'], infer_datetime_format=True)

    # --- 3. SPLITTING USER AND MESSAGE ---
    # This logic creates the two separate columns you requested
    users = []
    message_content = []
    
    for message in df['raw_content']:
        # Split only on the first occurrence of ': ' to separate name from text
        entry = re.split(r'([\w\W]+?):\s', message)
        
        if len(entry) > 1: # If it's a message from a user
            users.append(entry[1])
            message_content.append(entry[2])
        else: # If it's a system notification (e.g. "You were added", "Messages are encrypted")
            users.append('group_notification')
            message_content.append(entry[0])

    # Assign the new clean columns
    df['user'] = users
    df['message'] = message_content
    
    # --- 4. FEATURE EXTRACTION ---
    # Breaking down the date for easier analysis later
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # --- 5. CLEANUP ---
    # Dropping the temporary raw columns so only the clear ones remain
    df.drop(columns=['raw_content', 'message_date'], inplace=True)

    return df