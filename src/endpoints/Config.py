from falcon.status_codes import * 
from os import path

class config(object):
    def on_get(self, req, resp):
        resp.status = HTTP_200
        resp.content_type = 'text/html'
        print(path.relpath("render/config.html"))
        with open('/Users/leenton/python/hmp/rsc/html/config.html', 'r') as f:
            resp.text = f.read()