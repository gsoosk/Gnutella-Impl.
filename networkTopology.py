from mininet.topo import Topo
from mininet.link import TCLink

class MyTopo( Topo ):
    def build( self, n = 5 ):
	hosts = []
	switch = self.addSwitch("s1")
	for i in range(0, n):
		host = self.addHost("h%s"%(i+1))
		self.addLink(host, switch, cls = TCLink)
topos = {'mytopo' : MyTopo}


