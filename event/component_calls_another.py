from circuits import Debugger
from circuits import Event, Component

class Query(Event):
    success = ("query_success",) #channel for success replies, target omitted

class Responder(Component):
    def query(self, param):
        return "Reply to query '%s'" % param

class Requester(Component):
    def make_query(self):
        self.push(Query("hello"))

    def query_success(self, evt, handler, retval):
        print "Requester got query response: %s" % retval
        raise SystemExit, 0 #the thing worked, we're done!

req = Requester()
system = req + Responder() #+ Debugger()
req.make_query()
system.run(1)

"""output:
Requester got query response: Reply to query 'hello'
"""
