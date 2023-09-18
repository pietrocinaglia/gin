import os
from flask import Flask, render_template, request, Response, send_file, after_this_request
import json
import uuid
import shutil

from includes.generator import multilayerNetwork
from includes.noising import noising

app = Flask(__name__, template_folder='html')
app.config['DEBUG'] = True
app.config['TMP_DIRPATH'] = os.path.dirname(__file__) + "/tmp/"

@app.route('/generate', methods=['GET','POST'])
def generate():
    try:
        request_data = json.loads( request.get_json() )
        dataset_name = str( request_data['dataset_name'] )
        ntype = str( request_data['ntype'] )
        l = int( request_data['l'] )
        n = int( request_data['n'] )
        m = int( request_data['m'] )
        p = float( request_data['p'] )
        q = float( request_data['q'] )
        z = float( request_data['z'] )
        noises = request_data['noises'].split(" ")
        noise_type = 'shuffling'
    except ValueError:
        return json.dumps({'error':"Request consists of not valid params."}), 400, {'ContentType':'application/json'}

    # Generate UUDI for current request
    request_uuid = str(uuid.uuid4())
    # Create temporary directory for current request
    request_tmp_dirpath = app.config['TMP_DIRPATH'] + request_uuid + "/"
    os.mkdir( request_tmp_dirpath )

    # Type of network
    if ntype == 'multilayer':
        network = multilayerNetwork( dataset_name, l, n, m, p, q, z, request_tmp_dirpath )
        noising( dataset_name, network, noises, noise_type, request_tmp_dirpath )
    
    # Compress response as zip file
    shutil.make_archive( app.config['TMP_DIRPATH'] + dataset_name, 'zip', request_tmp_dirpath )
    
    @after_this_request
    def clean_temporary(response):
        try:
            shutil.rmtree( request_tmp_dirpath )
            os.remove( app.config['TMP_DIRPATH'] + dataset_name + ".zip" )
        except Exception as error:
            app.logger.error( "Error removing temporary director for UUID:" + str(request_uuid), error )
        return response
    
    return send_file( app.config['TMP_DIRPATH'] + dataset_name + ".zip", mimetype='application/zip' )

@app.route('/')
def test():
    return render_template('index.html')

###
###
if __name__ == '__main__':
    if not os.path.isdir( app.config['TMP_DIRPATH'] ):
        print( "[ WARNING ] The temporary files directory did not exist, and it was created ('tmp')." )
        os.mkdir( app.config['TMP_DIRPATH'] )
        with open( app.config['TMP_DIRPATH'] + 'index.html', 'w') as fp:
            pass
    # Running app
    app.run(debug=app.config['DEBUG'])