from flask import Flask, request, Response, make_response
from flask_cors import CORS, cross_origin
import json
from dlx import DlxProcessPool, DlxProcess
from middleware import checkDlxProcessIdHeader

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

dlxProcessPool = DlxProcessPool()

@app.route("/dlx/connect", methods=['GET'])
def connect():
	dlxProcess = DlxProcess()

	dlxProcess.load('examples/sum.asm')
	dlxProcess.trace()

	dlxProcessId = dlxProcessPool.add(dlxProcess)

	res = Response(json.dumps({
		'dlxProcessId': dlxProcessId
	}))

	# res.headers['Access-Control-Allow-Credentials'] = 'true'
	res.mimetype = 'application/json'
	res.set_cookie('DLX_PROCESS_ID', dlxProcessId,
	               domain='.dlxProcess.local', path='/', httponly=True)

	return res


@app.route("/dlx/disconnect", methods=['GET'])
@checkDlxProcessIdHeader
def disconnect():
	dlxProcess = request.environ['dlxProcess']
	dlxProcessPool.remove()

	res = Response('OK')

	res.set_cookie('DLX_PROCESS_ID', '', expires=0)

	return res


@app.route("/dlx/run", methods=['GET'])
@checkDlxProcessIdHeader
def run():
	dlxProcess = request.environ['dlxProcess']

	res = dlxProcess.run()
	return Response(res, mimetype='application/json')


@app.route("/dlx/step", methods=['GET'])
@checkDlxProcessIdHeader
def step():
	dlxProcess = request.environ['dlxProcess']

	res = dlxProcess.step()
	return Response(res, mimetype='application/json')


@app.route("/dlx/reset", methods=['GET'])
@checkDlxProcessIdHeader
def reset():
	dlxProcess = request.environ['dlxProcess']

	res = dlxProcess.reset()
	return Response(res, mimetype='application/json')


@app.route("/dlx/inspect", methods=['GET'])
@checkDlxProcessIdHeader
def inspect():
	dlxProcess = request.environ['dlxProcess']

	res = dlxProcess.inspect()
	return Response(res, mimetype='application/json')

@app.route("/dlx/disassemble", methods=['GET'])
@checkDlxProcessIdHeader
def disassemble():
	dlxProcess = request.environ['dlxProcess']

	res = dlxProcess.disassemble()
	return Response(res, mimetype='application/json')


if __name__ == '__main__':
	app.run(debug=True, port='5000')
