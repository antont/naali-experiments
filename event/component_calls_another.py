"""
An example of how event feedback channels work in Circuits,
and can be used to make a component based event driven app.

This was inspired by a need with inventory services in Naali: 

It would be nice if parts of Naali like inventory impls and their
users would not be tightly coupled. The service interfaces we have now
are one solution for that, but another idea would be to just use events.

A problem with events is that how to get a reply to a query event.
For example when someone wants to know what name an asset uuid has -- 
with opensim currently assets themselves don't have names but in inventory they do,
so the viewer gui must query the inventory to be able to show them.

This is a working implementation of such a query event, with two
separate components (could be modules in Naali), Responder and a
Requester (could be Inventory and Object edit GUI, for
example). Requester sends a Query event (would be
InventoryAssetinfoQuery or so in Naali) and gets the response from the
decoupled Responder.

The solution here is to use a new feature in Circuits, feedback
channels. The event type is defined so that the success channel for it
is called 'query_success'. The return value from the handler in Responder is sent as an event on that channel, so the Requester gets it.
"""

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
