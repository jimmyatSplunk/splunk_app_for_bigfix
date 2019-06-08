#!python

import os
import sys

sys.path.append(os.path.join(sys.path[0], '..', 'lib'))

from bigfix import query_runner

qr = query_runner.QueryRunner()
qr.filter = """whose (if (exists last login time of it) then (last login time of it >= {prev_run} as time) else False)"""
qr.expr = """
  (
   (if (exists last login time of item 0 of it) then last login time of item 0 of it as string else creation time of item 0 of it as string) &
   " name=%22" & name of item 0 of it & "%22" &
   " master_operator=" & master flag of item 0 of it as string &
   " action_count=" & number of issued actions of item 0 of it as string &
   " creation_time=%22" & creation time of item 0 of it as string & "%22" &
   " last_login_time=" & (if (exists last login time of item 0 of it) then "%22" & last login time of item 0 of it as string & "%22" else "") &
   " bigfix_server=" & item 1 of it &
   " soap_url=" & "{url}" &
   " soap_user=" & "{user}"
  )
  of (
   bes users {filter},
   (database name of it & "," & database id of it as string) of current bes server
  )
"""
for res in qr.run():
  print res.encode('utf-8')
