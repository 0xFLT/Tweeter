import tweepy
import openai
import requests
from bs4 import BeautifulSoup

#Twitter API keys
consumer_key = 'CONSUMER_KEY'
consumer_secret = 'CONSUMER_SECRET'
access_token = 'ACCESS_TOKEN'
access_secret = 'ACCESS_SECRET'

#OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

#Authenticate Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#Prompt for URL link
article_url = input("Enter the URL of the article: ")

#Fetch article content
response = requests.get(article_url)
soup = BeautifulSoup(response.content, 'html.parser')
article_content = soup.get_text()

#Define prompt
prompt = "Write the post to inspire and educate developers and crypto/blockchain enthusiasts in a technical but relatable way:\n\n"

#Train language model using the prompt, tweets dataset, and article content
training_data = prompt + "\n".join(tweets_dataset) + "\n" + article_content
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=training_data,
    max_tokens=150,
    temperature=0.7
)

#Generate tweet
new_tweet = response.choices[0].text.strip()

#Post generated tweet
api.update_status(new_tweet)
print("Tweet posted:", new_tweet)
