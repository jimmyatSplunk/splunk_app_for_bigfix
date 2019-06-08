#!python

#
# The main point of this script is to store the current time for a
# query and use that stored time on the next run in order to limit results
# to only those which have occured since the last run.
#
# On the first execution of a script utilizing this class, there will
# be no stored time and so all results will be fetched.  The second run
# will have a time reference from the first, and so, if a filter has been
# supplied, the previous run time will be applied to the filter and only results
# since the first run will be fetched.
#
# Required string interpolations:
#  {url}      will be filled with the soap url
#  {user}     will be filled with the soap user
#  {prev_run} if a filter is supplied
#  {filter}   add this to your query, in the appropriate location
#
import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], '..', 'lib'))

from bigfix import web_reports_config
from bigfix.soap import bfconnector

class QueryRunner:

  def __init__(self):
    self.expr = None
    self.filter = None
    self.real_filter = None

  def run(self):
    filter = ''  # default filter is empty
    run_file = os.path.join(sys.path[0], '..', 'var', 'run', os.path.basename(sys.argv[0]) + '.done')

    # Don't run if I don't have a query expression
    if self.expr == None:
      return(0)

    # If the store exists and a filter has been supplied get the date
    # from the store and apply it to the filter
    #
    # If the store doesn't exist, we haven't done our initial load yet
    # and so that's the first thing that will run
    if os.path.exists(run_file) and self.filter != None:
      prev_run = None

      with open(run_file, 'r') as f:
        prev_run = f.read().rstrip()
        filter = self.filter.format(prev_run='"' + prev_run + '"')

    self.real_filter = filter
    res = self.query()

    # Store the current time
    with open(run_file, 'w') as f:
      f.write(time.strftime('%a, %d %b %Y %H:%M:%S %z'))

    return res

  def query(self, expr=None):
    results = []
    threads = []

    if expr:
      self.expr = expr

    # Create a new thread for each instance and execute in parallel
    for instance in web_reports_config.get_instances():
      t = bfconnector.BFConnector()
      t.expr = self.expr.format(filter=self.real_filter, url='{url}', user='{user}')
      t.connect(instance['url'], instance['user'], instance['password'], instance.get('soap_timeout', None))
      t.start()
      threads.append(t)

    # Wait for threads to complete
    for t in threads:
      t.join()

    # Get the results from each
    for t in threads:
      for i in t.get_results():
        results.append(i)
      
    return results
