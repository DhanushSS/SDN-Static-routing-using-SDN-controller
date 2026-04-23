from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet

log = core.getLogger()

# ======================
# SELECT MODE HERE
# ======================
MODE = 1
# 1 → h1 → only h2 allowed
# 2 → allow everything
# 3 → block all from h1

# MAC learning table
mac_to_port = {}

def _handle_ConnectionUp(event):
    log.info("Switch connected")

def _handle_PacketIn(event):
    packet = event.parsed
    if not packet.parsed:
        return

    dpid = event.connection.dpid
    in_port = event.port

    # Initialize table
    if dpid not in mac_to_port:
        mac_to_port[dpid] = {}

    # Learn source MAC
    mac_to_port[dpid][packet.src] = in_port

    # ======================
    # DESTINATION DECISION
    # ======================

    if packet.dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][packet.dst]
        dst_known = True
    else:
        out_port = of.OFPP_FLOOD
        dst_known = False

    # ======================
    # MODE LOGIC
    # ======================

    # IMPORTANT: Only enforce rules if destination is known
    if dst_known:

        # MODE 1: h1 → only h2 allowed
        if MODE == 1:
            if in_port == 1 and out_port != 2:
                log.info("MODE1 BLOCK: h1 → port %s" % out_port)
                return

        # MODE 2: allow all
        elif MODE == 2:
            pass

        # MODE 3: block all from h1
        elif MODE == 3:
            if in_port == 1:
                log.info("MODE3 BLOCK: h1 → port %s" % out_port)
                return

    # ======================
    # FORWARD PACKET
    # ======================

    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=out_port))
    event.connection.send(msg)

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)

