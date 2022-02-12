import requests

BASE = "http://127.0.0.1:5000/"

response = requests.post(
    BASE + "tool/quote", {"tweet_url": "https://twitter.com/nunidior/status/1492269225519497223?s=20&t=_iHjKWmyRIwKCYNyP-otQw", "watermark": "finesstv"})

print(response.json())
