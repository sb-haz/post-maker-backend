"""
Imports
"""
from flask import Flask
from flask_restful import Api, Resource, reqparse

import tool_handler


"""
Flask app
"""
app = Flask(__name__)
api = Api(app)


"""
Request parser
"""
quote_put_args = reqparse.RequestParser()
quote_put_args.add_argument("tweet_url",
                            type=str,
                            help="Tweet URL",
                            required=True)
quote_put_args.add_argument("watermark",
                            type=str,
                            help="Watermark",
                            required=True)


"""
Quote POST request
"""
class QuoteMaker(Resource):
    def post(self):

        # get post request args
        args = quote_put_args.parse_args()

        tweet_url = args['tweet_url']
        watermark = args['watermark']
        print("TWEWEW", watermark)

        # create quote image
        # get auto gen caption
        # caption_text = tool_handler.generate_quote(url=args['twitter_url'],
        #                                           username=args['watermark'])

        # return caption as response
        return {'tweet': tweet_url,
                'watermark': watermark}, 201


"""
Add URL to resource
"""
api.add_resource(QuoteMaker, "/tool/quote")


"""
Run app
"""
if __name__ == "__main__":
    app.run(debug=True)
