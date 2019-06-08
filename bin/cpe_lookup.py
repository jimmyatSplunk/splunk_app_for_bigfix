#!python

import re
import csv
import sys

def convert(os_str):
  cpe      = 'cpe:/o:'
  vendor   = 'unknown'
  product  = 'unknown'
  version  = ''
  revision = ''
  edition  = ''
  os_str   = re.sub(re.compile(r'\302\256|\256|\(r\)', re.IGNORECASE), '', os_str.encode('utf-8'))
  osver    = re.compile(r'.* (\d+\.?\d*\.?\d*)\s*', re.IGNORECASE).match(os_str)

  if re.compile(r'microsoft', re.IGNORECASE).search(os_str):
    vendor = 'microsoft'
    win_server = re.compile(r'.* windows server (\w+)\s*', re.IGNORECASE).match(os_str)
    win_other  = re.compile(r'.* windows (\w+)\s*', re.IGNORECASE).match(os_str)
    win_ver    = re.compile(r'.*windows.* (r\d+)\s*', re.IGNORECASE).match(os_str)
    win_rev    = re.compile(r'.* service pack (\d+)\s*', re.IGNORECASE).match(os_str)
    win_beta   = re.compile(r'.* (beta\w*)\s*', re.IGNORECASE).match(os_str)

    if win_server:
      product = 'windows_server_' + win_server.group(1).lower()
    elif win_other:
      product = 'windows_' + win_other.group(1).lower()
    else:
      product = ''

    if win_ver:
      version = win_ver.group(1).lower()
    else:
      version = ''

    if win_rev:
      revision = 'sp' + win_rev.group(1)
    elif win_beta:
      revision = win_beta.group(1).lower()
    else:
      revision = ''
      
    if re.compile(r'.* (x64|64-?bit)\s*', re.IGNORECASE).search(os_str):
      edition1 = 'x64'
    elif re.compile(r'.* (x32|32-?bit)\s*', re.IGNORECASE).search(os_str):
      edition1 = 'x32'
    else:
      edition1 = None

    if re.compile(r'.* professional\s*', re.IGNORECASE).search(os_str):
      edition2 = 'professional'
    elif re.compile(r'.* pro\s*', re.IGNORECASE).search(os_str):
      edition2 = 'pro'
    elif re.compile(r'.* embedded\s*', re.IGNORECASE).search(os_str):
      edition2 = 'embedded'
    elif re.compile(r'.* media center\s*', re.IGNORECASE).search(os_str):
      edition2 = 'media_center'
    elif re.compile(r'.* tablet\s*', re.IGNORECASE).search(os_str):
      edition2 = 'tablet_pc'
    elif re.compile(r'.* home\s*', re.IGNORECASE).search(os_str):
      edition2 = 'home'
    elif re.compile(r'.* ultimate n\s*', re.IGNORECASE).search(os_str):
      edition2 = 'ultimate_n'
    elif re.compile(r'.* ultimate\s*', re.IGNORECASE).search(os_str):
      edition2 = 'ultimate'
    elif re.compile(r'.* datacenter\s*', re.IGNORECASE).search(os_str):
      edition2 = 'datacenter'
    elif re.compile(r'.* enterprise\s*', re.IGNORECASE).search(os_str):
      edition2 = 'enterprise'
    elif re.compile(r'.* standard\s*', re.IGNORECASE).search(os_str):
      edition2 = 'standard'
    elif re.compile(r'.* storage\s*', re.IGNORECASE).search(os_str):
      edition2 = 'storage'
    elif re.compile(r'.* advanced server\s*', re.IGNORECASE).search(os_str):
      edition2 = 'advanced_server'
    elif re.compile(r'.* datacenter server\s*', re.IGNORECASE).search(os_str):
      edition2 = 'datacenter_server'
    elif re.compile(r'.* terminal server\s*', re.IGNORECASE).search(os_str):
      edition2 = 'terminal_server'
    elif re.compile(r'.* compute cluster\s*', re.IGNORECASE).search(os_str):
      edition2 = 'compute_cluster'
    elif re.compile(r'.* web\s*', re.IGNORECASE).search(os_str):
      edition2 = 'web'
    elif re.compile(r'.* hpc\s*', re.IGNORECASE).search(os_str):
      edition2 = 'hpc'
    elif re.compile(r'.* itanium\s*', re.IGNORECASE).search(os_str):
      edition2 = 'itanium'
    else:
      edition2 = None

    edition = ('-').join([e for e in [edition1, edition2] if e != None])

  
  if re.compile(r'red\s?hat', re.IGNORECASE).search(os_str):
    vendor = 'redhat'

    if re.compile(r'.* enterprise server|linux\s*', re.IGNORECASE).search(os_str):
      product = 'enterprise_linux'
    else:
      product = ''
    
    redhat_version  = re.compile(r'.* enterprise server|linux (\d+)\s*', re.IGNORECASE).match(os_str)
    redhat_revision = re.compile(r'.* enterprise server|linux .* (\w+)$', re.IGNORECASE).match(os_str)
    redhat_edition  = re.compile(r'.* enterprise server|linux \S+ (AS|ES|WS)\s*', re.IGNORECASE).match(os_str)

    if redhat_version:
      version = redhat_version.group(1)
    else:
      version = ''
    
    if redhat_revision:
      revision = redhat_revision.group(1).lower()
    else:
      revision = ''
    
    if redhat_edition:
      edition = redhat_edition.group(1).lower()
    else:
      edition = None
    

  if re.compile(r'sunos', re.IGNORECASE).search(os_str):
    vendor  = 'oracle'
    product = 'sunos'

    if osver:
      version = osver.group(1)
    else:
      version = ''
    
  if re.compile(r'ibm aix', re.IGNORECASE).search(os_str):
    vendor  = 'ibm'
    product = 'aix'

    if osver:
      version = osver.group(1)
    else:
      version = ''
    
  if re.compile(r'hp-ux', re.IGNORECASE).search(os_str):
    vendor  = 'hp'
    product = 'hp-ux'

    if osver:
      version = osver.group(1)
    else:
      version = ''
    
  if re.compile(r'suse', re.IGNORECASE).search(os_str):
    vendor  = 'novell'
    product = 'suse_linux'

    if osver:
      version = osver.group(1)
    else:
      version = ''
    
    if re.compile(r'.* desktop\s*', re.IGNORECASE).search(os_str):
      edition = 'desktop'
    elif re.compile(r'.* server\s*', re.IGNORECASE).search(os_str):
      edition = 'server'
    elif re.compile(r'.* (pro|professional)\s*', re.IGNORECASE).search(os_str):
      edition = 'pro'
    else:
      edition = None

  if re.compile(r'vmware', re.IGNORECASE).search(os_str):
    vendor  = 'vmware'
    product = 'esx_server'

    if osver:
      version = osver.group(1)
    else:
      version = ''
    
  if re.compile(r'mac os', re.IGNORECASE).search(os_str):
    vendor  = 'apple'
    product = 'max_os_x'

    if osver:
      version = osver.group(1)
    else:
      version = ''
    

  return re.sub(re.compile(r':?::$'), '', cpe + (':').join([vendor, product, version, revision, edition]))

def lookup(fields):
  f_in  = sys.stdin
  f_out = sys.stdout

  csv_in = csv.DictReader(f_in)
  csv_out = csv.DictWriter(f_out, fields)

  # Write header row
  csv_out.writerow(dict(zip(fields, fields)))

  for row in csv_in:
    row['cpe'] = convert(row['full_os'])
    csv_out.writerow(row)

if __name__ == '__main__':
  fields = ['full_os', 'cpe']
  lookup(fields)
  
