from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.ofproto import ofproto_v1_3
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
import os

K_MINIMUM = 4

class FatTreeRyuApp(app_manager.RyuApp):
    # A Ryu app for the Fat-Tree topology

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.k = int(os.getenv('K_VALUE'))
        
        if self.k % 2 != 0 or self.k < K_MINIMUM:
            raise ValueError("k must be an even number greater than or equal to {}.".format(K_MINIMUM))

    def add_flow(self, datapath, priority, match, actions):
        # Adds a flow to the given datapath with certain priority, match, and actions. It is a general method.
        instruction = [datapath.ofproto_parser.OFPInstructionActions(datapath.ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod_msg = datapath.ofproto_parser.OFPFlowMod(datapath = datapath, priority = priority, match = match, instructions = instruction)
        datapath.send_msg(mod_msg)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def packet_features_handler(self, ev):
        """
        This method is triggered when a switch first establishes a connection with the controller and sends a 
        'features reply' message. The method identifies the type of the switch (core, aggregation, or edge) 
        based on its datapath ID and sets up the initial flow rules accordingly. It also sets up a 'table-miss' 
        flow entry with lowest priority (priority=0) that sends any unmatched packets to the controller. 
        """
        datapath = ev.msg.datapath  # Extract the datapath object from the event
        priority = 0  # Define the priority for our flow rule
        k = self.k 

        # Create a match object with no specific match fields (i.e., it will match all packets)
        match = datapath.ofproto_parser.OFPMatch()
        
        # Create an action that outputs all packets to the controller
        actions = [datapath.ofproto_parser.OFPActionOutput(datapath.ofproto.OFPP_CONTROLLER, datapath.ofproto.OFPCML_NO_BUFFER)]
        
        # Add a flow entry to the switch that matches all packets and sends them to the controller
        self.add_flow(datapath, priority, match, actions)

        # Convert the datapath ID of the switch into a 6-digit hexadecimal string
        dpid = '{:06x}'.format(datapath.id)
        self.logger.info("Switch with DPID: %s connected", dpid)

        # Extract the pod number and the switch number within the pod from the DPID
        pod_num = int(dpid[:2], 16)
        sw_num = int(dpid[-2:-4:-1], 16)