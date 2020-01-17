from flask import Flask, request, Response, make_response
from uuid import uuid1
from DLX import DLX

app = Flask(__name__)

dlx_pool = {}

# Session 1
@app.route("/dlx/connect", methods=['GET'])
def connect():
    dlx = DLX()

    dlx.load('examples/sum.asm')
    dlx.trace()

    dlxId = uuid1()
    dlx_pool[str(dlxId)] = dlx

    res = Response('OK')

    res.set_cookie('DLX_ID', str(dlxId))

    return res


@app.route("/dlx/disconnect", methods=['GET'])
def disconnect():
    dlxId = request.cookies.get('DLX_ID')
    del dlx_pool[dlxId]

    res = Response('OK')
    
    res.set_cookie('DLX_ID', '', expires=0)

    return res


@app.route("/dlx/run", methods=['GET'])
def run():
    dlxId = request.cookies.get('DLX_ID')
    dlx = dlx_pool[dlxId]

    res = dlx.run()
    return Response(res, mimetype='application/json')

@app.route("/dlx/step", methods=['GET'])
def step():
    dlxId = request.cookies.get('DLX_ID')
    dlx = dlx_pool[dlxId]

    res = dlx.step()
    return Response(res, mimetype='application/json')


@app.route("/dlx/inspect", methods=['GET'])
def inspect():
    dlxId = request.cookies.get('DLX_ID')
    print(dlxId)
    print(dlx_pool.keys())
    dlx = dlx_pool[dlxId]

    res = dlx.inspect()
    return Response(res, mimetype='application/json')

if __name__ == '__main__':
    app.run(port='3000')
