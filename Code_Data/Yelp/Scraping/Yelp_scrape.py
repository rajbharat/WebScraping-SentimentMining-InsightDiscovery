#Importing all libraries
import requests
from bs4 import BeautifulSoup
import csv
import collections
import re
import nltk
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#From Github; how to replace and expand contactions

cList = {
  "ain't": "am not",
  "aren't": "are not",
  "can't": "cannot",
  "can't've": "cannot have",
  "'cause": "because",
  "could've": "could have",
  "couldn't": "could not",
  "couldn't've": "could not have",
  "didn't": "did not",
  "doesn't": "does not",
  "don't": "do not",
  "hadn't": "had not",
  "hadn't've": "had not have",
  "hasn't": "has not",
  "haven't": "have not",
  "he'd": "he would",
  "he'd've": "he would have",
  "he'll": "he will",
  "he'll've": "he will have",
  "he's": "he is",
  "how'd": "how did",
  "how'd'y": "how do you",
  "how'll": "how will",
  "how's": "how is",
  "I'd": "I would",
  "I'd've": "I would have",
  "I'll": "I will",
  "I'll've": "I will have",
  "I'm": "I am",
  "I've": "I have",
  "isn't": "is not",
  "it'd": "it had",
  "it'd've": "it would have",
  "it'll": "it will",
  "it'll've": "it will have",
  "it's": "it is",
  "let's": "let us",
  "ma'am": "madam",
  "mayn't": "may not",
  "might've": "might have",
  "mightn't": "might not",
  "mightn't've": "might not have",
  "must've": "must have",
  "mustn't": "must not",
  "mustn't've": "must not have",
  "needn't": "need not",
  "needn't've": "need not have",
  "o'clock": "of the clock",
  "oughtn't": "ought not",
  "oughtn't've": "ought not have",
  "shan't": "shall not",
  "sha'n't": "shall not",
  "shan't've": "shall not have",
  "she'd": "she would",
  "she'd've": "she would have",
  "she'll": "she will",
  "she'll've": "she will have",
  "she's": "she is",
  "should've": "should have",
  "shouldn't": "should not",
  "shouldn't've": "should not have",
  "so've": "so have",
  "so's": "so is",
  "that'd": "that would",
  "that'd've": "that would have",
  "that's": "that is",
  "there'd": "there had",
  "there'd've": "there would have",
  "there's": "there is",
  "they'd": "they would",
  "they'd've": "they would have",
  "they'll": "they will",
  "they'll've": "they will have",
  "they're": "they are",
  "they've": "they have",
  "to've": "to have",
  "wasn't": "was not",
  "we'd": "we had",
  "we'd've": "we would have",
  "we'll": "we will",
  "we'll've": "we will have",
  "we're": "we are",
  "we've": "we have",
  "weren't": "were not",
  "what'll": "what will",
  "what'll've": "what will have",
  "what're": "what are",
  "what's": "what is",
  "what've": "what have",
  "when's": "when is",
  "when've": "when have",
  "where'd": "where did",
  "where's": "where is",
  "where've": "where have",
  "who'll": "who will",
  "who'll've": "who will have",
  "who's": "who is",
  "who've": "who have",
  "why's": "why is",
  "why've": "why have",
  "will've": "will have",
  "won't": "will not",
  "won't've": "will not have",
  "would've": "would have",
  "wouldn't": "would not",
  "wouldn't've": "would not have",
  "y'all": "you all",
  "y'alls": "you alls",
  "y'all'd": "you all would",
  "y'all'd've": "you all would have",
  "y'all're": "you all are",
  "y'all've": "you all have",
  "you'd": "you had",
  "you'd've": "you would have",
  "you'll": "you you will",
  "you'll've": "you you will have",
  "you're": "you are",
  "you've": "you have"
}

c_re = re.compile('(%s)' % '|'.join(cList.keys()))

def expandContractions(text, c_re=c_re):
    def replace(match):
        return cList[match.group(0)]
    return c_re.sub(replace, text.lower())
       
def dataIngestReview(data):
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.test
    collection = db.yelp_review_details
    collection.insert_many(data)
    return

