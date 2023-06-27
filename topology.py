from mininet.topo import Topo

# Create a class for the FatTree topology
class FatTree(Topo):
    # Initialize the topology
    def __init__(self, k):
        # Validate the value of k (to be larger than 4 and even)
        if k % 2 != 0 or k < 4:
            print("Error: k must be an even number greater than or equal to 4.")
            exit(1)
        self.k = k
        super(FatTree, self).__init__()

    # Build the topology
    def build(self):
        # Define the lists of switches
        edge_switches = []
        agg_switches = []
        core_switches = []

        # Define the number of switches and hosts
        pod = self.k
        num_edge_per_pod = self.k // 2
        num_agg_per_pod = self.k // 2
        hosts_per_edge = self.k // 2
        num_core_switches = (self.k // 2) ** 2

     