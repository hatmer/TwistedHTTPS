from twisted.application import internet, service
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.python import log
from twisted.web.static import File
from twisted.web.resource import Resource
from twisted.web import server
from twisted.internet import reactor

from OpenSSL import SSL
import os
import cgi
import time

class MyResource(Resource):
    isLeaf = True

    def render_POST(self,request):
        fname = "www/uploads/" + str(time.time())
        with open(fname, 'wb') as fh:
            fh.write(request.args["file_upload"][0])

        return "done"


### INTERNALS ###

class ServeFactory(server.Site):

    def __init__(self, service):
        pagedir = os.getcwd() + "/www"
        timeout = 60*60*12
        root = File(pagedir)
        dbres = MyResource()
        root.putChild("upload",dbres)
        root.childNotFound = File(pagedir+"/404.html")
        server.Site.__init__(self, root, logPath=None, timeout=timeout)
        self.service = service

class ServeService(service.Service):

    def startService(self):
        service.Service.startService(self)

### SSL ###

class ServerContextFactory:
    def getContext(self):
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_certificate_file('keys/server.crt')
        ctx.use_privatekey_file('keys/server.key')
        return ctx


### SERVER LAUNCH ###

top_service = service.MultiService()
myservice = ServeService()
myservice.setServiceParent(top_service)

# the tcp service connects the factory to a listening socket. it will
# create the listening socket when it is started
factory = ServeFactory(myservice)

ssl_service = internet.SSLServer(443, factory, ServerContextFactory())
ssl_service.setServiceParent(top_service)

# this variable has to be named 'application'
application = service.Application("serve!")


# this hooks the collection we made to the application
top_service.setServiceParent(application)
