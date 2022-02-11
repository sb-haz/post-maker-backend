import requests

BASE = "http://127.0.0.1:5000/"

response = requests.post(
    BASE + "tool/quote", {"tweet_url": "twitter.com", "watermark": "finesstv", "email": "finesstv@gmail.com"})

print(response.json())
