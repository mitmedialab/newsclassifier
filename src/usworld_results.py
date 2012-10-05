import csv
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import random

class USWorldResults:
  def __init__(self, folder):
    self.categories = {"sports":None, "local":None}
    self.category_words = {"content":[], "headline":[]}
    self.frequencies={"content":nltk.FreqDist(), "headline":nltk.FreqDist()}

    for category in self.categories:
      self.categories[category] = {}
      self.categories[category]["documents"] = [self.preprocess_article(row, category) 
        for row in csv.DictReader(open(folder + category + ".csv")) if row["answer"]=="Yes"]

    self.train_classifier()

  #tokenize and lemmatize incoming content,
  #set up frequency distributions
  def preprocess_article(self, row, category):
    row = self.load_article(row)

    self.frequencies["content"].update(row["content_tokens"])
    self.frequencies["headline"].update(row["headline_tokens"])

    self.category_words["content"].append((row["content_tokens"], category))
    self.category_words["headline"].append((row["headline_tokens"], category))

    return row

  #for a given CSV row coming in from crowdflower, tokenize, lemmatize, remove stopwords and punct
  def load_article(self, row):
    lmtz = WordNetLemmatizer()
    p = re.compile(r'[-.?!,":;()]')  
    row["content_tokens"] = [lmtz.lemmatize(w.lower()) for w in nltk.wordpunct_tokenize(row["content"]) 
                              if (not w in stopwords.words('english') and not p.search(w))]
    row["headline_tokens"] = [lmtz.lemmatize(w.lower()) for w in nltk.wordpunct_tokenize(row["headline"])
                              if (not w in stopwords.words('english') and not p.search(w))]
    return row

  #train a naive bayesian classifier on the training set
  #TODO: Include headlines, not just content
  def train_classifier(self):
    self.classifier = nltk.NaiveBayesClassifier.train(
                        nltk.classify.util.apply_features(
                          self.extract_content_features, 
                          self.category_words["content"]))

  def extract_headline_features(self, wordlist):
    return self.extract_features(wordlist, "headline")

  def extract_content_features(self, wordlist):
    return self.extract_features(wordlist, "content")

  def extract_features(self, wordlist, field_name):
    words = set(wordlist)
    features = {}
    for word in self.frequencies[field_name].keys():
      features['%s_contains(%s)' %(field_name, word)] = (word in words)
    return features

  #load evaluation dataset
  def setup_evaluation(self, folder):
    self.eval_categories = {"sports":None, "local":None}
    for category in self.eval_categories:
      self.eval_categories[category] = {}
      self.eval_categories[category]["documents"] = [self.load_article(row) 
        for row in csv.DictReader(open(folder + category + ".csv", "rb")) if row["answer"]=="Yes"]
