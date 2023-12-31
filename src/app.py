import os
from flask import Flask, render_template, request, Response, send_file, after_this_request
import json
import uuid
import shutil
import logging
#
from includes.generator import staticNetwork, multilayerNetwork
from includes.noising import noising

###
DEBUG = False
BASEPATH = os.path.dirname(__file__) + "/"
#
app = Flask(__name__, template_folder='html')
app.config['TMP_DIRPATH'] = BASEPATH + "tmp/"
app.config['DEBUG'] = DEBUG
#
logging.basicConfig(filename=(BASEPATH+'flask.log'), level=logging.WARNING, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
###

@app.route('/healthz', methods=['GET'])
def healthz():
    return json.dumps({'status':'online'}), 200

@app.route('/generate', methods=['GET','POST'])
def generate():
    #
    # Parse data
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
        app.logger.error( "Request consists of no valid params." )
        return json.dumps({'error':'Request consists of no valid params.'}), 400, {'ContentType':'application/json'}

    # 
    # Generate UUDI for current request
    request_uuid = str(uuid.uuid4())
    # Create temporary directory for current request
    request_tmp_dirpath = app.config['TMP_DIRPATH'] + request_uuid + "/"
    os.mkdir( request_tmp_dirpath )

    #
    # multilayer
    if ntype == 'multilayer' and l > 1:
        network, log = multilayerNetwork( dataset_name, l, n, m, p, q, z, request_tmp_dirpath )
        log = noising( dataset_name, network, noises, noise_type, True, request_tmp_dirpath, log )
    #
    # static or one-layer
    elif ntype == 'static' or l == 1:
        network, log = staticNetwork( dataset_name, n, m, p, q, request_tmp_dirpath )
        log = noising( dataset_name, network, noises, noise_type, False, request_tmp_dirpath, log )
    #
    # unrecognized
    else:
        app.logger.error( "UUID:" + str(request_uuid) + " - Network type not supported." )
        return json.dumps({'error':'Network type not supported.'}), 400, {'ContentType':'application/json'}
    
    #
    # write log
    log = json.dumps(log, indent=4)
    with open( request_tmp_dirpath+'log.json', 'w' ) as outfile:
        outfile.write(log)
    
    #
    # Compress response as zip file
    shutil.make_archive( app.config['TMP_DIRPATH'] + dataset_name, 'zip', request_tmp_dirpath )
    
    #
    ###
    @after_this_request
    def clean_temporary(response):
        try:
            shutil.rmtree( request_tmp_dirpath )
            os.remove( app.config['TMP_DIRPATH'] + dataset_name + ".zip" )
        except Exception as error:
            app.logger.warning( "UUID:" + str(request_uuid) + " - Error removing temporary directory.", error )
        return response
    ###

    #
    return send_file( app.config['TMP_DIRPATH'] + dataset_name + ".zip", mimetype='application/zip' )

@app.route('/')
def test():
    return render_template('index.html')

###
if __name__ == '__main__':
    if app.config['DEBUG']:
        if not os.path.isdir( app.config['TMP_DIRPATH'] ):
            app.logger.info( "Temporary files directory did not exist, and it was created ('tmp')." )
            os.mkdir( app.config['TMP_DIRPATH'] )
            with open( app.config['TMP_DIRPATH'] + 'index.html', 'w') as fp:
                pass
        # Running app
        app.run(debug=app.config['DEBUG'])
    else:
        print( "Autostart is available in Debug Mode only: DEBUG=True" )