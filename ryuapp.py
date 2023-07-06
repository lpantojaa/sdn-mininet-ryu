from ryu.base import app_manager
from ryu.ofproto import ofproto_v1_3
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