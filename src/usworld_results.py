import csv
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

class USWorldResults:
  def __init__(self, folder):
    self.sports = [self.preprocess_article(row) for row in csv.DictReader(open(folder + "sports.csv"))]
    self.local = [self.preprocess_article(row) for row in csv.DictReader(open(folder + "local.csv"))]

  def preprocess_article(self, row):
    lmtz = WordNetLemmatizer()
    row["content_tokens"] = [lmtz.lemmatize(w) for w in nltk.wordpunct_tokenize(row["content"]) 
                              if not w in stopwords.words('english')]
    row["headline_tokens"] = [lmtz.lemmatize(w) for w in nltk.wordpunct_tokenize(row["headline"])
                              if not w in stopwords.words('english')]
    return row
