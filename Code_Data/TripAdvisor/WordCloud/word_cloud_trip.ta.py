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


client = MongoClient('localhost:27017')
# creating connectioons for communicating with Mongo DB
client = MongoClient('localhost:27017')
db = client.hotels
mand_review = db.tripadvisor_reviews.find()
for review in mand_review:
    review_sentiment_list.append(review['review_sentiment_list'])
    review_text_list.append(review['review_text_list'])
    review_title_list.append(review['review_title_list'])
#re=[]    
#review_user=db.users_ta.find()
#pipe=[{'$group': {'_id': '$member_since_list', 'total': {'$sum': 1}}}]
#re=list(db.users_ta.aggregate(pipeline=pipe))
#print(re)
#
#plt.hist([re[1]], color = 'blue', edgecolor = 'black',
#         bins = int(180/5))

#plt.title('Histogram of Arrival Delays')
#plt.xlabel('Delay (min)')
#plt.ylabel('Flights')

# function to read records from mongo db

for i in range(len(review_sentiment_list)):
    index = ""
    if(review_sentiment_list[i] == "Positive" or review_sentiment_list[i] == "Neutral"):
        #global review_positive_cloud
        review_positive_cloud = review_positive_cloud+" "+review_text_list[i]
        #global review_subject_positive_cloud
        review_subject_positive_cloud = review_subject_positive_cloud+" "+review_title_list[i]
    elif(review_sentiment_list[i] == "Negative"):
        #global review_negative_cloud
        review_negative_cloud = review_negative_cloud+" "+review_text_list[i]
        #global review_subject_negative_cloud
        review_subject_negative_cloud = review_subject_negative_cloud+" "+review_title_list[i]
        
        

import numpy as np # linear algebra
import pandas as pd 
import matplotlib as mpl
import matplotlib.pyplot as plt
from subprocess import check_output
from wordcloud import WordCloud, STOPWORDS

mpl.rcParams['font.size']=12                #10 
mpl.rcParams['savefig.dpi']=100             #72 
mpl.rcParams['figure.subplot.bottom']=.1 


stopwords = set(STOPWORDS)

wordcloud_positive = WordCloud(
                          background_color='white',
                          stopwords=stopwords,
                          max_words=200,
                          max_font_size=40, 
                          random_state=42
                         ).generate(str(review_subject_positive_cloud.strip()))

wordcloud_negative = WordCloud(
                          background_color='white',
                          stopwords=stopwords,
                          max_words=200,
                          max_font_size=40, 
                          random_state=42
                         ).generate(str(review_subject_negative_cloud.strip()))



fig_postive = plt.figure(1)
plt.imshow(wordcloud_positive)
plt.axis('off')
plt.show()
fig_postive.savefig("C:\\Users\\Lenovo\\Downloads\\cloud.png", dpi=900)

fig_negative = plt.figure(1)
plt.imshow(wordcloud_negative)
plt.axis('off')
plt.show()
fig_negative.savefig("C:\\Users\\Lenovo\\Downloads\\cloud.png", dpi=900)



