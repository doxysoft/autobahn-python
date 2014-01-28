###############################################################################
##
##  Copyright (C) 2014 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.wamp.protocol import WampAppSession
from autobahn.wamp.types import PublishOptions, EventDetails, SubscribeOptions



class PubSubOptionsTestBackend(WampAppSession):
   """
   An application component that publishes an event every second.
   """

   @inlineCallbacks
   def onSessionOpen(self, details):

      counter = 0
      while True:
         publication = yield self.publish('com.myapp.topic1', counter,
               options = PublishOptions(acknowledge = True, discloseMe = True))
         print("Event published with publication ID {}".format(publication))
         counter += 1
         yield sleep(1)



class PubSubOptionsTestFrontend(WampAppSession):
   """
   An application component that subscribes and receives events,
   and stop after having received 5 events.
   """

   @inlineCallbacks
   def onSessionOpen(self, details):

      self.received = 0

      def on_event(i, details = None):
         print("Got event, publication ID {}, publisher {}: {}".format(details.publication, details.publisher, i))
         self.received += 1
         if self.received > 5:
            self.closeSession()

      yield self.subscribe(on_event, 'com.myapp.topic1',
         options = SubscribeOptions(details_arg = 'details'))


   def onSessionClose(self, details):
      reactor.stop()