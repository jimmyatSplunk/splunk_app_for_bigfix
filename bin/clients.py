#!python

import os
import sys

sys.path.append(os.path.join(sys.path[0], '..', 'lib'))

from bigfix import query_runner, helpers

qr = query_runner.QueryRunner()

# Do a straight query to get groups because I'm not good enough with
# relevance to do it within the query above
# Do this first because we store the time after the next (big/main) query
# and it's better if the query completes and we store the time immediately to
# avoid gaps.
groups = qr.query("""
  (
   name of item 0 of it,
   ids of members of item 0 of it as string,
   item 1 of it
  ) of (
   bes computer groups,
   (database name of it & "," & database id of it as string) of current bes server
  )
""")

# In bigfix version 8, you can simply use the relevance below, but
# not in version 7, so we'll make a separate query instead for all
# the same reasons as we did for groups.  Why didn't this always exist???
#   " site=%22" & concatenation "," of display names of subscribed sites of item 0 of it & "%22" &
sites = qr.query("""
  (
   name of item 0 of it,
   ids of subscribed computers of item 0 of it as string,
   item 1 of it
  ) of (
   bes sites,
   (database name of it & "," & database id of it as string) of current bes server
  )
""")

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
   " full_os=%22" & concatenation "," of unique values of (values of (results (bes property "Full Operating System Name and Service Pack Level - Windows", it); results (bes property "OS Name - Unix", it); results (bes property "OS Name - Mac OS X", it)) of item 0 of it) & "%22" &
   " ad_path=%22" & (if (exists active directory paths of item 0 of it) then concatenation ";" of (active directory paths of item 0 of it) else "none") & "%22" &
   " site=$SITE$" &
   " group=$GROUP$" &
   " client_version=" & value of result(item 0 of it, bes property "BES Client Version") &
   " client_admin=%22" & (if (exists administrators of item 0 of it) then concatenation "," of (names of administrators of item 0 of it) else "none") & "%22" &
   " relay_server=%22" & (if (exists relay server of item 0 of it) then relay server of item 0 of it else "none") & "%22" &
   " relay_distance=" & (if (exists relay distance of item 0 of it) then relay distance of item 0 of it as string else "none") &
   " relay_selection_method=" & (if (exists relay selection method of item 0 of it) then relay selection method of item 0 of it else "none") &
   " is_relay=" & (if (exists relay server flag of item 0 of it) then relay server flag of item 0 of it as string else "none") &
   " relay_version=" & (if (value of result(item 0 of it, bes property "BES Relay Version") = "Not Installed") or (value of result(item 0 of it, bes property "BES Relay Version") = "N/A") then "" else (value of result(item 0 of it, bes property "BES Relay Version"))) &
   " server_version=" & (if (value of result(item 0 of it, bes property "BES Server Version") = "Not Installed") or (value of result(item 0 of it, bes property "BES Server Version") = "N/A") then "" else (value of result(item 0 of it, bes property "BES Server Version"))) &
   " bigfix_server=" & item 1 of it &
   " soap_url=" & "{url}" &
   " soap_user=" & "{user}"
  )
  of (
   bes computers {filter},
   (database name of it & "," & database id of it as string) of current bes server
  )
"""
for res in qr.run():
  print res.replace('$GROUP$', helpers.join_data(res, groups)
          ).replace('$SITE$', helpers.join_data(res, sites)
          ).encode('utf-8')
