import pandas as pd
import re
import string
import numpy as np
# Install the emoji library
#!pip install emoji
import emoji
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer,WordNetLemmatizer
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv(r'C:\Users\Admin\Documents\Team 4 Cleaning\rowing_data.csv')
df.head()
#checking misiing values
percentage_missing = (df.isna().sum() / len(df)) * 100
percentage_missing
df.duplicated().sum()
#drop duplicates
df = df.drop_duplicates()
#dropping null values
df.dropna(inplace = True)
#dropping Unnecesary column
df.drop(columns=['links'],inplace=True)
#check for whitespaces by checking length of values
df['summary_length'] = df['summary'].apply(lambda x: len(str(x)))
print(df[['summary', 'summary_length']].sort_values('summary_length').head(10))
#converting whitespaces to NaN
df['summary'] = df['summary'].apply(lambda x: np.nan if isinstance(x, str) and x.strip()=='' else x)
#replace nan with unknown
df['summary'] = df['summary'].replace(np.nan, 'unknown')
#check for whitespaces in content column by checking length of values
df['content_length'] = df['content'].apply(lambda x: len(str(x)))
print(df[['content', 'content_length']].sort_values('content_length').head(10))
# Reset the index and drop the old index
df.reset_index(drop=True, inplace=True)
#remove urls
def remove_url(text):
    return re.sub(r'https?://\S+|www\.\S+', '', text)

df['summary'] = df['summary'].apply(remove_url)
df['content'] = df['content'].apply(remove_url)
#This function removes punctuations
def remove_punct(text):
    return text.translate(str.maketrans('', '', string.punctuation))

df['summary'] = df['summary'].apply(remove_punct)
df['content'] = df['content'].apply(remove_punct)
#This function removes username
def remove_at(text):
    return re.sub(r'@\w+', '', text)

df['summary'] = df['summary'].apply(remove_at)
df['content'] = df['content'].apply(remove_at)
#This function removes html tags
def remove_html(text):
    return re.sub(r'<.*?>', '', text)

df['summary'] = df['summary'].apply(remove_html)
df['content'] = df['content'].apply(remove_html)
# This function removes emoji
def remove_emoji(text):
    return emoji.replace_emoji(text, replace='')

df['summary'] = df['summary'].apply(remove_emoji)
df['content'] = df['content'].apply(remove_emoji)
# Download necessary NLTK data
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    # Remove Stopwords
def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return " ".join(filtered_words)

df['content'] = df['content'].apply(remove_punct)
df['summary'] = df['summary'].apply(remove_punct)
#!pip install wordninja
import wordninja
# Function to split merged words
def split_words(text):
    if isinstance(text, str):  # Ensure text is a string
        return " ".join(wordninja.split(text))
    return text  # Return as is if not a string
# Apply word splitting to 'summary' and 'content' columns
df['summary'] = df['summary'].apply(split_words)
df['content'] = df['content'].apply(split_words)
#convert to lower
df["summary"]=df["summary"].str.lower()
df["content"]=df["content"].str.lower()
df['title']=df['title'].str.lower()
# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Function to lemmatize text
def lemmatize_text(text):
    if isinstance(text, str):  # Ensure text is a string
        words = text.split()
        return " ".join(lemmatizer.lemmatize(word) for word in words)
    return text  # Return as is if not a string

# Apply lemmatization to 'summary' and 'content' columns
df["summary"] = df["summary"].apply(lemmatize_text)
df["content"] = df["content"].apply(lemmatize_text)
#drop unnecessary columns
df.drop(columns=['summary_length','content_length'],inplace=True)


"""def clean_text(text, politics_terms=None):
  
    #Cleans text while considering cases where the text may contain code snippets.
    
    if not isinstance(text, str):
        return text

    if is_code(text):
        return text  # Do not alter code snippets

    text = text.lower().replace("\n", " ")

    

    # Combined regex operations with pre-compiled patterns
    text = non_ascii_re.sub(" ", text)  # Remove non-ASCII
    text = number_word_re.sub(r"\1 \2", text)  # Separate numbers from words
    text = extra_space_re.sub(" ", text).strip()  # Remove extra spaces
    text = single_char_re.sub("", text)  # Remove single characters only

    text = process_numbers(text)
    text = process_math_expressions(text)

    return text.strip()"""