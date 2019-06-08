#!python

import os
import csv
import sys

def lookup(fields):
  f_in  = sys.stdin
  f_out = sys.stdout

  csv_in = csv.DictReader(f_in)
  csv_out = csv.DictWriter(f_out, fields)

  # Write header row
  csv_out.writerow(dict(zip(fields, fields)))

  for row in csv_in:
    scanned_count = row['scanned_count']
    passed_count  = row['passed_count']
    failed_count  = row['failed_count']

    try:
      pct = round(float(passed_count) / float(scanned_count), 4) * 100.0
      row['compliance_pct'] = pct
      csv_out.writerow(row)
    except:
      pass

if __name__ == '__main__':
  fields = ['scanned_count', 'passed_count', 'failed_count', 'compliance_pct']
  lookup(fields)
