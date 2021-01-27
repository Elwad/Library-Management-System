#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 14:22:53 2021

@author: elwadgedleh

Detect positive and negative reviews by creating model 
which processes text and predicts sentiment
"""
import spacy 
import random
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from spacy.util import minibatch


                            #Load/Split Data Version #1

#Load data from csv file 
#-----reviews_file_path = '/Users/elwadgedleh/Downloads/Womens Clothing E-Commerce Reviews.csv'

#Read data, use column already in data as index 
#-----reviews_file = pd.read_csv(reviews_file_path, index_col=0) 

#Drop any empty reviews (4%)
#-----reviews_file = reviews_file[reviews_file['Review Text'].notnull()]

#select feature data (reviews)
#-----text = reviews_file.loc[:, 'Review Text']          

#select y data, i.e., target data (Recommended)
#-----y = reviews_file.loc[:,'Recommended IND']
                      

#create a dict of boolean values for all target values. This will be used for model
#-----labels = [{"POSITIVE": bool(i), "NEGATIVE": not bool(i)} for i in y]
#-----split = int(len(reviews_file)*0.8)

#Apply labels on training data (80%)
#-----train_labels= [{"cats": labels} for labels in labels[:split]]
#Apply labels on validation/testing data (20%)
#-----val_labels= [{"cats": labels} for labels in labels[split:]]

#Divide into train & test data 
#-----text_train= text[:split]  
#-----y_train= y[:split]   
#-----text_test= text[split:]  
#-----y_test= y[split:]        
#-----print("Train Labels", len(train_labels))
#-----print("Val Labels", len(val_labels))
#-----print("Train Text", len(text_train))
#-----print("Train Test", len(text_test))



                           #Load/Split Data Version #2
                           
#Load data from csv file 
reviews_file_path = '/Users/elwadgedleh/Downloads/Womens Clothing E-Commerce Reviews.csv'                          

#Read data, use column already in data as index 
reviews_file = pd.read_csv(reviews_file_path, index_col=0) 

#Drop any empty reviews (4%)
reviews_file = reviews_file[reviews_file['Review Text'].notnull()]

#select feature data (reviews)
text = reviews_file.loc[:, 'Review Text']          

#select y data, i.e., target data (Recommended)
y = reviews_file.loc[:,'Recommended IND']

#Divide into train & test data
text_train, text_test, y_train, y_test = train_test_split(text, y, test_size=0.20, random_state=None, shuffle=False)

labels = [{"POSITIVE": bool(i), "NEGATIVE": not bool(i)} for i in y]


#TRAIN LABELS 
#Convert labels to form TextCategorizer model requires
#Apply labels on training data (80%) 
train_labels= [{"cats": labels} for labels in labels[:(len(text_train))]]
#Apply labels on validation/testing data (20%)
val_labels= [{"cats": labels} for labels in labels[(len(text_train)):]]

print("Train Labels", len(train_labels))
print("Val Labels", len(val_labels))
print("Train Text", len(text_train))
print("Train Test", len(text_test))


print('Texts from training data\n------')
print(text_train[:15])
print('\nLabels from training data\n------')
print(train_labels[:15])


                                    #Build BOW Model 

# (1) Vectorize text using BOW representation 
#TextCategorizer is a pipe, vectorizes text. Pipes process + transform tokens.

# Create empty model, add TextCategorizer Pipe
nlp = spacy.blank('en')
textCateg = nlp.create_pipe("textcat", 
                           config={"exclusive_classes": True,
                                   "architecture" : "bow" })
# Add text categorizer to empty model 
nlp.add_pipe(textCateg)

# ALTERNATIVE: Load in spacy model - English. Contains default pipes.
#----! nlp = spacy.load('en_core_web_sm')

# Add labels to text classifier 
textCateg.add_label("NEGATIVE")  #0-> Negative
textCateg.add_label("POSITIVE")  #1 -> Positive


random.seed(1)
spacy.util.fix_random_seed(1)

#TRAIN MODEL 
# Create optimizer, used to update model 
optimizer = nlp.begin_training() 

#Create empty dict, will be updated w/ losses 
losses = {}

# Zip/combine training text + training labels into single list. Batch generator 
# will go thru each list to extract a batch. (i.e., each batch = list)
iterable = list(zip(text_train, train_labels))


#epoch = training loop, train model in 10 loops of batches thru the data
for epoch in range(10): 
    # shuffle the data (optional)
    random.shuffle(iterable)
# Training in small batches, minibatch function returns small batches for training:
    # 2) Create batch generator 
batches = minibatch(iterable, size = 8)
    # 3) Generator returns batch (i.e., list of text & its label)
for batch in batches:
    #split batch into text and label
    texts, labels = zip(*batch)
    # 4) Update model parameters 
    # sgd updates models weight, losses is a dictionary to update w/ the loss  
    nlp.update(texts, labels, sgd = optimizer, losses= losses )


#nlp.update() updates the model after each loop. It goes through each word of the input and 
# makes a prediction. Then it consults annotations to see if its right. If its WRONG it 
# adjusts the weight so that the next action will score higher next time 


                                # Predict using BOW Model 
#Predict using validation text : text_test, get accuracy by comparing to acc results (y_test)

#Tokenize val text
val_text = [nlp.tokenizer(text) for text in text_test] 

textCateg = nlp.get_pipe('textcat')
scores, _ = textCateg.predict(val_text)

#Find predictions with highest prob of accuracy and print
highestPred = scores.argmax(axis=1)
#--------! print([textCateg.labels[label] for label in highestPred]) 
#--------! for p, t in zip(highestPred, val_text):
#--------!     print(f" {textCateg.labels[p]}: {t} \n")
    
                              # Accuracy Of BOW Model
#predict results: returns list of int model assigned to val_text where 1 is a review predicted
# to be positive, and 0 is negative
predict_val = highestPred
# Acc results: convert acc labels into list of integers (POSITIVE -> 1, NEGATIVE -> 0)
acc_results = [int(each['cats']['POSITIVE']) for each in val_labels]                   
# store correct predictions
correct_pred = predict_val == acc_results
#divide correct predictions by total predictions to see accuracy (i.e., mean)   
accuracy= correct_pred.mean()
print("Accuracy of BOW:", accuracy)



                           #Build Logistic Regression Model
# 1) Vectorize
#Take the words of each sentence and create vocab of all unique words in sentence 
vectorizer = CountVectorizer(min_df=0, lowercase=True)
vectorizer.fit(text_train)
X_train = vectorizer.transform(text_train)
X_test = vectorizer.transform(text_test)
                                        
# 2) Create model, fit with training data                              
classifier= LogisticRegression(max_iter=10000)
classifier.fit(X_train,y_train)
score = classifier.score(X_test,y_test)
print("Accuracy of LR:", score)


                           



