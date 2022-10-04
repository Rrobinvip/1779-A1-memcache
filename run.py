#!../venv/bin/python

from werkzeug.serving import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from frontend import app as frontend_app
from backend import app as backend_app

# werkzeug.wsgi.DispatcherMiddleware allows combining applications. 
application = DispatcherMiddleware(frontend_app, {
    '/backend': backend_app
})

if __name__ == "__main__":
    run_simple('localhost', 
               port = 5001, 
               application = application,
               use_reloader=True, 
               use_debugger=True, 
               use_evalex=True,
               threaded=True)