"""
Imports
"""
from numpy import extract

from tools import quote_maker
from tools import video_maker
from helpers import watermark
from helpers import constants
# from helpers import email
from apis import twitter_api


"""
Extract Tweet ID from share link
"""
def extract_id_from_url(url):
    tweet_id = ""
    try:
        tweet_id = url.split('/')[-1].split('?')[0]
    except Exception as e:
        print(e)
    return tweet_id


"""
Email video
"""
def email_user(user_email, username, tweet_id, tweet_author,
               filepath):

    # Email video to user
    # email.send_email_with_attachment(
    #     user_email, username, tweet_id, tweet_author, filepath)

    return True


"""
Create quote image
Returns generated caption text
"""
def generate_quote(url, username):

    # Extract tweet id from url
    tweet_id = extract_id_from_url(url)

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


"""
Create video
"""
def generate_video(height, url, username, user_email):

    # Extract tweet id from url
    tweet_id = extract_id_from_url(url)

    # Get Tweet info
    # try:
    #     tweet_text, tweet_author, media_type = twitter_api.getTweetInfo(
    #         tweet_id)
    # except Exception as e:
    #     print(e)
    media_type = "video"
    tweet_text = "Its the fact cant nobody talk about nobody yet they still be fkn talking"
    tweet_author = "nunidior"

    # Create watermark
    watermark_filepath = ""
    try:
        watermark_filepath = watermark.create_watermark(username=username,
                                                        media_type="video")
    except Exception as e:
        print(e)

    # Convert string text to image
    # Get filepath and height
    caption_height = ""
    caption_filepath = ""
    try:
        caption_height, caption_filepath = quote_maker.generate_quote(text=tweet_text,
                                                                      tweet_id=tweet_id,
                                                                      username=username)
    except Exception as e:
        print(e)

    # Check media type of tweet
    if media_type == "video":
        print("Media_Type is VIDEO")

        # # Download twitter video
        try:
            video_maker.download_twitter_video(url, tweet_id)
        except Exception as e:
            print(e)

        # Add caption and watermark to video
        try:
            filepath, video_duration = video_maker.generate_video(tweet_id=tweet_id,
                                                                  caption_height=caption_height,
                                                                  caption_filepath=caption_filepath,
                                                                  watermark_filepath=watermark_filepath,
                                                                  video_height=height,
                                                                  video_width=1080)

        except Exception as e:
            print(e)

        # Email video to user
        # if email_user(user_email, username, tweet_id, tweet_author,
        #               filepath):

            # If email is successful delete videos
            '''
            render_filepath = f"{ABSOLUTE_PATH}resources/videos/downloads/{tweet_id}.mp4"
            render_filepath = f"{ABSOLUTE_PATH}resources/videos/outputs/{height}x1080/{tweet_id}.mp4"
            try:
                os.remove(render_filepath)
                os.remove(render_filepath)
            except Exception as e:
                print(e)
            '''
            # pass

    # If tweet doesnt contain video
    elif media_type == "photo":
        print("Tweet contains photo, not video")
        return False

    elif media_type == "none":
        print("Tweet contains no media, not video")
        return False

    
    return True
