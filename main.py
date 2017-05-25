from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
FILES_DIR = "store/"
UPLOAD_DIR = "C:\UPLOAD"


class Plans(Resource):
    def get(self):
        current_plans = list()
        return current_plans

    def post(self):

        return {'request': request.content_length}

api.add_resource(Plans, '/plans')

if __name__ == '__main__':
    app.run(debug=True)