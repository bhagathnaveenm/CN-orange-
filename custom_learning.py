from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class LearningSwitch(object):
    def __init__(self, connection):
        self.connection = connection
        self.mac_to_port = {}

        connection.addListeners(self)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        in_port = event.port

        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        src = packet.src
        dst = packet.dst

        # 🔹 MAC Learning Logic
        self.mac_to_port[src] = in_port
        log.info("Learned MAC %s on port %s", src, in_port)

        # 🔹 Forwarding Logic
        if dst in self.mac_to_port:
            out_port = self.mac_to_port[dst]
            log.info("Forwarding %s -> %s via port %s", src, dst, out_port)

            # 🔹 Install Flow Rule
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet, in_port)
            msg.actions.append(of.ofp_action_output(port=out_port))
            self.connection.send(msg)

        else:
            out_port = of.OFPP_FLOOD
            log.info("Flooding packet %s -> %s", src, dst)

        # 🔹 Packet Out
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=out_port))
        msg.in_port = in_port
        self.connection.send(msg)


def launch():
    def start_switch(event):
        log.info("Controlling %s", event.connection)
        LearningSwitch(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
