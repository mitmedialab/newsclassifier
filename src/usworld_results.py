import csv
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import random

class USWorldResults:
  def __init__(self, folder, category_list):
    #["sports", "local", "arts_entertainment", "usnational", "non_us_foreign", "us_foreign"]:
    self.categories = {}
    for category in category_list: 
      self.categories[category] = None

    self.category_words = []
    self.frequency=nltk.FreqDist()

    for category in self.categories:
      self.categories[category] = {}
      self.categories[category]["documents"] = [self.preprocess_article(row, category) 
        for row in csv.DictReader(open(folder + category + ".csv")) if row["answer"]=="Yes"]

    self.train_classifier()


  @staticmethod
  def create_training_test_datasets(input_folder, output_base_folder, category_list):
    training = {}
    evaluation = {}
    for category in category_list: #["sports", "local", "arts_entertainment", "usnational", "non_us_foreign", "us_foreign"]:
      docs = [row for row in csv.DictReader(open(input_folder + category + ".csv")) if row["answer"]=="Yes"]
      random.shuffle(docs)
      
      length = len(docs)
      cutoff = length * 3/4
      dict_writer = csv.DictWriter(open(output_base_folder + "evaluation/" + category + ".csv", "wb"), docs[0].keys())
      dict_writer.writer.writerow(docs[0].keys())
      dict_writer.writerows(docs[cutoff:])

      dict_writer = csv.DictWriter(open(output_base_folder + "training/" + category + ".csv", "wb"), docs[0].keys())
      dict_writer.writer.writerow(docs[0].keys())
      dict_writer.writerows(docs[:cutoff])



  #tokenize and lemmatize incoming content,
  #set up frequency distributions
  def preprocess_article(self, row, category):
    row = self.load_article(row)
    if(len(row["content_tokens"])>0):
      self.frequency.update(row["content_tokens"])
      self.category_words.append((row["content_tokens"], category))

    return row

  #for a given CSV row coming in from crowdflower, tokenize, lemmatize, remove stopwords and punct
  def load_article(self, row):
    lmtz = PorterStemmer()
    p = re.compile(r'[-.?!,":;()]')  
    row["content_tokens"] = [lmtz.stem(w.lower()) for w in nltk.wordpunct_tokenize(row["content"]) 
                              if (not w in stopwords.words('english') and not p.search(w))]
    return row

  #train a naive bayesian classifier on the training set
  def train_classifier(self):
    self.classifier = nltk.NaiveBayesClassifier.train(
                        nltk.classify.util.apply_features(
                          self.extract_features, 
                          self.category_words))

  def extract_features(self, wordlist):
    words = set(wordlist)
    features = {}
    for word in self.frequency.keys():
      #features['%s_contains(%s)' %(field_name, word)] = (word in words)
      if(word in words):
        features['contains(%s)' %(word)] = True#(word in words)
    return features

  #load evaluation dataset
  def setup_evaluation(self, folder):
    self.eval_categories = {}
    for category in self.categories:
      self.eval_categories[category] = {}
      self.eval_categories[category]["documents"] = [self.load_article(row) 
        for row in csv.DictReader(open(folder + category + ".csv", "rb")) if row["answer"]=="Yes"]
