"""
Imports
"""
from apis import twitter_api
from helpers import watermark
from helpers import constants
from tools import quote_maker


"""
Create quote image
Returns generated caption text
"""
def generate_quote(url, username):

    # Extract tweet id from url
    try:
        tweet_id = url.split('/')[-1].split('?')[0]
    except Exception as e:
        print(e)

    # Get tweet text
    # try:
    #     tweet_text, tweet_author, media_type = twitter_api.getTweetInfo(
    #         tweet_id)
    # except Exception as e:
    #     print(e)
    tweet_text = "Its the fact cant nobody talk about nobody yet they still be fkn talking"
    tweet_author = "nunidior"
    
    # Create watermark
    try:
        watermark.create_watermark(username=username,
                                   media_type="image")
    except Exception as e:
        print(e)
        
    # Convert string text to image
    # Get filepath and height
    try:
        quote_maker.generate_quote(
            text=tweet_text,
            tweet_id=tweet_id,
            username=username)
    except Exception as e:
        print(e)

    # Return caption text containing tweet author
    caption_text = constants.default_caption(tweet_author)
    return caption_text
