#!python

import os
import sys

sys.path.append(os.path.join(sys.path[0], '..', 'lib'))

from bigfix import query_runner

qr = query_runner.QueryRunner()
qr.expr = """
  (
   "fixlet_id=" & item 0 of it as string &
   " name=" & item 1 of it as string &
   " site=" & item 2 of it as string &
   " category=" & item 3 of it as string &
   " type=" & item 4 of it as string &
   " open_action_count=" & item 5 of it as string &
   " custom_flag=" & item 6 of it as string &
   " custom_site_flag=" & item 7 of it as string &
   " source_severity=" & item 8 of it as string &
   " source_fix=" & item 9 of it as string &
   " source_release_date=" & item 10 of it as string &
   " cve=" & item 16 of it as string &
   " source_id=" & item 17 of it as string &
   " scanned_count=" & item 11 of it as string &
   " passed_count=" & item 12 of it as string &
   " failed_count=" & item 13 of it as string &
   " patched_count=" & item 14 of it as string &
   " mean_time_to_patch=" & (if (nan of item 15 of it) then "" else item 15 of it as string) &
   " bigfix_server=" & item 18 of it &
   " soap_url=" & "{url}" &
   " soap_user=" & "{user}"
  ) of (
   id of item 0 of it,
   "%22" & (concatenation "%27" of (substrings separated by "%22" of name of item 0 of it)) & "%22",
   "%22" & display name of site of item 0 of it & "%22",
   (if (exists category of item 0 of it) then "%22" & category of item 0 of it & "%22" else ""),
   type of item 0 of it,
   open action count of item 0 of it,
   custom flag of item 0 of it,
   custom site flag of item 0 of it,
   (if (exists source severity of item 0 of it) then "%22" & source severity of item 0 of it & "%22" else ""),
   (if (exists source of item 0 of it) then "%22" & source of item 0 of it & "%22" else ""),
   (if (exists source release date of item 0 of it) then "%22" & source release date of item 0 of it as string & "%22" else ""),
   item 1 of it,
   item 1 of it - number of results whose (relevant flag of it = True) of item 0 of it,
   number of results whose (relevant flag of it = True) of item 0 of it,
   number of results whose (relevant flag of it = False and exists last became nonrelevant of it) of item 0 of it,
   mean of ((it / hour) of (last became nonrelevant of it - last became relevant of it) of results whose (relevant flag of it = False and exists last became nonrelevant of it) of item 0 of it),
   (if (exists cve id list of item 0 of it) then "%22" & cve id list of item 0 of it & "%22" else ""),
   (if (exists source id of item 0 of it) then "%22" & source id of item 0 of it & "%22" else ""),
   item 2 of it
  ) of (
   fixlets whose ((True)
     and (name of it as lowercase does not contain "superseded")
     and (name of it as lowercase does not contain "corrupt patch")) of item 0 of it,
   item 1 of it,
   item 2 of it
  ) of (
   it,
   number of subscribed computers of it,
   (database name of it & "," & database id of it as string) of current bes server
  )
  of bes sites whose (True)
"""
for res in qr.run():
  print res.encode('utf-8')
