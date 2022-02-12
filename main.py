from distutils.log import debug
from email.quoprimime import quote
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

quote_put_args = reqparse.RequestParser()
quote_put_args.add_argument("tweet_url", type=str,
                            help="Tweet URL", required=True)
quote_put_args.add_argument("watermark", type=str,
                            help="Watermark", required=True)
quote_put_args.add_argument("email", type=str, help="Email", required=True)

videos = {}


class QuoteMaker(Resource):
    def post(self):
        args = quote_put_args.parse_args()
        print(args)
        return {"status": "preparing"}, 201

        # return {"data": args}


api.add_resource(QuoteMaker, "/tool/quote")


if __name__ == "__main__":
    app.run(debug=True)
