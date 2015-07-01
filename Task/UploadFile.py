from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

import cgi
import mimetypes
import os
import pycurl

class UploadFile(Resource):
    # Will respond to GET requests with blank page
    def render_GET(self, request):
        return ''
    
    # To POST requests, will allow uploading of files   
    def render_POST(self, request):
        filename = os.path.join("", cgi.escape(request.args["file-name"][0]))
        urlSplit = request.URLPath().__str__().split('/')
        url = urlSplit[0] + "//" + urlSplit[2]
        POSTValues = [("file", (pycurl.FORM_FILE, filename))]
        
        if not os.path.exists(filename):
            print "The file does not exist."
            raise SystemExit
            
        try:
            c = pycurl.Curl()
            c.setopt(c.POST, 1)
            c.setopt(c.URL, url)
            c.setopt(c.HTTPHEADER, ['Content-Disposition: form-data; filename="%s"' % filename.split('/')[-1], 'Content-Type: %s' % mimetypes.guess_type(filename)[0]])
            c.setopt(c.HTTPPOST, POSTValues)
            c.setopt(c.VERBOSE, 1)
            c.perform()
            c.close()
            
        except IOError:
            traceback.print_tb()
            return "Error in uploading file."
                    
root = Resource()
root.putChild("file", UploadFile())
factory = Site(root)
reactor.listenTCP(8881, factory)
reactor.run()
