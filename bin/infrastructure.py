#!python

import os
import sys

sys.path.append(os.path.join(sys.path[0], '..', 'lib'))

from bigfix import query_runner

qr = query_runner.QueryRunner()
qr.filter = 'whose (last report time of it >= {prev_run} as time)'
qr.expr = """
  (
   item 0 of it &
   " client_id=" & item 1 of it &
   " client_name=" & item 2 of it &
   " dns_name=" & item 4 of it &
   " src_ip=%22" & item 3 of it & "%22" &
   " os=%22" & item 5 of it & "%22" &
   " ad_path=%22" & item 6 of it & "%22" &
   " actionsite_size=%22" & item 7 of it & "%22" &
   " actionsite_version=" & item 8 of it &
   " relay_free_space=" & item 9 of it &
   " filldb_logfile_size=%22" & item 10 of it & "%22" &
   " bufferdir_file_count=" & item 11 of it &
   " registration_list_size=" & item 12 of it &
   " bigfix_server=" & item 13 of it &
   " soap_url=" & "{url}" &
   " soap_user=" & "{user}"
  ) of (
   last report time of item 0 of it as string,
   (if (exists id of item 0 of it) then id of item 0 of it as string else "none"),
   (if (exists name of item 0 of it) then name of item 0 of it as string else "none"),
   (if (exists ip addresses of item 0 of it) then concatenation "," of (ip addresses of item 0 of it as string) else "none"),
   (if (exists hostname of item 0 of it) then hostname of item 0 of it as string else "none"),
   (if (exists operating system of item 0 of it) then operating system of item 0 of it as string else "none"),
   (if (exists active directory paths of item 0 of it) then concatenation ";" of (active directory paths of item 0 of it as string) else "none"),
   values of results(item 0 of it, bes property "BES Health Checks::Actionsite Size"),
   values of results(item 0 of it, bes property "BES Health Checks::Actionsite Version"),
   (if (value of result(item 0 of it, bes property "BES Health Checks::BES Relay Free Disk Space") = "N/A") then "" else (value of result(item 0 of it, bes property "BES Health Checks::BES Relay Free Disk Space"))),
   values of results(item 0 of it, bes property "BES Health Checks::FillDB Log File Size"),
   values of results(item 0 of it, bes property "BES Health Checks::Number of Files in FillDB Bufferdir"),
   values of results(item 0 of it, bes property "BES Health Checks::Registration List Size"),
   item 1 of it
  ) of (
   bes computers {filter},
   (database name of it & "," & database id of it as string) of current bes server
  )
"""
for res in qr.run():
  print res.encode('utf-8')
