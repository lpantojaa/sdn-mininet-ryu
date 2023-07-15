# Fat-Tree Topology Generation and Routing Protocol Implementation

This repository contains a Mininet script for generating a Fat-Tree topology and a Ryu application to implement Fat-Tree's routing protocol. 

## Requirements

- [Mininet](http://mininet.org/download/)
- [Ryu Controller](https://ryu.readthedocs.io/en/latest/getting_started.html)

## How to Run

1. Start the Ryu controller with the Ryu application. In a terminal, navigate to the directory containing `ryuapp.py` and run:

    ```bash
    K_VALUE=4 ryu-manager ryuapp.py
    ```

    Note: Replace `4` with your desired value of `k`.

2. In another terminal, navigate to the directory containing `topology.py`. Start Mininet with the custom topology:

    ```bash
    mn --custom topology.py --topo fattree,4 --mac --arp --controller=remote,ip=127.0.0.1,port=6633
    ```

    Note: Replace `4` in `--topo fattree,4` with your desired value of `k`.

## Structure

- `ryuapp.py`: This is the Ryu application which implements the Fat-Tree routing protocol.
- `topology.py`: This is the Mininet script to generate a Fat-Tree topology.

## About Fat-Tree Topology

Fat-Tree is a promising topology for future Data Center Networks (DCNs). It is characterized by its hierarchical structure and its ability to grow with respect to the value of `k`. This topology is composed of `k` pods, each containing two layers of `k/2` switches. Each `k`-port switch in the lower layer (Edge) is directly connected to `k/2` hosts. Each of the remaining `k/2` ports is connected to `k/2` of the `k` ports in the Aggregation layer of the hierarchy. There are `(k/2)^2` `k`-port core switches, each has one port connected to each of `k` pods.

## About Fat-Tree Routing Protocol

The Fat-Tree routing protocol is designed to evenly distribute the traffic load among all switches. It allows two-level prefix lookup, where each entry in the main routing table has an additional pointer to a small secondary table of (suffix, port) entries. This approach enables efficient load balancing across the network.