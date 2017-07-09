from flask import Flask, request, make_response, send_file, jsonify, render_template, abort
from flask_restful import Resource, Api
from pprint import pprint
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

    def get(self, filename=None):
        current_bundles = list()
        if filename is None:
            files = os.listdir(BUNDLES_UPLOAD_DIR)
            current_bundles = files
            logger.debug(files)
            return jsonify(current_bundles)
        else:
            bundlepath = os.path.join(BUNDLES_UPLOAD_DIR,filename)
            with open(bundlepath,'rt') as file:
                jsondata = file.read()
                #FIXME: double converting
                data = json.loads(jsondata)
                return jsonify(data)

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

    def get(self, filename=None):
        if filename is None:
            measures = os.listdir(MEASURES_UPLOAD_DIR)
            #FIXME: security issue? path traversal?
            return jsonify(measures)
        else:
            #FIXME: brak filtrowania arguemtnow gdziekolwiek
            with open(os.path.join(MEASURES_UPLOAD_DIR, filename),'rt') as measure_file:
                data = json.load(measure_file)
            pprint(data)
        return jsonify(data)

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
    rawplans = os.listdir(RAWPLANS_UPLOAD_DIR)
    bundles = os.listdir(BUNDLES_UPLOAD_DIR)
    pprint(bundles)
    #plan = request.args.get('plan')
    #FIXME: security issue? path traversal?
    return render_template('index.html', rawplans=rawplans, bundles=bundles)


@app.route('/map')
def map():
    plan = request.args.get('plan')
    return render_template('map.html', plan=plan)

@app.route('/bundle_details/<bundle>')
def bundle_detail(bundle=None):
    if bundle is None:
        abort(404)
    else:
        #FIXME: brak filtrowania arguemtnow gdziekolwiek
        with open(os.path.join(BUNDLES_UPLOAD_DIR,bundle),'rt') as bundle_file:
            data = json.load(bundle_file)
        pprint(data)

    return render_template('bundle.html', bundle_data=data)

api.add_resource(Plans, '/plans', '/plans/<filename>')
api.add_resource(Bundles, '/bundles', '/bundles/<filename>',endpoint='bundles')
api.add_resource(RawPlans, '/rawplans', '/rawplans/<filename>',endpoint='rawplans')
api.add_resource(Measures,'/measures','/measures/<filename>',endpoint='measures')
api.add_resource(HelloWorld, "/")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=9999)