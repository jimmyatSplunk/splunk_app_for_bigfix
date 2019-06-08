#!python

# This is a little helper method to extract groups and sites and join
# them as a nice 'group="group1,group2,group3"' entry
#
def join_data(evt_str, data):
  results = []

  for row in data:
    name, client_id, bigfix_server = row.split(', ')

    # For each result, if the client and server of the group are also
    # found on this client, the client is a member of the group
    if 'client_id=' + client_id + ' ' in evt_str:
      if 'bigfix_server=' + bigfix_server.replace('( ', '').replace(' )', '') + ' ' in evt_str:
        results.append(name)

  if len(results) > 0:
    return '"' + ','.join(set(results)) + '"'
  else:
    return ''
