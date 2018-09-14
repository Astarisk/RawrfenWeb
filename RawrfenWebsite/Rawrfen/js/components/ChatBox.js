import React from "react";
import { inject, observer} from "mobx-react";

import ChatTabBar from "./ChatTabBar"
import MessageList from "./MessageList"

@inject("SessionStore")
@observer
export default class ChatBox extends React.Component {
    onEnter = e =>
    {
        if(e.key == 'Enter'){
            var msg = {
                type: 'chat_msg',
                chat_id: this.props.SessionStore.focusedChat,
                chat_msg: e.target.value
            }
            e.target.value = ""
            
            //I only want to send a message if it has something in it.
            if(msg.chat_msg != "")
                this.props.SessionStore.ws.send(JSON.stringify(msg))    
        }
    }
    
    render() {
        return (
            <div>
            <ChatTabBar style={styles.TabBar}/>
                <div style={{ height: '30%', display: 'flex-inline', overflowY: 'scroll' }}>
                    <MessageList/>
                </div>
                <input style={styles.InputField} onKeyPress={this.onEnter}/>
            </div>
        )
    }
}

const styles = 
{
    InputField: {
        width: '100%'
    },
    MessageBox: {
        width: '100%',
        backgroundColor: 'black',
    },
    TabBar: {
        block: 'inline',
        cursor: 'pointer'
    }
}