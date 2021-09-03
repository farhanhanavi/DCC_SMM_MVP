from analysis.get_tweets import get_tweets                   #GET twitter data
from analysis.realtime_nlp import tweet_string, real_time   


'''
Finalize from analysis folder
'''

def convert_tweets(response_json):

    #Get response from Twitter 
    response = get_tweets(response_json)

    #Get analysis for each string
    #Get strings in each response
    strings = tweet_string(response, full_result=False)
    #Get analysis result
    analysis = real_time(strings)

    #Get all twitter data
    all_data = tweet_string(response, full_result=True)
    all_data['insight'] = analysis



    #Return
    return all_data