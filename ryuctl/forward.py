from ryu.base import app_manager
from ryu.ofproto import ofproto_v1_3, ofproto_v1_3_parser
from ryu.controller.handler import set_ev_cls
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller import ofp_event
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.topology import event
from ryu.lib.packet import ether_types
from ryu.topology.api import get_switch, get_link
import networkx as nx
from ryu.lib.packet import arp
from ryu.lib.packet import icmp


class ShortestForwarding(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(ShortestForwarding, self).__init__(*args, **kwargs)
        self.topology_api_app = self
        self.network = nx.DiGraph()
        self.paths = {}
        self.switch_id_to_dp = {}
        self.ingraph = {}
        self.vis = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_feature_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        ofp_parser = datapath.ofproto_parser
        self.switch_id_to_dp.setdefault(datapath.id, datapath)

        match = ofp_parser.OFPMatch()
        actions = [ofp_parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                              ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        match = ofp_parser.OFPMatch(eth_type=0x0806, in_port=20)
        actions=[]
        self.add_flow(datapath, 10, match, actions)



    def add_flow(self, datapath, priority, match, actions):
        print "datapath", datapath
        ofproto = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        inst = [ofp_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                                 actions)]
        mod = ofp_parser.OFPFlowMod(
            datapath=datapath, priority=priority, match=match, instructions=inst)
        datapath.send_msg(mod)

    events = [event.EventSwitchEnter,
              event.EventSwitchLeave,
              event.EventPortAdd,
              event.EventPortDelete,
              event.EventPortModify,
              event.EventLinkAdd,
              event.EventLinkDelete]
    @set_ev_cls(events)
    def get_topology(self, ev):
        print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        switch_list = get_switch(self.topology_api_app, None)
        switches = [switch.dp.id for switch in switch_list]
        self.network.add_nodes_from(switches)

        links_list = get_link(self.topology_api_app, None)
        links = [(link.src.dpid, link.dst.dpid, {'port': link.src.port_no})
                 for link in links_list]
        self.network.add_edges_from(links)

        links = [(link.dst.dpid, link.src.dpid, {'port': link.dst.port_no})
                 for link in links_list]
        print "links = ", links
        self.network.add_edges_from(links)

    def get_out_port(self, datapath, src, dst, in_port):
        dpid = datapath.id
        if src not in self.network:
            self.network.add_node(src)
            self.network.add_edge(dpid, src, port=in_port)
            self.network.add_edge(src, dpid)
            self.paths.setdefault(src, {})

        if dst in self.network:
            if dst not in self.paths[src]:
                path = nx.shortest_path(self.network, src, dst)
                self.paths[src][dst] = path

            path = self.paths[src][dst]
            next_hop = path[path.index(dpid) + 1]
            out_port = self.network[dpid][next_hop]['port']
            print("path: ", path)
        else:
            out_port = datapath.ofproto.OFPP_FLOOD
        return out_port

    def add_node(self, datapath, src,  in_port):
        dpid = datapath.id
        if src not in self.network:
            print "adding node ip: ", src
            self.network.add_node(src)
            self.network.add_edge(dpid, src, port=in_port)
            self.network.add_edge(src, dpid)
            self.paths.setdefault(src, {})

    def get_path(self, src, dst, datapath):
        dpid = datapath.id
        if dst in self.network:
            if dst not in self.paths[src]:
                path = nx.shortest_path(self.network, src, dst)
                self.paths[src][dst] = path
            path = self.paths[src][dst]
            next_hop = path[path.index(dpid) + 1]
            out_port = self.network[dpid][next_hop]['port']
            return path
        return []


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        in_port = msg.match["in_port"]
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        arppart = pkt.get_protocol(arp.arp)
        icmppart = pkt.get_protocol(icmp.icmp)

        if in_port == 20:
            return ;


        if eth.ethertype == ether_types.ETH_TYPE_IPV6:
            return

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return

        if icmppart is not None:
            print "code = ", icmppart.code
            print "data = ", icmppart.data

        out_port = ofproto.OFPP_FLOOD
        if arppart is not None:
            dst_mac = arppart.dst_mac
            print "========================================="
            print "dst_mac: ", dst_mac
            self.vis.setdefault(arppart.src_ip, {})
            if arppart.dst_ip in self.vis[arppart.src_ip]:
                flag = False
            else:
                self.vis[arppart.src_ip][arppart.dst_ip] = True
                print "vis path"
                flag = True
            if not self.ingraph.get(eth.src, False):
                self.add_node(datapath, arppart.src_ip, in_port)
                self.ingraph[eth.src] = True

            path = []
            path2 = []
            if eth.dst != 'ff:ff:ff:ff:ff:ff':
                path = self.get_path(arppart.src_ip, arppart.dst_ip, datapath)
                path2 = self.get_path(arppart.dst_ip, arppart.src_ip, datapath)
                print "path2 = ", path2

            if len(path) and flag:
                next_hop = path[path.index(datapath.id) + 1]
                print "path is ", path
                temp_out_port = self.network[datapath.id][next_hop]['port']
                print "temp_out_port = ", temp_out_port

                # in_port = self.network[datapath]

                match = ofp_parser.OFPMatch(eth_type=0x0800, in_port=in_port,
                                            ipv4_src=arppart.src_ip, ipv4_dst=arppart.dst_ip)
                actions = [ofp_parser.OFPActionOutput(20)]
                self.add_flow(datapath, 20, match, actions)

                match = ofp_parser.OFPMatch(eth_type=0x0800, in_port=20,
                                            ipv4_src=arppart.src_ip, ipv4_dst=arppart.dst_ip)
                actions = [ofp_parser.OFPActionOutput(temp_out_port)]
                self.add_flow(datapath, 20, match, actions)

                # src->dst
                index = 2
                temp_id = datapath.id
                print "which switch now ", temp_id
                cnt = len(path)
                while index < cnt - 1:
                    print "where ", path[index]
                    temp_id = path[index]
                    next_hop = path[index + 1]
                    # print
                    # print
                    print  " temp_id: ", temp_id, " next_hop: ", next_hop
                    temp_out_port = self.network[temp_id][next_hop]['port']
                    print " out_port: ", temp_out_port
                    match = ofp_parser.OFPMatch(eth_type=0x0800,
                                    ipv4_src=arppart.src_ip, ipv4_dst=arppart.dst_ip)
                    actions = [ofp_parser.OFPActionOutput(temp_out_port)]
                    self.add_flow(self.switch_id_to_dp[temp_id], 10, match, actions)
                    index += 1
                    # temp_id = (int)(path[index])

            if len(path2) and flag:
                now = 1
                now_switch_id = path2[now]
                next_hop = path2[now + 1]

                temp_in_port = self.network[now_switch_id][arppart.dst_ip]['port']
                print "temp_in_port: ", temp_in_port
                temp_out_port = self.network[now_switch_id][next_hop]['port']
                match = ofp_parser.OFPMatch(eth_type=0x0800, in_port=temp_in_port,
                                            ipv4_src=arppart.dst_ip, ipv4_dst=arppart.src_ip)
                actions = [ofp_parser.OFPActionOutput(20)]
                self.add_flow(self.switch_id_to_dp[now_switch_id], 20, match, actions)

                match = ofp_parser.OFPMatch(eth_type=0x0800, in_port=20,
                                            ipv4_src=arppart.dst_ip, ipv4_dst=arppart.src_ip)
                actions = [ofp_parser.OFPActionOutput(temp_out_port)]
                self.add_flow(self.switch_id_to_dp[now_switch_id], 20, match, actions)




                index = 2
                cnt = len(path2)
                while index < cnt - 1:
                    print "where ", path2[index]
                    temp_id = path2[index]
                    next_hop = path2[index + 1]
                    print "temp_id: ", temp_id, " next_hop: ", next_hop
                    temp_out_port = self.network[temp_id][next_hop]['port']
                    print "out_port ", temp_out_port
                    match = ofp_parser.OFPMatch(eth_type=0x0800,
                                                ipv4_src=arppart.dst_ip, ipv4_dst=arppart.src_ip)
                    actions = [ofp_parser.OFPActionOutput(temp_out_port)]
                    self.add_flow(self.switch_id_to_dp[temp_id], 10, match, actions)
                    index += 1

            print "========================================="


        print "e"
        print "leave the controller "
        print "datapath.id ", datapath.id
        # out_port = self.get_out_port(datapath, eth.src, eth.dst, in_port)
        actions = [ofp_parser.OFPActionOutput(out_port)]
        #
        # if out_port != ofproto.OFPP_FLOOD:
        #     match = ofp_parser.OFPMatch(in_port=in_port, eth_dst = eth.dst)
        #     self.add_flow(datapath, 1, match, actions)
        #
        out = ofp_parser.OFPPacketOut(
            datapath=datapath, buffer_id = msg.buffer_id, in_port=in_port, actions=actions
        )
        datapath.send_msg(out)