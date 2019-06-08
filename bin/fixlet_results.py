#!python

import os
import sys

sys.path.append(os.path.join(sys.path[0], '..', 'lib'))

from bigfix import query_runner

qr = query_runner.QueryRunner()
qr.filter = 'whose (first became relevant of it >= {prev_run} as time or last became relevant of it >= {prev_run} as time or last became nonrelevant of it >= {prev_run} as time)'
qr.expr = """
  (
   last report time of computer of item 0 of it as string &
   " client_id=" & (if (exists id of computer of item 0 of it) then id of computer of item 0 of it as string else "none") &
   " client_name=" & (if (exists name of computer of item 0 of it) then name of computer of item 0 of it else "none") &
   " dns_name=" & (if (exists hostname of computer of item 0 of it) then hostname of computer of item 0 of it else "none") &
   " src_ip=%22" & (if (exists ip addresses of computer of item 0 of it) then concatenation "," of (ip addresses of computer of item 0 of it as string) else "none") & "%22" &
   " user_name=%22" & concatenation "," of values of results(computer of item 0 of it, bes property "User Name") & "%22" &
   " os=%22" & (if (exists operating system of computer of item 0 of it) then operating system of computer of item 0 of it else "none") & "%22" &
   " ad_path=%22" & (if (exists active directory paths of computer of item 0 of it) then concatenation ";" of (active directory paths of computer of item 0 of it) else "none") & "%22" &
   " type=" & type of fixlet of item 0 of it &
   " open_action_count=" & open action count of fixlet of item 0 of it as string &
   " custom_flag=" & custom flag of fixlet of item 0 of it as string &
   " custom_site_flag=" & custom site flag of fixlet of item 0 of it as string &
   " source_severity=" & (if (exists source severity of fixlet of item 0 of it) then "%22" & source severity of fixlet of item 0 of it & "%22" else "") &
   " source_fix=" & (if (exists source of fixlet of item 0 of it) then "%22" & source of fixlet of item 0 of it & "%22" else "") &
   " source_release_date=" & (if (exists source release date of fixlet of item 0 of it) then "%22" & source release date of fixlet of item 0 of it as string & "%22" else "") &
   " fixlet_id=" & id of fixlet of item 0 of it as string &
   " fixlet_name=%22" & (concatenation "%27" of (substrings separated by "%22" of name of fixlet of item 0 of it)) & "%22" &
   " fixlet_site=%22" & display name of site of fixlet of item 0 of it & "%22" &
   " relevant=" & relevant flag of item 0 of it as string &
   " first_relevant_time=" & (if (exists first became relevant of item 0 of it) then "%22" & first became relevant of item 0 of it as string & "%22" else "") &
   " last_relevant_time=" & (if (exists last became relevant of item 0 of it) then "%22" & last became relevant of item 0 of it as string & "%22" else "") &
   " last_nonrelevant_time=" & (if (exists last became nonrelevant of item 0 of it) then "%22" & last became nonrelevant of item 0 of it as string & "%22" else "") &
   " cve=" & (if (exists cve id list of fixlet of item 0 of it) then "%22" & cve id list of fixlet of item 0 of it & "%22" else "") &
   " source_id=" & (if (exists source id of fixlet of item 0 of it) then "%22" & source id of fixlet of item 0 of it & "%22" else "") &
   " bigfix_server=" & item 1 of it &
   " soap_url=" & "{url}" &
   " soap_user=" & "{user}"
  )
  of (
   results {filter} of bes fixlets,
   (database name of it & "," & database id of it as string) of current bes server
  )
"""
for res in qr.run():
  print res.encode('utf-8')
