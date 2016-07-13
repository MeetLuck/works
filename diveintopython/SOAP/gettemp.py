from SOAPpy import SOAPProxy            
url = 'http://services.xmethods.net:80/soap/servlet/rpcrouter'
namespace = 'urn:xmethods-Temperature'
server = SOAPProxy(url, namespace)
print server.getTemp('27502')
