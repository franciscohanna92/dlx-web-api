from werkzeug.wrappers import Request, Response
from dlx import DlxProcessPool

dlxProcessPool = DlxProcessPool()

class DlxProcessMiddleware(object):
  def __init__(self, app):
    self.app = app
    
  def __call__(self, environ, start_response):
    request = Request(environ, shallow=True)

    if(request.path != '/dlx/connect' and request.method != 'OPTIONS'):
      dlxProcessId = request.headers.get('DLX-Process-Id')

      if(dlxProcessId is None):
        res = Response('Missing DLX-Process-Id header', mimetype= 'text/plain', status=400)
        return res(environ, start_response)

      environ['dlxProcess'] = dlxProcessPool.get(dlxProcessId)

    return self.app(environ, start_response)