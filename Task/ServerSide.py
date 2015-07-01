""" Script to upload file to Twisted server using PUT
    and POST. Can also use DELETE to delete a resource
    Usage for upload: With UploadFilePycURL.py
    Usage for DELETE: http://localhost:8080/file?resource=<filename>
    Returns headers of the request as well."""


from twisted.web.server import Site
from twisted.web import http, resource
from twisted.web.iweb import IRequest
from twisted.internet import reactor

import os, re, shutil

class ServerSide(resource.Resource):
    # Refer http://www.restapitutorial.com/lessons/httpmethods.html for response values
    
    def printHeaders(self, request):
        string = ""
        for key in request.getAllHeaders():
            string += "%s: %s\n" % (key, request.getHeader(key))
        print string
    
    def render_POST(self, request):
        # Find filename from Content-Disposition header
        content = request.getHeader("Content-Disposition")
        filename = re.search('filename="(.*)"$', content).group(0)
        filename = filename.split('"')[1]
            
        if (os.path.exists(filename)):
            request.setResponseCode(409)  # Resource exists, responseCode = 409 (Conflict)
            return "Cannot upload file; File already exists on server."
               
        else:
            try:
                fd = open(filename, 'wb')
                contents = request.content.read()
                fd.write(contents[contents.find('\r\n\r\n')+4:contents.rfind('\r\n\r\n')+2])  
                # contents contains Content-Disposition details too, hence have to slice      
                # +4 because there are two unmatched (\r\n)s in the beginning, +2 in the end
                fd.close()
                request.setResponseCode(201)  # Resource has been created, hence responseCode = 201
                return "File uploaded."     
            
            except IOError:
                request.setResponseCode(501)  # Request not implemented, hence responseCode = 501
                return "File was not uploaded."
        
    def render_PUT(self, request):
        # Find filename from Content-Disposition header
        content = request.getHeader("Content-Disposition")
        filename = re.search('filename="(.*)"$', content).group(0)
        filename = filename.split('"')[1]
        
        if (os.path.exists(filename)):
            # File exists. Hence update. Try to open and write. If success, 200. Else 501
            try:
                fd = open(filename, 'wb')
                contents = request.content.read()
                fd.write(contents[contents.find('\r\n\r\n')+4:contents.rfind('\r\n\r\n')+2])         
                fd.close()
                request.setResponseCode(200)  # Resource has been updated, hence responseCode = 200
                return "File uploaded."     
            
            except IOError:
                request.setResponseCode(501)  # Request not implemented, hence responseCode = 501
                return "File was not uploaded."
            
        else:
            try:
                fd = open(filename, 'wb')
                contents = request.content.read()
                fd.write(contents[contents.find('\r\n\r\n'):contents.rfind('\r\n\r\n')])         
                fd.close()
                request.setResponseCode(201)  # Resource has been created, hence responseCode = 201
                return "File uploaded."     
            
            except IOError:
                request.setResponseCode(501)  # Request not implemented, hence responseCode = 501
                return "File was not uploaded."
                
    def render_DELETE(self, request):
        # Deleting a resource can include deleting a folder and a file
        #ServerSide.printHeaders(self, request)
        resName = request.args['resource'][0]
        if (os.path.exists(resName)):
            if (os.path.isdir(resName)):    # is a directory
                if not os.listdir(resName):     # not an empty directory
                    os.rmdir(resName)
                else:
                    shutil.rmtree(resName)
            else:   # is a file
                os.remove(resName)
            request.setResponseCode(200)
        else:
            request.setResponseCode(404)
            
        return ""
                             
root = resource.Resource()
root.putChild("file", ServerSide())
factory = Site(root)
reactor.listenTCP(8080, factory)
reactor.run()
