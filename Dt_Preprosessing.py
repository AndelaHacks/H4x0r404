# import basic libraries
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
stemmer = PorterStemmer()

# function to clean text
def review_to_words(raw_review):
    # 1. Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", raw_review) 
    #
    # 2. Convert to lower case, split into individual words
    words = letters_only.lower().split()
    #
    # 3. Remove Stopwords. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))                  
    # 
    # 4. Remove stop words
    meaningful_words = [w for w in words if not w in stops]  #returns a list 
    #
    # 5. Stem words. Need to define porter stemmer above
    singles = [stemmer.stem(word) for word in meaningful_words]
    # 6. Join the words back into one string separated by space, 
    # and return the result.
    return( " ".join( singles ))  

# apply it to our text data 
# dataset is named wine_data and the text are in the column "wmn"
processed_wmn = [ review_to_words(text) for text in wine_data.wmn]
