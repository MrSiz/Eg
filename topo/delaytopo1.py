from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
 
class DelayTopo( Topo ):
    "Simple topology example."
 
    def __init__( self ):
        "Create custom topo."
 
        # Initialize topology
        super(DelayTopo, self).__init__()

        #add host
        h1 = self.addHost('h1', ip='10.0.0.1', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', ip='10.0.0.2', mac='00:00:00:00:00:02')
        h3 = self.addHost('h3', ip='10.0.0.3', mac='00:00:00:00:00:03')
        h4 = self.addHost('h4', ip='10.0.0.4', mac='00:00:00:00:00:04')
        h5 = self.addHost('h5', ip='10.0.0.5', mac='00:00:00:00:00:05')
        h6 = self.addHost('h6', ip='10.0.0.6', mac='00:00:00:00:00:06')
        h7 = self.addHost('h7', ip='10.0.0.7', mac='00:00:00:00:00:07')
        h8 = self.addHost('h8', ip='10.0.0.8', mac='00:00:00:00:00:08')
	#add delayhost
	h9 = self.addHost('h9', ip='10.0.0.9')
        h10 = self.addHost('h10', ip='10.0.0.10')
        h11 = self.addHost('h11', ip='10.0.0.11')
        h12 = self.addHost('h12', ip='10.0.0.12')
        #add switch
        c1 = self.addSwitch('c1')
        c2 = self.addSwitch('c2')

        a3 = self.addSwitch('a3')
        a4 = self.addSwitch('a4')
        a5 = self.addSwitch('a5')
        a6 = self.addSwitch('a6')

        e7 = self.addSwitch('e7')
        e8 = self.addSwitch('e8')
        e9 = self.addSwitch('e9')
        e10 = self.addSwitch('e10')
        #add link between c-switch and a-switch
	self.addLink(c1, a3)
        self.addLink(c1, a4)        
        self.addLink(c1, a5)
        self.addLink(c1, a6)
        self.addLink(c2, a3)
        self.addLink(c2, a4)
        self.addLink(c2, a5)
        self.addLink(c2, a6) 
        #add link between a-switch and e-switch
        self.addLink(a3, e7)
        self.addLink(a3, e8)
        self.addLink(a4, e7)
        self.addLink(a4, e8)
        self.addLink(a5, e9)
        self.addLink(a5, e10)
        self.addLink(a6, e9)
        self.addLink(a6, e10)
        #add link between e-switch and host
	self.addLink(e7, h1 ) 
	self.addLink(e8, h3 ) 
	self.addLink(e9, h5 )
	self.addLink(e10, h7 )
        self.addLink(e7, h2 ) 
	self.addLink(e8, h4 ) 
	self.addLink(e9, h6 )
	self.addLink(e10, h8 )
	#add link between delayhost and switch
	self.addLink(e7, h9,20) 
	self.addLink(e8, h10,20) 
	self.addLink(e9, h11,20)
	self.addLink(e10, h12,20)
 
def perfTest():
    "Create network and run simple performance test"
    topo = DelayTopo()
    net = Mininet( topo=topo, controller=lambda name: RemoteController( name,     ip='127.0.0.1' ) )
    net.start()
    CLI(net)
    net.stop()
        
topos = { 'delaytopo': ( lambda: DelayTopo() ) }      
