#!python

import os
import sys

sys.path.append(os.path.join(sys.path[0], '..', 'lib'))

from bigfix import query_runner

qr = query_runner.QueryRunner()
qr.filter = 'whose (last report time of computer of it >= {prev_run} as time)'
qr.expr = """
  (
   last report time of computer of item 1 of it as string & 
   " client_id=" & (if (exists id of computer of item 1 of it) then id of computer of item 1 of it as string else "none") &
   " client_name=" & (if (exists name of computer of item 1 of it) then name of computer of item 1 of it else "none") &
   " dns_name=" & (if (exists hostname of computer of item 1 of it) then hostname of computer of item 1 of it else "none") &
   " src_ip=%22" & (if (exists ip addresses of computer of item 1 of it) then concatenation "," of (ip addresses of computer of item 1 of it as string) else "none") & "%22" &
   " user_name=%22" & concatenation "," of values of results(computer of item 1 of it, bes property "User Name") & "%22" &
   " os=%22" & (if (exists operating system of computer of item 1 of it) then operating system of computer of item 1 of it else "none") & "%22" &
   " ad_path=%22" & (if (exists active directory paths of computer of item 1 of it) then concatenation ";" of (active directory paths of computer of item 1 of it) else "none") & "%22" &
   " property_name=%22" & name of item 0 of it & "%22" &
   " property_values=%22" & concatenation "%27" of (substrings separated by "%22" of (concatenation "," of substrings separated by "%00" whose (length of it > 0) of values of item 1 of it)) & "%22" &
   " bigfix_server=" & item 2 of it &
   " soap_url=" & "{url}" &
   " soap_user=" & "{user}"
  )
  of (
   it,
   results {filter} of it,
   (database name of it & "," & database id of it as string) of current bes server
  )
  of properties of bes fixlets whose (name of it contains "Application Information")
"""
for res in qr.run():
  print res.encode('utf-8')
