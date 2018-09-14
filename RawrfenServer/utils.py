from message import Message, RMessage



# Create a login message
def login(charname, charlist_wdgid):
    msg = Message()
    msg.add_uint8(RMessage.RMSG_WDGMSG)
    msg.add_uint16(charlist_wdgid)
    msg.add_string('play')
    msg.add_list([charname])
    return msg

# Send a message through a chat
def send_chat_msg(chat_id, chat_msg):
    print("sending a chat message...")
    msg = Message()
    msg.add_uint8(RMessage.RMSG_WDGMSG)
    msg.add_uint16(chat_id)
    msg.add_string('msg')
    msg.add_list([chat_msg])
    return msg
