import httplib, urllib, urllib2
import xml.etree.ElementTree as ET
class nsConnection:
	def __init__(self, user, passport, acc):
		self.password = passport
		self.account = acc
		self.user = user
		self.lastRequest = None
		self.lastResponse = None
		self.lastResponseData = None
		self.ENDPOINTURL = 'https://webservices.netsuite.com/services/NetSuitePort_2013_2'
		self.header = '<soapenv:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"> <soapenv:Header> <ns1:passport soapenv:mustUnderstand="0" soapenv:actor="http://schemas.xmlsoap.org/soap/actor/next" xmlns:ns1="urn:messages_2012_2.platform.webservices.netsuite.com"> <ns2:email xmlns:ns2="urn:core_2012_2.platform.webservices.netsuite.com">'+self.user+'</ns2:email> <ns3:password xmlns:ns3="urn:core_2012_2.platform.webservices.netsuite.com">'+self.password+'</ns3:password> <ns4:account xmlns:ns4="urn:core_2012_2.platform.webservices.netsuite.com">'+self.account+'</ns4:account> <ns5:role internalId="3" xmlns:ns5="urn:core_2012_2.platform.webservices.netsuite.com" /> </ns1:passport> <ns6:applicationInfo soapenv:mustUnderstand="0" soapenv:actor="http://schemas.xmlsoap.org/soap/actor/next" xmlns:ns6="urn:messages_2012_2.platform.webservices.netsuite.com"> <ns6:applicationId>100401</ns6:applicationId> </ns6:applicationInfo> </soapenv:Header> '
	def __connect(self, apiName, data):
		#create a request
		headers = {'SOAPAction' : apiName};
		req = urllib2.Request(self.ENDPOINTURL, (self.header+data+'</soapenv:Envelope>'), headers)
		self.lastRequest = req
		try:
			response =  urllib2.urlopen(req)
			self.lastResponse = response
			self.lastResponseData = response.read()
			if(response.code == 200):
				return True
			else:
				print self.getErrorFromResponse()
				return False
		except urllib2.HTTPError as e:
			self.lastResponseData = e.read()
			self.lastResponse = e
			print self.getErrorFromResponse()
			return False
	def testConnection(self):
		str    = '<soapenv:Body> <getServerTime xmlns="urn:messages_2012_2.platform.webservices.netsuite.com"/> </soapenv:Body>';
		return self.__connect('getServerTime',str);
	def getErrorFromResponse(self):
		try:
			tree = ET.fromstring( self.lastResponseData )
			if len(tree.findall('.//faultstring')) > 0:
				return tree.findall('.//faultstring')[0].text
			else:
				return None
		except ET.ParseError as e:
			return e.message

ns = nsConnection('tarun.gupta@celigo.com','******','******')
ns.testConnection()