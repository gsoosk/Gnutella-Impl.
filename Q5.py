import ping
from ping import Ping
from random import randint
import random
import commands
import time 
import socket
import sys
import threading 

numberOfClient = 5
protocolTag = '~'

def splitFile(fileName = 'test.txt'):
	f = open(fileName, 'rb')
	result = []
	try:
		byte = f.read(1)
		result.append(str(byte))
		while byte != "":
			byte = f.read(1)
			result.append(str(byte))
	finally:
		f.close()
	return result

def send():
	sourceIp = findRandomIp()
	destinationIp = findRandomIp()
	while destinationIp == sourceIp:
		 destinationIp = findRandomIp()
	print "from %s to %s" % (sourceIp, destinationIp)
        Server = Ping(sourceIp , destinationIp)
        Server.do_send()

def findRandomIp():   
	hostname = socket.gethostname()    
	#ip = socket.gethostbyname(hostname)
	#print ip  
	ip = commands.getoutput('/sbin/ifconfig').split('\n')[1][20:28]
	ipFounded = False
	newIpToJoin = ""
	while not ipFounded :
		newIpToJoin = randint(1, numberOfClient)
		newIpToJoin = "10.0.0." + str(newIpToJoin)
		if not newIpToJoin == ip:
			ipFounded = True

	return newIpToJoin

def senderFunction():


def main(isSender = False):
	isSender = (sys.argv[1].lower() == 'true')
	
	if(isSender):

		#fileName = raw_input("file name: ")
		
		#split file
		fileData = splitFile(fileName = 'test.txt')
		
		#send file
		i = 0
		while i < len(fileData):
			data = ''
			for j in range(i , i + 7):
				if j < len(fileData):
					data += fileData[j]
			print (data) 
			payload = '0' + protocolTag + data + protocolTag + '%s'%(i/8)
			Ping(findRandomIp() , findRandomIp() , payload = payload).do_send()
			i = i + 8
		#return home

		#receive file

	else:
		receiverFunction()
        
def receiverFunction():
	p = Ping('0.0.0.0' , '0.0.0.0', payload="test")
	returnHome = False
	returnIp = 0
	while(True):
		packet_size , src_ip, dest_ip, ip_header, icmp_header , payLoad = p.do_receive()
		if not packet_size == 0:
			payloadData = payLoad.split('~')
			if(payloadData[0] == 'return'): #If msg was return to home
				returnIp = payloadData[1]
				returnHome = True
			if(icmp_header['type'] == ping.ICMP_ECHOREPLY):
				print "PayLoad is %s"%(payLoad)
				if(payloadData[5] == '1'):
					print "***********Deleting"
				elif(returnHome and not payloadData[0] == 'return'):
					payloadData[5] = '1'
					payLoad = '~'.join(payloadData)
					print "************Sending to Home %s"%(returnIp)
					ourIp = commands.getoutput('/sbin/ifconfig').split('\n')[1][20:28];
					p.set_new_config(ourIp, returnIp, payLoad)
					# time.sleep(1)
					p.do_send()
				else : 
					sourceIp, destinationIp = getRandomSourceAndIp()
					print "random src is %s and dst is %s"%(sourceIp, destinationIp)
					p.set_new_config(sourceIp, destinationIp, payLoad)
					# time.sleep(1)
					p.do_send()
        

def getRandomSourceAndIp():
        sourceIp = findRandomIp()
        destinationIp = findRandomIp()
        while destinationIp == sourceIp :
                destinationIp = findRandomIp()
        return sourceIp, destinationIp
	
if __name__ == "__main__":
    main(isSender=False)
