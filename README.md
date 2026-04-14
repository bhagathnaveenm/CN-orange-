Problem Statement

Design and implement a Software Defined Networking (SDN) controller that mimics the behavior of a learning switch. The controller should dynamically learn MAC addresses of hosts, install forwarding rules in the switch, and efficiently forward packets based on learned information. The system should demonstrate controller-switch interaction using OpenFlow and allow inspection of flow tables and packet forwarding behavior.


Setup & Execution Steps
1. Install Dependencies
sudo apt update
sudo apt install mininet git python3
2. Clone POX Controller
git clone https://github.com/noxrepo/pox.git
cd pox
3. Add Custom Controller
Place custom_learning.py inside:
pox/pox/forwarding/
4. Run Controller
./pox.py forwarding.custom_learning log.level --DEBUG
5. Run Mininet Topology
sudo mn --topo single,3 --controller=remote,ip=127.0.0.1
6. Test Connectivity
mininet> pingall
7. Inspect Flow Table
sudo ovs-ofctl dump-flows s1


Expected Output
1.MAC Address Learning
Controller logs show:
Learned MAC XX:XX:XX:XX:XX:XX on port X
2.Packet Forwarding Behavior
First packet → Flooded
Subsequent packets → Direct forwarding
3.Flow Rule Installation
Flow table entries appear:
in_port=X,dl_dst=MAC → output:Y
4.Network Performance
Reduced latency after learning
Improved throughput (iperf results)
