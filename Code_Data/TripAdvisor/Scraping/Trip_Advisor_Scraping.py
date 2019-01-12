# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 13:10:27 2018

@author: Lenovo
"""
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import re

urls_guid=["g294265-d1770798","g294265-d302109","g294265-d1086295","g294265-d2226820","g294265-d1239596"]
urls_hn=["Marina_Bay_Sands-Singapore","Shangri_La_Hotel_Singapore-Singapore","Crowne_Plaza_Changi_Airport-Singapore","Oasia_Hotel_Novena_Singapore_by_Far_East_Hospitality-Singapore","Park_Hotel_Clarke_Quay-Singapore"]
hotel_names=["Marina Bay Sands","Shangri-La Hotel, Singapore","Crowne Plaza Changi Airport","Oasia Hotel Novena, Singapore by Far East Hospitality","Park Hotel Clarke Quay"]



def dataIngestReview(data):
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.hotels
    collection = db.tripadvisor_reviews
    collection.insert_many(data)
    return

def dataIngestUserInfo(data):
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.hotels
    collection = db.tripadvisor_users
    collection.insert_many(data)
    return

def iterationfunction(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    reviews_container=soup.find(id='REVIEWS')
    for review in reviews_container.find_all(class_='review-container'):
        if(review.find(class_='noQuotes')):
            review_title = review.find(class_='noQuotes')
            review_title = review_title.text.strip()
            review_title = str.replace(review_title,'\n','')
            review_title_list.append(review_title)
            #global review_subject_word_cloud
            #review_subject_word_cloud = review_subject_word_cloud+" "+review_title.strip()
        else:review_title_list.append("NA")
        
        if(review.find(class_='partial_entry')):
            review_text = review.find(class_='partial_entry')
            review_text = review_text.text.strip()
            review_text = str.replace(review_text,'\n','')
            review_text = str.replace(review_text,'...More','')
            review_text_list.append(review_text)
            #global review_word_cloud
            #review_word_cloud = review_word_cloud+" "+review_text.strip()
        else: review_text_list.append('NA')
        
        if(review.find(class_='viaMobile')):
            review_mode = review.find(class_='viaMobile')
            review_mode = review_mode.text.strip()
            review_mode = str.replace(review_mode,'\n','')
            review_mode_list.append(review_mode)
        else: review_mode_list.append('NA')
        
        if(review.find(class_='ratingDate')):
            review_date = review.find(class_='ratingDate')
            review_date = review_date['title'].strip()
            review_date = str.replace(review_date,'\n','')
            review_date_list.append(review_date)
        else: review_date_list.append('NA')
        
        if(review.find(class_='numHelp emphasizeWithColor')):
            thank_user = review.find(class_='numHelp emphasizeWithColor')
            thank_user = thank_user.text.strip()
            thank_user = str.replace(thank_user,'\n','')
            thank_user_list.append(thank_user)
        else: thank_user_list.append('NA')
        
        if(review.find(class_='userLoc')):
            user_loc=review.find(class_='userLoc')
            user_loc=user_loc.text.strip()
            user_loc=str.replace(user_loc,'\n','')
            user_loc_list.append(user_loc)
        else:user_loc_list.append('NA')
        
        span_tags=review.find_all('span')
        for span_tag in span_tags:
            if 'ui_bubble_rating' in span_tag['class']:
                review_rating=span_tag['class'][1]
                review_rating=review_rating[7:-1]+" stars"
                review_rating_list.append(review_rating)
                break
        
        member = review.find('div',{'class':'memberOverlayLink'})
        
        if(member):
            empty, uid, src = re.split('UID...|-|-SRC_',member['id'])
            #username = member.find("div",class_='username')
            #username = username.text.strip()
            
            uu = member['id']
            userid = uu.split("-")[0]
            userid = userid.split("_")[1]
            
            
            src_number=src.split("_")[1]
            
            
            url2 = "https://www.tripadvisor.com.sg/MemberOverlay?Mode=owa&uid="+str(userid)+"&c=&src="+str(src_number)+"&fus=false&partner=false&LsoId=&metaReferer=Hotel_Review"
            response = requests.get(url2)
            
            
            overlay = BeautifulSoup(response.content, "html.parser")
            
            if(overlay.find(class_='username reviewsEnhancements')):
                user_name = overlay.find(class_='username reviewsEnhancements')
                user_name = user_name.text.strip()
                user_name = str.replace(user_name,'\n','')
                user_name_list.append(user_name)
            else: user_name_list.append('NA')
            
            if(overlay.find('li')):
                
                member_since = overlay.find('li')
                member_since = member_since.text.strip()
                member_since = str.replace(member_since,'\n','')
                member_since_list.append(member_since)
            else: member_since_list.append('NA')
            
            if(overlay.find(class_='badgeinfo')):
                badge_info=overlay.find(class_='badgeinfo')
                badge_info=badge_info.text.strip()
                badge_info= str.replace(badge_info,'\n','')
                badge_info_list.append(badge_info)
            else:badge_info_list.append('NA')
            
            if(overlay.find(class_='countsReviewEnhancementsItem')):
                user_info_li_count =len( overlay.find_all(class_='countsReviewEnhancementsItem'))
                user_info_li =overlay.find_all(class_='countsReviewEnhancementsItem')
                if(user_info_li_count>=1):
                    member_contribution = user_info_li[0].text.strip()
                    member_contribution = str.replace(member_contribution,'\n','')
                    if("Contribution" in member_contribution):
                        member_contribution_list.append(member_contribution)
                    else:member_contribution_list.append('NA')
                else:member_contribution_list.append('NA')
                if(user_info_li_count>=2):
                    cities_visited=user_info_li[1].text.strip()
                    cities_visited=str.replace(cities_visited,'\n','')
                    if("visited" in cities_visited):
                        cities_visited_list.append(cities_visited)
                    else:cities_visited_list.append('NA')
                else:cities_visited_list.append('NA')
                if(user_info_li_count>=3):
                    helpful_votes=user_info_li[2].text.strip()
                    helpful_votes=str.replace(helpful_votes,'\n','')
                    if("vote" in helpful_votes):
                        helpful_votes_list.append(helpful_votes)
                    else:helpful_votes_list.append('NA')
                else:helpful_votes_list.append('NA')
            else: 
                member_contribution_list.append('NA')
                cities_visited_list.append('NA')
                helpful_votes_list.append('NA')
        else:
            user_name_list.append('NA')
            member_since_list.append('NA')
            member_contribution_list.append('NA')
            cities_visited_list.append('NA')
            helpful_votes_list.append('NA')
            badge_info_list.append('NA')
        
for c in range(len(urls_guid)):
    review_title_list=[]
    review_text_list=[]
    review_mode_list=[]
    review_date_list=[]
    review_sentiment_list=[]
    review_rating_list=[]
    member_since_list=[]
    thank_user_list=[]
    member_contribution_list=[]
    cities_visited_list=[]
    helpful_votes_list=[]
    badge_info_list=[]
    user_name_list=[]
    user_loc_list=[]
    final_review_data_list=[]
    user_data_list=[]
    cloudlist = []

    url="https://www.tripadvisor.com.sg/Hotel_Review-"+urls_guid[c]+"-Reviews-"+urls_hn[c]+".html"
    iterationfunction(url)
    count = 5
    for i in range(600):
        url2 = ("https://www.tripadvisor.com.sg/Hotel_Review-"+urls_guid[c]+"-Reviews-or"+str(count)+"-"+urls_hn[c]+".html")
        iterationfunction(url2)
        count = count + 5
    
    for rev in range(len(review_title_list)):
        wiki = TextBlob(review_title_list[rev].strip())
        #print(wiki.sentiment.polarity)
        if(wiki.sentiment.polarity > -0.4 and wiki.sentiment.polarity < 0.3):
            review_sentiment_list.append("Neutral")
        elif(wiki.sentiment.polarity >= 0.3 ):
            review_sentiment_list.append("Positive")
        else: review_sentiment_list.append("Negative")
    
    for i in range(count-5):
    
        user_data={'user_name_list':user_name_list[i],
                   'user_loc_list':user_loc_list[i],
                   'badge_info_list':badge_info_list[i],
                   'cities_visited_list':cities_visited_list[i],
                   'helpful_votes_list':helpful_votes_list[i],
                   'member_contribution_list':member_contribution_list[i],
                   'member_since_list':member_since_list[i]
                   }
        review_data={
                'Hotel_name':hotel_names[c],
                'review_date_list':review_date_list[i],
                'review_mode_list':review_mode_list[i],
                'review_rating_list':review_rating_list[i],
                'review_sentiment_list':review_sentiment_list[i],
                'review_text_list':review_text_list[i],
                'review_title_list':review_title_list[i],
                'thank_user_list':thank_user_list[i],
                'user_name_list':user_name_list[i] 
                }
        final_review_data_list.append(review_data)
        user_data_list.append(user_data)
    
    dataIngestReview(final_review_data_list)
    dataIngestUserInfo(user_data_list)

