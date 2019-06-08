#!python

import os
import re
import sys
import logging
import threading

sys.path.append(os.path.join(sys.path[0], '..', '..'))

import suds

logging.basicConfig(level=logging.INFO)
# Uncomment these only for debugging / troubleshooting
#logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
#logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)

class BFConnector(threading.Thread):

  def __init__(self):
    self.expr = None
    threading.Thread.__init__(self)

  def connect(self, url, user, passwd, timeout=90):
    self.url    = re.sub(r'//*$', '', url) + '/?wsdl' # append the wsdl path
    self.user   = user
    self.passwd = passwd
    self.client = suds.client.Client(self.url, timeout=int(timeout))
    self.results= []

  def get_results(self):
    return self.results

  def run(self, expr = None):
    if expr == None and self.expr == None:
      raise 'Argument Error: no query expression has been defined'
    else:
      if expr == None:
        expr = self.expr

      try:
        self.results = self.client.service.GetRelevanceResult(expr.format(url=self.url, user=self.user), self.user, self.passwd)
      except:
        logging.exception('Encountered Exception in GetRelevanceResult:\n')
