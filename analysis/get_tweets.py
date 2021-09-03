import requests as request
import json
import pandas as pd 


'''
Untuk GET dari twitter berdasarkan input dari user
'''



def get_tweets(json):

    #Add variables
    query       = json['query']
    fromDate    = json['fromDate']
    todate      = json['toDate']
    maxResults  = 10
    lang        = 'in'
    result_type = 'popular'

    #Convert to UTC

    #Request to twitter
    headers = {"Authorization":"Bearer AAAAAAAAAAAAAAAAAAAAAEnVRAEAAAAARMhBLKXrx5MdAQnNkEYbEXmv34U%3DyW8fgHyI835ociNQb9r2F4Upri455siDC3BgX76SY0zpeFp5aG", "Content-Type": "application/json"} 
    url = f'https://api.twitter.com/1.1/tweets/search/30day/premiumenvironment.json?query={query}?result_type={result_type}?lang={lang}&fromDate={fromDate}&toDate={todate}&maxResults={maxResults}'
    response = request.get(url, headers=headers)
    response = response.json()

    #Pagination

    return response



