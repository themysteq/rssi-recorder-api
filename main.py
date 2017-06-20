from flask import Flask, request, make_response, send_file
from flask_restful import Resource, Api
import logging
import os
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
api = Api(app)
FILES_DIR = "store/"
UPLOAD_DIR = "C:\UPLOAD"
BUNDLES_UPLOAD_DIR = "C:\UPLOAD\BUNDLES"
RAWPLANS_UPLOAD_DIR = "C:\UPLOAD\RAWPLANS"
MEASURES_UPLOAD_DIR = "C:\UPLOAD\MEASURES"
PLANS_UPLOAD_DIR = "C:\UPLOAD\PLANS"

logger = logging.getLogger(__name__)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class Bundles(Resource):

    def get(self):
        current_bundles = list()
        files = os.listdir(BUNDLES_UPLOAD_DIR)
        logger.debug(files)
        return current_bundles


class RawPlans(Resource):
    def get(self, filename=None):

        if(filename is None):
            files = os.listdir(RAWPLANS_UPLOAD_DIR)
            return files
        else:
            response = make_response()
            return send_file(RAWPLANS_UPLOAD_DIR+'/'+filename, mimetype='image/png')


class Plans(Resource):

    def get(self, filename=None):

        if(filename is None):
            files = os.listdir(PLANS_UPLOAD_DIR)
            return files
        else:
            response = make_response()
            return send_file(PLANS_UPLOAD_DIR+'/'+filename, mimetype='image/png')

    def post(self):
        return {'request': request.content_length}

api.add_resource(Plans, '/plans', '/plans/<filename>')
api.add_resource(Bundles, '/bundles')
api.add_resource(RawPlans, '/rawplans', '/rawplans/<filename>')
api.add_resource(HelloWorld, "/")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=9999)