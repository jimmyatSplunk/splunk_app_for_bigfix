#!python

import os
import sys

sys.path.append(os.path.join(sys.path[0], '..', 'lib'))

from bigfix import query_runner

qr = query_runner.QueryRunner()
qr.filter = 'whose (last report time of it >= {prev_run} as time)'
qr.expr = """
  (
   last report time of item 0 of it as string &
   " client_id=" & (if (exists id of item 0 of it) then id of item 0 of it as string else "none") & 
   " client_name=" & (if (exists name of item 0 of it) then name of item 0 of it else "none") &
   " dns_name=" & (if (exists hostname of item 0 of it) then hostname of item 0 of it else "none") &
   " src_ip=%22" & (if (exists ip addresses of item 0 of it) then concatenation "," of (ip addresses of item 0 of it as string) else "none") & "%22" &
   " user_name=%22" & concatenation "," of values of results(item 0 of it, bes property "User Name") & "%22" &
   " os=%22" & (if (exists operating system of item 0 of it) then operating system of item 0 of it else "none") & "%22" &
   " ad_path=%22" & (if (exists active directory paths of item 0 of it) then concatenation ";" of (active directory paths of item 0 of it) else "none") & "%22" &
   " status=" & item 1 of it &
   " issuer=" & item 2 of it &
   " issue_time=" & item 3 of it &
   " start_time=" & item 4 of it &
   " end_time=" & item 5 of it &
   " fixlet_id=" & item 6 of it &
   " fixlet_name=" & item 7 of it &
   " fixlet_site=" & item 8 of it &
   " action_id=" & item 9 of it &
   " action_name=" & item 10 of it &
   " reapply=" & item 11 of it &
   " restart_required=" & item 12 of it &
   " stopper=" & item 13 of it &
   " time_stopped=" & item 14 of it &
   " bigfix_server=" & item 15 of it &
   " soap_url=" & "{url}" &
   " soap_user=" & "{user}"
  ) of (
   computers {filter} of item 0 of it,
   "%22" & status of item 0 of it as string & "%22",
   "%22" & name of issuer of item 2 of it & "%22",
   "%22" & time issued of item 2 of it as string & "%22",
   (if (exists end date of item 2 of it) then "%22" & end date of item 2 of it as string & " " & end time_of_day of item 2 of it as string & "%22" else ""),
   (if (exists start date of item 2 of it) then "%22" & start date of item 2 of it as string & " " & start time_of_day of item 2 of it as string & "%22" else ""),
   id of item 1 of it as string,
   "%22" & (concatenation "%27" of (substrings separated by "%22" of name of item 1 of it)) & "%22",
   "%22" & display name of site of item 1 of it & "%22",
   id of item 2 of it as string,
   "%22" & (concatenation "%27" of (substrings separated by "%22" of name of item 2 of it)) & "%22",
   reapply flag of item 2 of it as string,
   restart flag of item 2 of it as string,
   (if (exists stopper of item 2 of it) then "%22" & name of stopper of item 2 of it as string & "%22" else ""),
   (if (exists time stopped of item 2 of it) then "%22" & time stopped of item 2 of it as string & "%22" else ""),
   item 3 of it
  )
  of (results of item 0 of it, source fixlets of item 0 of it, item 0 of it, item 1 of it)
  of (bes actions, (database name of it & "," & database id of it as string) of current bes server) 
"""
for res in qr.run():
  print res.encode('utf-8')
