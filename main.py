import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = 'M31RIST54Y9K6824'
NEWS_API_KEY = '39709398305945eb818f723ec48de585'
TWILIO_SID = 'AC19a08ecffde25e6720eb9152fbbd304e'
TWILIO_AUTH_TOKEN = 'beac24a4cec304348641875f9edd521b'

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
#TODO 2. - Get the day before yesterday's closing stock price

stock_params = {
    'function':'TIME_SERIES_WEEKLY',
    'symbol': STOCK_NAME,
    'interval':'1min',
    'apikey':STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT,params=stock_params)
stocks_data = response.json()
stocks_data1 = response.json()['Weekly Time Series']
# print(stocks_data)
# print('=======')
# print(stocks_data1)
# stocks_data_meta = response.json()['Meta Data']
# print(stocks_data_meta)

# data_list = [new_item for item in list] -> keyword for a list comprehension
# but we are dealing with a dictionary so we use the keyword below to create a list so we can use the index of each item instead of the key which is a date that changes everytime, this will be hard coded everytime because the date changes everyday, unlike the list which we will use to have 0 and 1 as our target data everytime, we are interested only in the value from the dictionary
# data_list_key = [key for(key,value) in stocks_data1.items()]
# print(data_list_key)
data_list_value = [value for(key,value) in stocks_data1.items()]
# print(data_list_value)

# last week's data
print(data_list_value[0])
# data from two weeks ago
print(data_list_value[1])

# from the two dictionaries above, we need to compare the closing value for each, which means that we are interested in the value of the key:'4. close'

last_week_close_value = data_list_value[0]['4. close']
print(last_week_close_value)

two_weeks_close_value =  data_list_value[1]['4. close']
print(two_weeks_close_value)


#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp

diff_closing_value = abs(float(last_week_close_value) - float(two_weeks_close_value))
print(diff_closing_value)

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

percent_diff = (diff_closing_value / float(last_week_close_value)) * 100
print(percent_diff)

#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
## STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if percent_diff > 0.3:
    news_params = {
        'apiKey': NEWS_API_KEY,
        'qInTitle': COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT,params=news_params)
    articles = news_response.json()['articles'][:3]
    print(articles)
    print(type(articles))

    # [new_item for item in list]
    article_list = [f"Title: {article['title']} Description: {article['description']}" for article in articles]
    print(article_list)

    # print(news_response.json())
    # print('====')
    # print(news_response.json()['articles'])
    # print('====')
    # print(type(news_response.json()))
    # print(len(news_response.json()))
    # print(news_response.json()['articles'][0])
    # print('====')
    # print(news_response.json()['articles'][1])
    # print('====')
    # print(news_response.json()['articles'][2])

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for artikulo in article_list:
        message = client.messages \
            .create(
            body=artikulo,
            from_='+14066292641',
            to='+639282022640'
        )

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation


## STEP 3: Use twilio.com/docs/sms/quickstart/python
#to send a separate message with each article's title and description to your phone number.

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

#TODO 9. - Send each article as a separate message via Twilio. 



#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
