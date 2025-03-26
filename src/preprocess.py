# Let them know that data is sort of biased. With a lot of occurences of 5 star ratings
# Text Pre-Processing


import spacy
import pandas as pd
from tqdm import tqdm
tqdm.pandas()


pd.set_option('display.max_colwidth', None)

df = pd.read_csv('Zillow data - CA.csv') 

# Load the English model
nlp = spacy.load("en_core_web_sm")


def spacy_preprocess(text):
    doc = nlp(text.lower())  # lowercasing + spaCy pipeline
    
    tokens = []
    for token in doc:
        # Filter tokens
        if (not token.is_stop) and (not token.is_punct) and (token.is_alpha or token.like_num):
            tokens.append(token.lemma_)  # Lemmatize
        
    return ' '.join(tokens)

    
#small_df = df.head(1000)
df['Cleaned_Description'] = df['Description'].astype(str).progress_apply(spacy_preprocess)

# Save df to CSV in your local machine
df.to_csv('processed_zillow_reviews.csv', index=False)
