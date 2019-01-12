# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 09:29:20 2018

@author: Lenovo
"""
from pymongo import MongoClient
import matplotlib.pyplot as plt

review_sentiment_list=[]
review_text_list=[]
review_title_list=[]
review_word_cloud = ""
review_subject_word_cloud = ""
review_positive_cloud = ""
review_negative_cloud = ""
review_subject_positive_cloud = ""
review_subject_negative_cloud = ""
review_negative_freq_list=[]
review_positive_freq_list=[]

client = MongoClient('localhost:27017')
# creating connectioons for communicating with Mongo DB
client = MongoClient('localhost:27017')
db = client.test
mand_review = db.yelp_review_details.find()
for review in mand_review:
    review_sentiment_list.append(review['Sentiment'])
    review_text_list.extend(review['pre_processed_review'])
    #review_title_list.append(review['review_title_list'])
#re=[]    
# function to read records from mongo db

for i in range(len(review_sentiment_list)):
    index = ""
    if(review_sentiment_list[i] == "Positive" or review_sentiment_list[i] == "Neutral"):
        #global review_positive_cloud
        review_positive_cloud = review_positive_cloud+" "+review_text_list[i]
        review_positive_freq_list.append(review_text_list[i])
        #global review_subject_positive_cloud
        #review_subject_positive_cloud = review_subject_positive_cloud+" "+review_title_list[i]
    elif(review_sentiment_list[i] == "Negative"):
        #global review_negative_cloud
        review_negative_cloud = review_negative_cloud+" "+review_text_list[i]
        review_negative_freq_list.append(review_text_list[i])
        #global review_subject_negative_cloud
        #review_subject_negative_cloud = review_subject_negative_cloud+" "+review_title_list[i]
        
        

import numpy as np # linear algebra
import pandas as pd 
import matplotlib as mpl
import matplotlib.pyplot as plt
from subprocess import check_output
from wordcloud import WordCloud
#, STOPWORDS
from nltk.corpus import stopwords

mpl.rcParams['font.size']=12                #10 
mpl.rcParams['savefig.dpi']=100             #72 
mpl.rcParams['figure.subplot.bottom']=.1 


#stopwords = set(STOPWORDS)

stopwords = set(stopwords.words('english'))
stopwords.add('&')
stopwords.add("'ve")
stopwords.add("l")
stopwords.add('without')
stopwords.add("'m")
stopwords.add("n't")


wordcloud_positive = WordCloud(
                          background_color='white',
                          stopwords=stopwords,
                          max_words=200,
                          max_font_size=40, 
                          random_state=42
                         ).generate(str(review_positive_cloud.strip()))

wordcloud_negative = WordCloud(
                          background_color='white',
                          stopwords=stopwords,
                          max_words=200,
                          max_font_size=40, 
                          random_state=42
                         ).generate(str(review_negative_cloud.strip()))



fig_postive = plt.figure(1)
plt.imshow(wordcloud_positive)
plt.axis('off')
plt.show()
fig_postive.savefig("C:\\Users\\RajBharat\\Downloads\\cloud+ve.png", dpi=900)

fig_negative = plt.figure(1)
plt.imshow(wordcloud_negative)
plt.axis('off')
plt.show()
fig_negative.savefig("C:\\Users\\RajBharat\\Downloads\\cloud-ve.png", dpi=900)

from nltk.probability import FreqDist

positive_word_fc = [w for w in review_positive_freq_list if not w in stopwords]
fc_freq = FreqDist(positive_word_fc)
fd=fc_freq.plot(30)
#plt.imshow(fd)
##plt.axis('off')
##plt.show()
##fd.savefig("C:\\Users\\RajBharat\\Downloads\\fd+ve.png", dpi=900)


negative_word_fc = [w for w in review_negative_freq_list if not w in stopwords]
fd_freq = FreqDist(negative_word_fc)
fe=fd_freq.plot(30)
#plt.imshow(fe)
##plt.axis('off')
##plt.show()
##fe.savefig("C:\\Users\\RajBharat\\Downloads\\fe-ve.png", dpi=900)
##

