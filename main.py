"""
Imports
"""
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

import tool_handler


"""
Flask app
"""
app = Flask(__name__)
api = Api(app)
CORS(app, resources={r'/*': {'origins': '*'}})


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

        # create quote image
        # get auto gen caption
        caption_text = tool_handler.generate_quote(url=tweet_url, username=watermark)

        # return caption as response
        return {'caption': caption_text}, 201


"""
Add URL to resource
"""
api.add_resource(QuoteMaker, "/tool/quote")


"""
Run app
"""
if __name__ == "__main__":
    app.run(debug=True)
