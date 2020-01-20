from flask import Flask, request, Response, make_response
from flask_cors import CORS, cross_origin
import json
from dlx import DlxProcessPool, DlxProcess
import middleware

app = Flask(__name__)
CORS(app)

app.wsgi_app = middleware.DlxProcessMiddleware(app.wsgi_app)

dlxProcessPool = DlxProcessPool()

@app.route("/dlx/connect", methods=['GET'])
@cross_origin()
def connect():
    dlxProcess = DlxProcess()

    dlxProcess.load('examples/sum.asm')
    dlxProcess.trace()

    dlxProcessId = dlxProcessPool.add(dlxProcess)

    res = Response(json.dumps({
        'dlxProcessId': dlxProcessId
    }))

    res.mimetype = 'application/json'
    res.set_cookie('DLX_PROCESS_ID', dlxProcessId, domain='.dlxProcess.local', path='/', httponly=True)

    return res


@app.route("/dlx/disconnect", methods=['GET'])
@cross_origin
def disconnect():
    dlxProcess = request.environ['dlxProcess']
    dlxProcessPool.remove()

    res = Response('OK')
    
    res.set_cookie('DLX_PROCESS_ID', '', expires=0)

    return res


@app.route("/dlx/run", methods=['GET'])
@cross_origin()
def run():
    dlxProcess = request.environ['dlxProcess']

    res = dlxProcess.run()
    return Response(res, mimetype='application/json')

@app.route("/dlx/step", methods=['GET'])
@cross_origin()
def step():
    dlxProcess = request.environ['dlxProcess']

    res = dlxProcess.step()
    return Response(res, mimetype='application/json')

@app.route("/dlx/reset", methods=['GET', 'OPTIONS'])
@cross_origin()
def reset():
    dlxProcess = request.environ['dlxProcess']

    res = dlxProcess.reset()
    return Response(res, mimetype='application/json')

@app.route("/dlx/inspect", methods=['GET', 'OPTIONS'])
@cross_origin()
def inspect():
    dlxProcess = request.environ['dlxProcess']
    
    res = dlxProcess.inspect()
    return Response(res, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port='5000')
