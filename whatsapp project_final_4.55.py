# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 13:26:46 2024

@author: Felipe Leite
"""

import emoji
import emot
import pandas as pd
from collections import Counter
from whatstk import WhatsAppChat
from bertopic import BERTopic
from umap import UMAP

chat = WhatsAppChat.from_source(filepath=r"C:\Users\Felipe Leite\Downloads\2024-WhatsApp Chat1.txt", auto_header=True).df
print(chat)

import re
import unicodedata

def clean_text(text):
    # Normalize text to handle hidden characters
    text = unicodedata.normalize("NFKD", text)
    # Remove media placeholders and deleted message tags
    text = text.replace('<Media omitted>', '').replace('This message was deleted', '')
    text = text.replace('[Media omitted]', '').replace('[Media Omitted]', '').replace('<media omitted>', '')
    # Remove URLs
    text = re.sub(r'(https?://\S+|www\.\S+)', '', text)
    # Remove numbers
    text = re.sub(r'[0-9]+', '', text)
    # Standardize whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep emojis using a regex pattern
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F700-\U0001F77F"  # alchemical symbols
                               u"\U0001F780-\U0001F7FF"  # geometric shapes extended
                               u"\U0001F800-\U0001F8FF"  # supplemental arrows-C
                               u"\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
                               u"\U0001FA00-\U0001FA6F"  # chess symbols
                               u"\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-A
                               u"\U00002702-\U000027B0"  # dingbats
                               u"\U000024C2-\U0001F251"  # enclosed characters
                               "]+", flags=re.UNICODE)
    # Keep emojis and remove other non-alphanumeric characters
    text = ''.join([char if emoji_pattern.match(char) else re.sub(r'[^\w\s]', '', char) for char in text])
    return text.lower().strip()

# Function to normalize emojis
def normalize_emojis(text):
    return emoji.demojize(text)  # Converts emojis to descriptive text

# Apply functions
chat['clean_msg'] = chat['message'].apply(clean_text).apply(normalize_emojis)



# Apply the function to the 'message' column
chat['clean_msg'] = chat['message'].apply(clean_text)
emot_obj = emot.emot()
chat['message'].apply(lambda x: '' if re.compile(r'http\S+').search(x) else ''.join(emot_obj.emoticons(x)['value'])
                      ).value_counts().rename_axis('emoticon').reset_index(name='count').query("emoticon != ''")[['emoticon']]
chat['message'] = chat['message'].replace({':\(': '☹️', '>:\(': '😠',
                                           ':\)': '🙂', ':D': '😃'
                                           }, regex=True)

# emoji extraction
chat['emoji'] = chat['message'].apply(lambda x: ''.join(c for c in x if c in emoji.EMOJI_DATA))
# date extraction
chat['hour'] = chat['date'].dt.hour
chat['day_name'] = chat['date'].dt.day_name()
chat['week'] = (chat['date'] - pd.Timestamp('2024-01-01')).dt.days // 7


# Aggregate message count and emojis, then reset the index to add the 'username' column
stats = chat.groupby('username').agg({
    'message': 'count',
    'emoji': lambda x: ' '.join(set(emoji for emojis in x.dropna() for emoji in emojis))
}).sort_values(by='message', ascending=False).reset_index()

import matplotlib.pyplot as plt

# Calculate the values for 'Chats without emoji' and 'Chats with emoji'
emoji_counts = chat.assign(is_emoji=chat['emoji'].apply(lambda x: True if x != '' else False))\
                  .groupby('is_emoji').count()[['message']].reset_index()['message']
# Define labels and colors
labels = ['Chats without emoji', 'Chats with emoji']
colors = ['#25D366', '#075E54']
# Create the pie chart
plt.figure(figsize=(6, 6))
plt.pie(emoji_counts, labels=labels, colors=colors, autopct='%1.1f%%', startangle=65, pctdistance=0.85)
# Add a hole in the middle (for a donut chart effect)
centre_circle = plt.Circle((0, 0), 0.50, color='white', fc='white', linewidth=0)
plt.gca().add_artist(centre_circle)
# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')  
# Show the chart
plt.title('Emojis?')
plt.show()

# Save in PNG
# plt.savefig('emoji_chat_pie_chart.png', bbox_inches='tight')

# Count all emojis and create a DataFrame with their frequency
emoji_counts = Counter([emoji for message in chat.emoji for emoji in message])
emoji_stats = pd.DataFrame(emoji_counts.most_common(), columns=['emoji', 'count'])
# Display the entire list of used emojis and their frequencies
print(emoji_stats)
#emoji_stats definition
emoji_stats_top = pd.DataFrame(Counter([emoji for message in chat.emoji for emoji in message]).most_common(),
              columns=['emoji', 'count'],
              index=range(1, len(Counter([emoji for message in chat.emoji for emoji in message]).most_common())+1)
              ).head()

# Create a list of (username, emoji) pairs for all messages
username_emoji_pairs = [(username, emoji) 
                        for username, emojis in zip(chat['username'], chat['emoji']) 
                        for emoji in emojis]

# Convert to a DataFrame
emoji_user_dataset = pd.DataFrame(username_emoji_pairs, columns=['username', 'emoji'])

# Display the DataFrame
print(emoji_user_dataset)

# Calculate message length for each message
chat['message_length'] = chat['message'].apply(lambda x: len(x.split()) if x != '<Media omitted>' else 0)
# Compute average message length per username
average_message_length = chat.groupby('username')['message_length'].mean().reset_index()

# Rename the column for clarity (optional)
average_message_length.rename(columns={'message_length': 'average_message_length'}, inplace=True)

#emojis chart
# Plot the bar chart
plt.figure(figsize=(15, 8))
plt.bar(emoji_stats_top['emoji'], emoji_stats_top['count'], color='orange')
# Add labels and title
plt.xlabel('Emoji')
plt.ylabel('Frequency')
plt.title('Top Emoji Usage in Chat')
# Optionally rotate emoji labels for readability if there are many
plt.xticks(rotation=45)
# Display the bar chart
plt.show()

#messages chart
# Plot the bar chart
plt.figure(figsize=(12, 6))
plt.bar(stats['username'], stats['message'], color='green')
# Add labels and title
plt.xlabel('Emoji')
plt.ylabel('Frequency')
plt.title('Top Emoji Usage in Chat')
# Optionally rotate emoji labels for readability if there are many
plt.xticks(rotation=90)
# Display the bar chart
plt.show()

import nltk
from nltk.corpus import stopwords

# Download the stopwords dataset if you haven't already
nltk.download('stopwords')

# Load Brazilian Portuguese stopwords
stop_words = stopwords.words('portuguese')

# Add your own stopwords (example words added here)
custom_stopwords = ['nao', 'pra', 'ta', 'vc', 'vai', 'ja', 'q', 'aqui', 'ai', 'gente', 'vou', 'dia', 'hahaha', 'hahahaha', 'vcs', 'edited',]  # Add more words as needed

# Combine the default stopwords with your custom ones
stop_words.extend(custom_stopwords)

# Remove stopwords from your clean messages
chat['clean_msg'] = chat['clean_msg'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))

# Continue with your wordcloud or other analysis

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Join all cleaned messages into a single string
text = ' '.join(chat['clean_msg'])

# Create a word cloud
wordcloud = WordCloud(width=1200, height=800, background_color='white', collocations=False).generate(text)

# Display the generated word cloud
plt.figure(figsize=(15, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # Turn off axis
plt.show()

# Group by 'day_name' and count occurrences
day_name_counts = chat.groupby('day_name').size().reset_index(name='count')

# Define the order of days of the week
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Sort the dataframe according to the days of the week
day_name_counts['day_name'] = pd.Categorical(day_name_counts['day_name'], categories=days_order, ordered=True)
day_name_counts = day_name_counts.sort_values('day_name')

# Plot the line chart
plt.figure(figsize=(12, 6))
plt.plot(day_name_counts['day_name'], day_name_counts['count'], marker='o', color='orange')

# Add labels and title
plt.xlabel('Day of the Week')
plt.ylabel('Frequency')
plt.title('Frequency of Messages by Day')

# Optionally rotate the x-axis labels for readability
plt.xticks(rotation=45)

# Display the chart
plt.show()

# Group by 'day_name' and 'username', then count occurrences
day_name_counts = chat.groupby(['day_name', 'username']).size().reset_index(name='count')

# Define the order of days of the week
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Sort the dataframe according to the days of the week
day_name_counts['day_name'] = pd.Categorical(day_name_counts['day_name'], categories=days_order, ordered=True)
day_name_counts = day_name_counts.sort_values('day_name')

# Get unique usernames for different lines
usernames = day_name_counts['username'].unique()

# Define a list of 14 distinct colors using hex color codes or common color names
color_list = [
    'blue', 'orange', 'green', 'red', 'purple', 'brown', 
    'pink', 'gray', 'olive', 'cyan', 'yellow', 'magenta', 
    'lime', 'indigo'
]

# Plot the line chart for each user
plt.figure(figsize=(14, 8))

# Add labels and title
plt.xlabel('Day of the Week')
plt.ylabel('Frequency')
plt.title('Frequency of Messages by Day for Each User')

# Optionally rotate the x-axis labels for readability
plt.xticks(rotation=45)

# Show legend
plt.legend(title='Username')

# Display the chart
plt.show()

# Group by 'name' and 'date', and aggregate to count messages and words
summary = chat.groupby(['username', chat['date'].dt.date]).agg(
    messages=('message', 'count'),
    words=('message_length', 'sum')
).reset_index()

# Save the summary as a new CSV file
output_path = 'chat_summary_by_name_and_date.csv'
summary.to_csv(output_path, index=False)

print(f"Summary data has been saved to {output_path}")

# # Fit the BERTopic model using the clean messages
# model = BERTopic(
#     umap_model=UMAP(n_neighbors=15,
#                     n_components=5,
#                     min_dist=0.0,
#                     metric='cosine',
#                     random_state=13),
#     language='multilingual',
#     calculate_probabilities=True,
#     nr_topics='auto'
# )

# # Ensure only non-empty messages are used
# topics, probabilities = model.fit_transform(chat.loc[chat['clean_msg'] != '', 'clean_msg'].tolist())

# topic_words = model.get_topic_info()  # Get top words for each topic
# topic_labels = {topic_id: ', '.join(words[:5]) for topic_id, words in topic_words.iterrows()}

# # Map numerical topics to labels
# topics = [topic_labels[topic] for topic in topics]



# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Create a pivot table: rows = users, columns = hours
# heatmap_data = chat.pivot_table(index='username', columns='date', values='message', aggfunc='count', fill_value=0)

# # Plot heatmap
# plt.figure(figsize=(12, 6))
# sns.heatmap(heatmap_data, annot=True, cmap='coolwarm', fmt='d')
# plt.title('User Message Responses Heatmap')
# plt.xlabel('Hour of the Day')
# plt.ylabel('User')
# plt.show()

# Save to a specific folder (Desktop/ChatAnalysis)
file_path = r'C:\Users\Felipe Leite\Downloads\day_name_counts.txt'
day_name_counts.to_csv(file_path, sep='\t', index=False)

print(f"File saved successfully at: {file_path}")

file_path = r'C:\Users\Felipe Leite\Downloads\average_message_length.txt'
average_message_length.to_csv(file_path, sep='\t', index=False)

print(f"File saved successfully at: {file_path}")

file_path = r'C:\Users\Felipe Leite\Downloads\chat.txt'
chat.to_csv(file_path, sep='\t', index=False)

print(f"File saved successfully at: {file_path}")

file_path = r'C:\Users\Felipe Leite\Downloads\emoji_user_dataset.txt'
emoji_user_dataset.to_csv(file_path, sep='\t', index=False)

print(f"File saved successfully at: {file_path}")

# file_path = r'C:\Users\Felipe Leite\Downloads\topic_words.txt'
# topic_words.to_csv(file_path, sep='\t', index=False)

# print(f"File saved successfully at: {file_path}")

file_path = r'C:\Users\Felipe Leite\Downloads\summary.txt'
summary.to_csv(file_path, sep='\t', index=False)

print(f"File saved successfully at: {file_path}")