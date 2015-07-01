""" Script to download file from Twisted server using GET.
    Usage: http://localhost:9009/<filename with extension>
    Reactor is listening to TCP connections on port 9009."""
    
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

# Will contain filename, will call GET method
class DownloadFile(Resource):
    def __init__(self, path):
        Resource.__init__(self)
        self.path = path
        
    def render_GET(self, request):
        filename = self.path.split('/')[-1]
        try:
            fRequested = open(filename, "r")
            fileContents = fRequested.read()
            fRequested.close()
            request.setResponseCode(200)
        except IOError:
            request.setResponseCode(404)
            return "File not found."
        
        request.responseHeaders.setRawHeaders('Content-Disposition', ['attachment; filename="'+filename+'"'])
        return "%s" % (fileContents)
        
# Will internally create DownloadFile object
class Download(Resource):
    def getChild (self, name, request):
        return DownloadFile(request.URLPath().__str__())
        
root = Download()
factory = Site(root)
reactor.listenTCP(9009, factory)
reactor.run()
