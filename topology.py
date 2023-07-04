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

        # Create core switches
        for c in range(num_core_switches):
            j = c // (self.k // 2)
            i = c % (self.k // 2)
            core_switch = self.addSwitch('crSw{}'.format(c), dpid='00:00:00:00:00:{:02x}:{:02x}:{:02x}'.format(self.k, j, i))
            core_switches.append(core_switch)

        # Create pods
        for p in range(pod):
            pod_edge_switches = []
            pod_agg_switches = []
            # Create aggregation switches
            for s in range(num_agg_per_pod):
                agg_switch = self.addSwitch('agSw{}{}'.format(p, s), dpid='00:00:00:00:00:{:02x}:{:02x}:01'.format(p, s + self.k // 2))
                pod_agg_switches.append(agg_switch)

            # Create edge switches
            for s in range(num_edge_per_pod):
                edge_switch = self.addSwitch('edSw{}{}'.format(p, s), dpid='00:00:00:00:00:{:02x}:{:02x}:01'.format(p, s))
                pod_edge_switches.append(edge_switch)

                # Create hosts
                for h in range(hosts_per_edge):
                    host_id_ip = h + 2
                    host = self.addHost('h{}{}{}'.format(p, s, h), ip = '10.{}.{}.{}'.format(p, s, host_id_ip) + '/8')
                    self.addLink(host, edge_switch)
            
            edge_switches.append(pod_edge_switches)
            agg_switches.append(pod_agg_switches)

        # Create links among switches
        # Create connections of edge switches to aggregation switches
        for p in range(pod):
            for s in range(num_edge_per_pod):
                for a in range(num_agg_per_pod):
                    self.addLink(edge_switches[p][s], agg_switches[p][a])

        # Create connections of aggregation switches to core switches
        for p in range(pod):
            for a in range(num_agg_per_pod):
                for c in range(num_core_switches):
                    if (c // (self.k // 2)) == a:
                        self.addLink(agg_switches[p][a], core_switches[c])

# Add the topology to the dictionary of available topologies
topos = { 'fattree' : ( lambda k : FatTree(k)) }