def dataIngestUserInfo(data):
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.test
    collection = db.yelp_user_details
    collection.insert_many(data)
    return
# In[4]:

#We will use the iteration to retrieve and scrape the web pages, reviews_list, and ratings from each page on Yelp
reviews_list = []
#ratings = [] 
int_rating_list=[]
rating_list=[]
user_name_list=[]
user_location_list=[]
is_elite_list=[]
total_user_photos_list=[]
total_user_reviews_list=[]
total_user_friends_list=[]
total_useful_upvote_list=[]
total_funny_upvote_list=[]
total_cool_upvote_list=[]
review_date_list=[]
final_review_data_list=[]
user_data_list=[]
hotel_list=[]
pre_processed_review_list=[]

#Headers will make it look like you are using a web browser
headers = {'user_info-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
#biz_entities = ['shangri-la-hotel-singapore-singapore-2','crowne-plaza-hotel-changi-airport-singapore','village-hotel-changi-singapore','oasia-hotel-novena-singapore-singapore','park-hotel-clarke-quay-singapore','marina-bay-sands-singapore-2']
biz_entities = ['marina-bay-sands-singapore-2']

for val in biz_entities:
    print (val)
    import re
    hotel_name = re.sub('[^a-zA-Z]+',' ',val)
    
    for i in range (0,250,20):
        url = 'https://www.yelp.com.sg/biz/{}?start={}'.format(val,i)
        print(url)
        print('running for {} - {}'.format(hotel_name,i))
        response = requests.get(url, headers=headers, verify=False).text
        soup = BeautifulSoup(response, "lxml")
        if (len(soup.text.strip())==0):
                print("breaking loop")
                break

        #Looping through 'div' 'review_text-content' will help find all the review_text containers we need in each page that have rating and review_text
        for s in soup.find_all("div", attrs={'class': 'review review--with-sidebar'}):

            hotel_list.append(hotel_name.strip())
            print(hotel_name.strip())
            #print("Parsing html")
            re = s.find('p', attrs={'lang': 'en'})

            #Makes all the letters lower in reviews_list
            review_text = re.text.lower()
            
            reviews_list.append(review_text)          
            
            user_info = s.find("div", attrs={'class': 'media-story'})
            name_field = user_info.find("a", attrs={'class': 'user-display-name js-analytics-click'})
            user_name= name_field.text.lower().strip() if user_info.find("a", attrs={'class': 'user-display-name js-analytics-click'}).text else ''
            user_name_list.append(user_name)

            review_date = s.find("span", attrs={'class': 'rating-qualifier'}).text.lower().strip()
            review_date_list.append(review_date)

            user_location = user_info.find("li", attrs={'class': 'user-location responsive-hidden-small'}).text.lower().strip()
            user_location_list.append( user_location)

            is_elite = user_info.find("li", attrs={'class': 'is-elite responsive-small-display-inline-block'}).text.lower().strip() if user_info.find("li", attrs={'class': 'is-elite responsive-small-display-inline-block'}) else ''
            is_elite_list.append(is_elite)

            total_user_reviews = user_info.find("li", attrs={'class': 'review-count responsive-small-display-inline-block'}).text.lower().strip() if user_info.find("li", attrs={'class': 'review-count responsive-small-display-inline-block'}) else '' 
            total_user_reviews_list.append(total_user_reviews)
            
            total_user_photos = user_info.find("li", attrs={'class': 'photo-count responsive-small-display-inline-block'}).text.lower().strip() if user_info.find("li", attrs={'class': 'photo-count responsive-small-display-inline-block'}) else '' 
            total_user_photos_list.append(total_user_photos)
            
            total_user_friends = user_info.find("li", attrs={'class': 'friend-count responsive-small-display-inline-block'}).text.lower().strip() if user_info.find("li", attrs={'class': 'friend-count responsive-small-display-inline-block'}) else '' 
            total_user_friends_list.append(total_user_friends)
            
            footer =  s.find("ul", attrs={'class': 'voting-buttons'})
            
            useful_field = footer.find("a", attrs={'class': 'ybtn ybtn--small useful js-analytics-click'})
            total_useful_upvote=useful_field.find("span", attrs={'class':'count'}).text.lower().strip() if useful_field.find("span", attrs={'class':'count'}) else ''
            total_useful_upvote_list.append(total_useful_upvote)
            
            funny_field = footer.find("a", attrs={'class': 'ybtn ybtn--small funny js-analytics-click'})
            total_funny_upvote=funny_field.find("span", attrs={'class':'count'}).text.lower().strip() if funny_field.find("span", attrs={'class':'count'}) else ''
            total_funny_upvote_list.append(total_funny_upvote)
            
            cool_field = footer.find("a", attrs={'class': 'ybtn ybtn--small cool js-analytics-click'})
            total_cool_upvote=cool_field.find("span", attrs={'class':'count'}).text.lower().strip() if cool_field.find("span", attrs={'class':'count'}) else ''
            total_cool_upvote_list.append(total_cool_upvote)
            
            #expandContractions will put the dictionary made earlier to replace the contractions in the reviews_list
            #Make sure to to run the cList dict cell or else there will be an error
            expandContractions(review_text)
            #Cleaning the lemmas or words in reviews_list now will make it easier when we start predictive modeling
            words = word_tokenize(review_text)
            words = word_tokenize(review_text.replace('\n',' '))
            clean_words = [word.lower() for word in words if word not in set(string.punctuation)]
            characters_to_remove = ["''",'``','...']
            clean_words = [word for word in clean_words if word not in set(characters_to_remove)]
            english_stops = set(stopwords.words('english'))
            clean_words = [word for word in clean_words if word not in english_stops]
            wordnet_lemmatizer = WordNetLemmatizer()
            lemma_list = [wordnet_lemmatizer.lemmatize(word) for word in clean_words]
            pre_processed_review_list.append(lemma_list)

            #Here we are using a simple control flow to recode the ratings for our model. If rating is greater than 3 positive, else negative   
            rating = s.find_all('img', attrs={'class': 'offscreen'})
            #the rating is actually an image, so we need to convert it into a string and then to an integer
            rate = str(rating)
            int_rating = int(rate[11:12])
            int_rating_list.append(int_rating)
            
            if int_rating == 1 or int_rating == 2:
                rating_text = 'Negative'
            elif int_rating == 3:
                rating_text = 'Neutral'
            elif int_rating == 4 or int_rating == 5:
                rating_text = 'Positive'
            rating_list.append(rating_text)      
    print("Hotel Name:")
    print(hotel_name)
    print(len(reviews_list))
##        print("---------------")
##        print(review_text)
##        #if user_name in "hana a.":    
##        print(int_rating)
##        print(rating)
##        print(user_name)
##        print(user_location)
##        print(is_elite)
##        print(total_user_photos)
##        print(total_user_reviews)
##        print(total_user_friends)
##        print(total_useful_upvote)
##        print(total_funny_upvote)
##        print(total_cool_upvote)
##        print(review_date)
##        print("---------------")



#Making sure the number of reviews_list and ratings match before we append them for our featureset
total_records=len(reviews_list)
x=173

for i,j in zip(range(101,total_records),range(101,total_records)):
    user_data={'_id':j+x,
               'user_name':user_name_list[i],
               'user_loc':user_location_list[i],
               'is_elite':is_elite_list[i],
               'total_user_photos':total_user_photos_list[i],
               'total_user_reviews':total_user_reviews_list[i],
               'total_user_friends':total_user_friends_list[i]
            }
    review_data={
          '_id':i+x,
          '_user_id':j+x,
          'Hotel_name':hotel_list[i],
          'int_rating':int_rating_list[i],
          'Sentiment':rating_list[i],
          'review_text':reviews_list[i],
          'review_date':review_date_list[i],
          'total_useful_upvote':total_useful_upvote_list[i],
          'total_funny_upvote':total_funny_upvote_list[i],
          'total_cool_upvote':total_cool_upvote_list[i],
          'pre_processed_review':pre_processed_review_list[i]
            }
    final_review_data_list.append(review_data)
    user_data_list.append(user_data)

print("record count")
print(len(user_data_list))
print(len(final_review_data_list))
print("mongo db inserting now..")
dataIngestReview(final_review_data_list)
dataIngestUserInfo(user_data_list)
print("after mongo insert")
