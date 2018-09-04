from message import Message, RMessage



# Create a login message
def login(charname, charlist_wdgid):
    msg = Message()
    #msg.type = RMessage.RMSG_WDGMSG
    msg.add_uint8(RMessage.RMSG_WDGMSG)
    msg.add_uint16(charlist_wdgid)
    msg.add_string('play')
    msg.add_list([charname])
    print(msg.buf)

    print("login: " + str(msg.buf))
    return msg

