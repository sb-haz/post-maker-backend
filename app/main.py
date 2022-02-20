"""
Imports
"""
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import threading

import tool_handler


"""
Flask app
"""
app = Flask(__name__)
api = Api(app)
CORS(app, resources={r'/*': {'origins': '*'}})


"""
Quote Request parser
tweet_url, watermark
"""
quote_put_args = reqparse.RequestParser()
quote_put_args.add_argument("tweet_url", type=str, help="Tweet URL", required=True)
quote_put_args.add_argument("watermark", type=str, help="Watermark", required=True)


"""
Video Request parser
tweet_url, watermark, email
"""
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("tweet_url", type=str, help="Tweet URL", required=True)
video_put_args.add_argument("watermark", type=str, help="Watermark", required=True)
video_put_args.add_argument("email", type=str, help="Email", required=True)


"""
Homepage
"""
class Home(Resource):
    def get(self):
        return "Post Maker API v2"


"""
Quote POST request
"""
class QuoteMaker(Resource):
    def post(self):

        # get post request args
        args = quote_put_args.parse_args()

        tweet_url = args['tweet_url']
        watermark = args['watermark']

        # create quote image
        # get auto gen caption
        caption_text = tool_handler.generate_quote(url=tweet_url, username=watermark)

        # return caption as response
        return {'render_src': '/examples/quote_maker.png', 'caption': caption_text}, 201


"""
Video POST request
"""
class VideoMaker(Resource):
    def post(self):

        # get post request args
        args = video_put_args.parse_args()

        tweet_url = args['tweet_url']
        watermark = args['watermark']
        email = args['email']

        # create caption image
        # create video
        newThread = threading.Thread(target=tool_handler.generate_video, args=(1080, tweet_url, watermark, email))
        newThread.start()

        # return caption as response
        return {"status_msg": "When your video is ready, it will be emailed to you."}, 201


"""
Reel POST request
"""
class ReelMaker(Resource):
    def post(self):

        # get post request args
        args = video_put_args.parse_args()

        tweet_url = args['tweet_url']
        watermark = args['watermark']
        email = args['email']

        # create caption image
        # create video
        newThread = threading.Thread(target=tool_handler.generate_video, args=(1920, tweet_url, watermark, email))
        newThread.start()
        # tool_handler.generate_video(height=1920, url=tweet_url, username=watermark, user_email=email)

        # return caption as response
        return {"status_msg": "When your video is ready, it will be emailed to you."}, 201


"""
Add URL to resource
"""
api.add_resource(Home, "/")
api.add_resource(QuoteMaker, "/tool/quote")
api.add_resource(VideoMaker, "/tool/video")
api.add_resource(ReelMaker, "/tool/reel")


"""
Run app
"""
if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
