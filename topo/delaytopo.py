# -*- coding:utf-8 –*-
from mininet.topo import Topo

#               c0
#           /   |    \
#   h1 -- s1 -- s2 -- s3 -- h4
#          |           |
#         h2(delay)   h3(delay)
#



class DelayTopo(Topo):

    def __init__(self):
        super(DelayTopo, self).__init__()

        # h1 = self.addHost('h1', ip='10.0.0.1', mac='00:00:00:00:00:01')
        # h2 = self.addHost('h2', ip='10.0.0.2', mac='00:00:00:00:00:02')
        # h3 = self.addHost('h3', ip='10.0.0.3', mac='00:00:00:00:00:03')
        # h4 = self.addHost('h4', ip='10.0.0.4', mac='00:00:00:00:00:04')
        # h1 = self.addHost('h1', ip='10.0.0.1')
        # h2 = self.addHost('h2', ip='10.0.0.2')
        # h4 = self.addHost('h4', ip='10.0.0.4')

        # h1 = self.addHost('h1', ip='10.0.0.1')
        # h2 = self.addHost('h2', ip='10.0.0.2')
        # h3 = self.addHost('h3', ip='10.0.0.3')
        #
        # s1 = self.addSwitch('s1')
        #
        # self.addLink(s1, h1,1,1)
        # self.addLink(s1, h2,20,2)
        # self.addLink(s1, h3,2,3)

        h1 = self.addHost('h1', ip='10.0.0.1', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', ip='10.0.0.2', mac='00:00:00:00:00:02')
        h3 = self.addHost('h3', ip='10.0.0.3', mac='00:00:00:00:00:03')
        h4 = self.addHost('h4', ip='10.0.0.4', mac='00:00:00:00:00:04')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        self.addLink(s1, s2, 2, 1)
        self.addLink(s2, s3, 2, 2)
        self.addLink(s1, h1, 1, 1)

        self.addLink(s1, h2, 20, 1)
        self.addLink(s3, h3, 20, 1)

        self.addLink(s3, h4)

        # switches = []
        # for i in range(1, 51):
        #     newSwitch = self.addSwitch('s' + str(i))
        #     switches.append(newSwitch)
        # print len(switches)
        # h1 = self.addHost('h1', ip='10.0.0.1', mac='00:00:00:00:00:01')
        # h2 = self.addHost('h2', ip='10.0.0.2', mac='00:00:00:00:00:02')
        # h3 = self.addHost('h3', ip='10.0.0.3', mac='00:00:00:00:00:03')
        # h4 = self.addHost('h4', ip='10.0.0.4', mac='00:00:00:00:00:04')
        #
        # for i in range(1, 50):
        #     self.addLink(switches[i - 1], switches[i])
        #
        # self.addLink(switches[0], h1)
        # self.addLink(switches[0], h2, 20, 1)
        # self.addLink(switches[49], h3, 20, 1)
        # self.addLink(switches[49], h4)

        # host1 = self.addHost('h1', ip='10.0.0.1', mac='00:00:00:00:00:01')
        # host2 = self.addHost('h2', ip='10.0.0.2', mac='00:00:00:00:00:02')
        # host3 = self.addHost('h3', ip='10.0.0.3', mac='00:00:00:00:00:03')
        #
        # switch1 = self.addSwitch('s1')
        #
        # self.addLink(switch1, host1,1,1)
        # self.addLink(switch1, host2, 20,1)
        # self.addLink(switch1, host3,3,1)


topos = {'delaytopo': (lambda: DelayTopo())}
