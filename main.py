from flask import Flask, request, make_response, send_file, jsonify, render_template
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
import logging, os, json

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

    def post(self, filename=None):
        #FIXME: unsafe due to lack of filename parsing
        bundle = request.get_json()
        #with open()
        if filename is not None:
            savepath = os.path.join(BUNDLES_UPLOAD_DIR, filename)
            logger.debug("savepath: "+savepath)
            with open(savepath, 'w') as f:
                json.dump(bundle, f)
        # with open('file.json', 'w') as f:
        #json.dump(request.form, f)
        return jsonify({'plan': bundle['building_plan_filename'], 'bundle': filename})


class RawPlans(Resource):
    def get(self, filename=None):

        if(filename is None):
            files = os.listdir(RAWPLANS_UPLOAD_DIR)
            return jsonify(files)
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
        file = request.files['file']
        logger.debug("file: "+file.filename)
        return {'request': request.content_length}


class Measures(Resource):

    def get(self):
        return "MEASURES"

    def post(self, filename=None):
    #FIXME: unsafe due to lack of filename parsing
        measure = request.get_json()
        #with open()
        if filename is not None:
            savepath = os.path.join(MEASURES_UPLOAD_DIR, filename)
            logger.debug("savepath: "+savepath)
            with open(savepath, 'w') as f:
                json.dump(measure, f)
        # with open('file.json', 'w') as f:
        #json.dump(request.form, f)
        return {'measure': filename}


@app.route('/')
def main():
    plan = request.args.get('plan')
    #FIXME: security issue? path traversal?
    return render_template('index.html', plan=plan)


api.add_resource(Plans, '/plans', '/plans/<filename>')
api.add_resource(Bundles, '/bundles', '/bundles/<filename>')
api.add_resource(RawPlans, '/rawplans', '/rawplans/<filename>')
api.add_resource(Measures,'/measures','/measures/<filename>')
api.add_resource(HelloWorld, "/")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=9999)