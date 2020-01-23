from functools import wraps
from flask import request, Response
# from werkzeug.wrappers import Request, Response
from dlx import DlxProcessPool

dlxProcessPool = DlxProcessPool()

def checkDlxProcessIdHeader(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
      dlxProcessId = request.headers.get('DLX-Process-Id')

      if(dlxProcessId is None):
        res = Response('Missing DLX-Process-Id header', mimetype= 'text/plain', status=400)
        return res

      dlxProcess = dlxProcessPool.get(dlxProcessId)
      
      if(dlxProcess is None):
        res = Response('The DLX process does not exists', mimetype= 'text/plain', status=400)
        return res

      request.environ['dlxProcess'] = dlxProcess

      return f(*args, **kwargs)
    
    wrapper.__name__ = f.__name__
    return wrapper
