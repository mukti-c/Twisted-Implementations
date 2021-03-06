from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.resource import NoResource

from calendar import calendar

class YearPage(Resource):
    def __init__(self, year):
        Resource.__init__(self)
        self.year = year
        
    def render_GET(self, request):
        return "%s" % (calendar(self.year),)
        
class Calendar(Resource):
    def getChild(self, name, request):
        try:
            year = int(name)
        except ValueError:
            return NoResource()
        else:
            return YearPage(year)
            
root = Calendar()
factory = Site(root) # Created site using Resource subclass
reactor.listenTCP(8880, factory)
reactor.run()
