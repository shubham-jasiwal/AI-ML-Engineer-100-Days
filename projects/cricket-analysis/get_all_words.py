import pandas as pd
import pandas as pd
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize

from nltk import word_tokenize, pos_tag


extra_noise = {
    "oh", "wow", "nicely", "watchful", "lovely", "beautiful", "brilliant", "surely",
    "really", "just", "bit", "ah", "yes", "no", "great", "fantastic"
}

def remove_names(text):
    tokens = word_tokenize(str(text))
    tagged = pos_tag(tokens)
    
    # Filter out proper nouns and extra_noise
    filtered = [
        word for word, tag in tagged 
        if tag not in ('NNP', 'NNPS') and word.lower() not in extra_noise
    ]
    
    return ' '.join(filtered)
    
def remove_name(text):
    tokens = word_tokenize(str(text))
    tagged = pos_tag(tokens)
    
    filtered = [word for word, tag in tagged if tag not in ('NNP', 'NNPS')]
    return ' '.join(filtered)

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

df = pd.read_json('data/ind_vs_eng-1_test.json')

data=[]

def lemmatize_text(text):
    tokens = word_tokenize(str(text).lower())
    filtered_tokens = [word for word in tokens if word not in stop_words]
    lemmas = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    return ' '.join(lemmas)

for i in df['content']:
    print("--")
    print(i)
    print("--")
    remove_name = remove_names(i)
    print(remove_name)
    print("--")
    lemma = lemmatize_text(remove_name)
    print(lemma)
    print("--")
    print(word_tokenize(str(lemma).lower()))
