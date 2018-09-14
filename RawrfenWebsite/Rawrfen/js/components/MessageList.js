import React from "react";
import { inject, observer } from "mobx-react";

@inject("SessionStore")
@observer
export default class MessageList extends React.Component {
    
    scrollToBottom = () => {
        this.messageEnd.scrollIntoView()   
    }
    
    componentDidUpdate() {
        this.scrollToBottom()
    }
    
    render () {
        
        return (
            <div>
                <ul style={styles.MessageList}>
                    {
                        //TODO: Should not use index as a key for this
                       this.props.SessionStore.filteredMessages.map((message, index) =><li style={styles.Message} key={index}>{message.msg}</li>)
                    }
                </ul>
                <div ref={(messageEnd) => {this.messageEnd = messageEnd;}}>
                </div>
            </div>
        )
        
    }
}


const styles = 
{
    Message: {
        color: 'black'
    }
}