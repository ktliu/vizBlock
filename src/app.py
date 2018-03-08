from flask import Flask, jsonify, render_template, request
from datetime import datetime
import sys
sys.path.append('/vagrant/pyethereum') #TODO: I'm a noob :D
sys.path.append('/vagrant/viper')

#### ethereum
import pytest
from ethereum.tools import tester
from ethereum.tests.utils import new_db
from ethereum.db import EphemDB
from ethereum.hybrid_casper import casper_utils
from ethereum.slogging import get_logger
from ethereum.tests.hybrid_casper.testing_lang import TestLangHybrid
from ethereum.visualization import CasperVisualization
########
 
app = Flask(__name__)
API_PATH = '/api/v1.0/'
 
@app.route(API_PATH + 'draw', methods=['POST'])
def test_string_to_graphviz():
	request_json = request.get_json(force=True)
	#Grab from client
	test_string = request_json['test_string']
	epoch = int(request_json['epoch'])
	withdrawal_delay = int(request_json['withdrawal_delay'])
	base_interest_factor = float(request_json['base_interest_factor'])
	base_penalty_factor = float(request_json['base_penalty_factor'])
	type_graph = request_json['type']

	#draw epochs or blocks
	is_draw_epoch = True
	if type_graph == "block":
		is_draw_epoch = False

	#run test string
	_db = new_db()

	@pytest.fixture(scope='function')
	def db():
	    return EphemDB()

	alt_db = db	 
	test = TestLangHybrid(epoch, withdrawal_delay, base_interest_factor, base_penalty_factor)
	test.parse(test_string)
	cv = CasperVisualization('test', test.t, is_draw_epoch)

	output = cv.graphviz_output().source

	response = jsonify({'output': output})
	response.headers.add('Access-Control-Allow-Origin', '*') #TODO: aha :p
	return response

@app.route('/')
def homepage():
	return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True, port=3000)