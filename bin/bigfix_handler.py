import splunk.admin as admin
import splunk.entity as en

'''
Copyright (C) 2005 - 2010 Splunk Inc. All Rights Reserved.
Description:	This skeleton python script handles the parameters in the configuration page.
				handleList method: lists configurable parameters in the configuration page
				                   corresponds to handleractions = list in restmap.conf
				handleEdit method: controls the parameters and saves the values 
				                   corresponds to handleractions = edit in restmap.conf

'''


class ConfigApp(admin.MConfigHandler):
	'''
	Set up supported arguments
	'''
	def setup(self):
		if self.requestedAction == admin.ACTION_EDIT:
			for arg in ['url', 'user', 'password', 'soap_timeout']:
				self.supportedArgs.addOptArg(arg)
				
	'''
	Read the initial values of the parameters from the custom file myappsetup.conf
	and write them to the setup screen. 
	If the app has never been set up, uses <appname>/default/myappsetup.conf. 
	If app has been set up, looks at local/myappsetup.conf first, then looks at 
	default/myappsetup.conf only if there is no value for a field in local/myappsetup.conf

	For boolean fields, may need to switch the true/false setting
	For text fields, if the conf file says None, set to the empty string.
	'''
	def handleList(self, confInfo):
		confDict = self.readConf("bigfix")
		if None != confDict:
			for stanza, settings in confDict.items():
				for key, val in settings.items():
					if key in ['url', 'user', 'password'] and val in [None, '']:
						val = ''
					if key in ['soap_timeout'] and val in [None, '']:
						val = '90'
					confInfo[stanza].append(key, val)
					
	'''
	After user clicks Save on setup screen, take updated parameters, normalize them, and 
	save them somewhere
	'''
	def handleEdit(self, confInfo):
		name = self.callerArgs.id
		args = self.callerArgs
		
		if self.callerArgs.data['url'][0] in [None, '']:
			self.callerArgs.data['url'][0] = ''	

		if self.callerArgs.data['user'][0] in [None, '']:
			self.callerArgs.data['user'][0] = ''	

		if self.callerArgs.data['password'][0] in [None, '']:
			self.callerArgs.data['password'][0] = ''	

		if self.callerArgs.data['soap_timeout'][0] in [None, '']:
			self.callerArgs.data['soap_timeout'][0] = '90'	

		self.writeConf('bigfix', 'bigfix_config', self.callerArgs.data)
			
# initialize the handler
admin.init(ConfigApp, admin.CONTEXT_NONE)
