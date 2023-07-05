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

   