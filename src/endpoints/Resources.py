from falcon.status_codes import * 


class resources(object):
    def on_get(self,req, resp, folder, filename):
        resp.status = HTTP_200
        #logic to check what the file extension is and to set the correct header based on the file type. 
        file_format = (filename.split('.'))[-1]
        match (file_format):
            case 'css':
                resp.content_type = 'text/css'
            case 'htm':
                resp.content_type = 'text/html'
            case 'html':
                resp.content_type = 'text/html'
            case 'jpg':
                resp.content_type = 'image/jpg'
            case 'png':
                resp.content_type = 'image/png'
            case 'svg':
                resp.content_type = 'image/svg+xml'
            case 'gif':
                resp.content_type = 'image/gif'
            case 'ttf':
                resp.content_type = 'image/ttf'
            case 'js':
                resp.content_type = 'text/javascript'
        with open('/Users/leenton/python/hmp/rsc/' + folder + '/' + filename, 'rb') as f:
            resp.text = f.read()
        