import tweepy
import openai
import requests
from bs4 import BeautifulSoup

# Set up Twitter API keys
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_secret = 'YOUR_ACCESS_SECRET'

# Set up OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# Read tweet dataset from a text file named 'AllTimeHits.txt'
with open('AllTimeHits.txt', 'r') as file:
    raw_tweets = file.read().split('\n\n')

# Separate raw_tweets into individual multi-line tweets
tweets_dataset = [tweet.replace('\n', ' ') for tweet in raw_tweets]

# Prompt for a URL link
article_url = input("Enter the URL of the article: ")

# Fetch article content from the URL
response = requests.get(article_url)
soup = BeautifulSoup(response.content, 'html.parser')
article_content = soup.get_text()

# Define the prompt
prompt = "Write the post to inspire and educate developers and crypto/blockchain enthusiasts in a technical but relatable way:\n\n"

# Train the language model using the prompt, tweets dataset, and article content
training_data = prompt + "\n".join(tweets_dataset) + "\n" + article_content
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=training_data,
    max_tokens=150,
    temperature=0.7
)

# Generate a new tweet using the trained model
new_tweet = response.choices[0].text.strip()

# Post the generated tweet on Twitter
api.update_status(new_tweet)
print("Tweet posted:", new_tweet)
