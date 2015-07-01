from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

import cgi

class FormPage(Resource):
    def render_GET(self, request):
        return ''
        
    def render_POST(self, request):
        return 'You submitted: %s' % (cgi.escape(request.args["the-field"][0]),)
        
root = Resource()
root.putChild("form", FormPage())
factory = Site(root)
reactor.listenTCP(8880, factory)
reactor.run()
