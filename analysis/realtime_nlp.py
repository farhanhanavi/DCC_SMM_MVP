import requests as req
import pandas as pd


'''
Untuk merubah full response dari GET Twitter menjadi lists of string [tweet_string]
Merubah list of strings menjadi list of insights [real_time]
'''


#GET LIST OF STRINGS FROM RESPONSE
def tweet_string(response, full_result=False):

    print(response)

    #Tweet container
    tweet_id = []
    tweets = []
    screen_name = []
    user_verified = []
    user_pp = []
    tweet_date = [] 
    tweet_quote_count = []
    tweet_reply_count = []
    tweet_retweet_count = []
    tweet_favorite_count = []


    #Get tweet
    for i in response['results']:
        if i.get('extended_tweet'):
            tweets.append(i['extended_tweet']['full_text'])
        else:
            tweets.append(i['text'])


    if full_result == True:
        for i in response['results']:

            #Get tweet_id
            tweet_id.append(i['id'])

            #Get screen name
            screen_name.append(i['user']['screen_name'])

            #Get verified Status
            if i['user']['verified']:
                user_verified.append('Yes')
            else:
                user_verified.append('No')

            #Get profile picture
            user_pp.append(i['user']['profile_image_url_https'])

            #Get Tweet Date
            tweet_date.append(i['created_at'])

            #Get retweets
            tweet_quote_count.append(i['quote_count'])
            tweet_reply_count.append(i['reply_count'])
            tweet_retweet_count.append(i['retweet_count'])
            tweet_favorite_count.append(i['favorite_count'])

            

        return  {'tweet_id':tweet_id,
                'tweet': tweets, 
                'screen_name':screen_name, 
                'user_verified':user_verified,
                'user_pp':user_pp, 
                'tweet_date':tweet_date, 
                'tweet_quote_count': tweet_quote_count, 
                'tweet_reply_count':tweet_reply_count,
                'tweet_retweet_count': tweet_retweet_count, 
                'tweet_favorite_count': tweet_favorite_count}

    return tweets

    

    
    

#SEND TO WATSON
def real_time(list_of_strings):

    #Get Watson Default URL
    url = 'http://78.46.195.24:8393/api/v10/analysis/text/?'

    #Container
    all_result = []

    #Iterate in each string
    for string in list_of_strings:
        
        #Container
        insight_dict = {'nama':[], 'organisasi':[], 'insight_keyword':[], 'sentiment':[]}
        
        #PARAMS
        params = {
            'collection':'col_31538',
            'text':string,
            'output':'application/json',
            'language':'id'
        }
        
        #Get Response
        response = req.get(url, params=params, auth=('esadmin','P@ssw0rd')).json()
        response = response['metadata']['textfacets']
        
        for i in response:
            if (i['path'][0] == 'insight'):
                insight_dict[i['path'][1]].append(i['keyword'])
            elif (i['path'][0] == '_word' and i['path'][1] == 'adj'):
                insight_dict['insight_keyword'].append(i['keyword'])
            elif (i['path'][0] == '$view'):
                insight_dict['sentiment'].append(i['keyword'])
            
        all_result.append(insight_dict)

    return all_result
        