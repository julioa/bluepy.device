import struct
import binascii

# HCI Events

E_DISCONN_COMPLETE = 0x05
E_ENCRYPT_CHANGE = 0x08
E_CMD_RESPONSE = 0x0E
E_CMD_STATUS = 0x0F
E_LE_META_EVENT = 0x3E

# LE Meta-event subcodes

E_LE_CONN_COMPLETE = 0x01
E_LE_CONN_UPDATE_COMPLETE = 0x03

def eventMask(evtList):
    w=0
    for e in evtList:
        assert(e > 0)
        w |= (1 << (e-1))
    return w

DEFAULT_EVENT_MASK = eventMask([E_DISCONN_COMPLETE, E_ENCRYPT_CHANGE, E_CMD_RESPONSE, E_CMD_STATUS, E_LE_META_EVENT])

DEFAULT_LE_EVENT_MASK = eventMask([E_LE_CONN_COMPLETE, E_LE_CONN_UPDATE_COMPLETE])

class EventHandler:
    # This is basically a mixin to do the event-handling portion of 
    # the main Device class. Kept separate to aid reuse.

    def onEventReceived(self, data):
        eventCode = data[0]
        dlen = data[1]
        if len(data) != dlen+2:
            print ("Invalid length %d in packet: %s" % (dlen, binascii.b2a_hex(data).decode('ascii')))
            return
        if eventCode == E_CMD_RESPONSE:
            (n_cmds, opcode) = struct.unpack("<BH", data[2:5])
            self.onCommandResponse(n_cmds, opcode, data[5:])
        else:
            print ("Unhandled event")

    # Stub event handlers   
    def onCommandResponse(self, n_cmds, opcode, params):
        pass


