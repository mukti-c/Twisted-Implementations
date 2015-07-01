"""To upload fileToUpload using pycURL.
    Can use either POST or PUT"""

from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

import pycurl
import StringIO

def uploadPOST(fileToUpload):
    buf = StringIO.StringIO()
    
    c = pycurl.Curl()
    c.setopt(c.POST, 1)
    c.setopt(c.URL, "http://127.0.0.1:8080/file")
    c.setopt(c.HTTPHEADER, ["Content-Disposition: form-data; name=\"file\"; filename=\"%s\"" % fileToUpload.split('/')[-1]])
    c.setopt(c.HTTPPOST, [("file", (pycurl.FORM_FILE, fileToUpload))])
    c.setopt(c.VERBOSE, 1)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.perform()
    c.close()
    
def uploadPUT(fileToUpload):
    buf = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, "http://127.0.0.1:8080/file")
    c.setopt(c.HTTPHEADER, ["Content-Disposition: form-data; name=\"file\"; filename=\"%s\"" % fileToUpload.split('/')[-1]])
    c.setopt(c.HTTPPOST, [("file", (pycurl.FORM_FILE, fileToUpload))])
    c.setopt(c.CUSTOMREQUEST, "PUT")
    c.setopt(c.VERBOSE, 1)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.perform()
    c.close()

#uploadPUT('/home/clogeny/Desktop/haha.txt')
