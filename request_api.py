import requests

BASE = "http://127.0.0.1:5000/"

response = requests.post(
    BASE + "tool/video", {"tweet_url": "https://twitter.com/tinaqueen_15/status/1469709115144478729?s=20&t=WmrW8R5mDRT-hm83AJRakA", "watermark": "finesstv", "email": "teamfinesstv@gmail.com"})

# print(response.json())
