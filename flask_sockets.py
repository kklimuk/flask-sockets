# -*- coding: utf-8 -*-
from werkzeug.routing import Map, Rule, NotFound
from werkzeug.exceptions import HTTPException

def log_request(self):
    log = self.server.log
    if log:
        if hasattr(log, 'info'):
            log.info(self.format_request() + '\n')
        else:
            log.write(self.format_request() + '\n')


# Monkeys are made for freedom.
# I don't know why they are, just that they must be.
try:
    import gevent
    from geventwebsocket.gunicorn.workers import GeventWebSocketWorker as Worker
except ImportError:
    pass

if 'gevent' in locals():
    # Freedom-Patch logger for Gunicorn.
    if hasattr(gevent, 'pywsgi'):
        gevent.pywsgi.WSGIHandler.log_request = log_request



class SocketMiddleware(object):
    def __init__(self, wsgi_app, socket):
        self.ws = socket
        self.app = wsgi_app

    def __call__(self, environ, start_response):
        urls = self.ws.url_map.bind_to_environ(environ)

        try:
            endpoint, args = urls.match()
            handler = self.ws.endpoints[endpoint]
            environment = environ['wsgi.websocket']

            handler(environment, **args)

        except HTTPException, error:
            return self.app(environ, start_response)



class Sockets(object):
    def __init__(self, app=None):
        self.endpoints = {}
        self.url_map = Map()
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.wsgi_app = SocketMiddleware(app.wsgi_app, self)

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.pop('endpoint', None)
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator

    def add_url_rule(self, rule, endpoint, f, **options):
        self.endpoints[endpoint if endpoint else rule] = f
        self.url_map.add(Rule(rule, endpoint=endpoint if endpoint else rule))


# CLI sugar.
if 'Worker' in locals():
    worker = Worker