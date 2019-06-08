import splunk.clilib.cli_common 

config    = splunk.clilib.cli_common.getMergedConf('bigfix')

def get_instances():
  instances = []

  for key, val in config.items():
    if key.startswith("bigfix_config"):
      if val.has_key('url') and val.has_key('user') and val.has_key('password'):
        if val['url'] != '' and val['user'] != '' and val['password'] != '':
          instances.append(val)

  return instances
