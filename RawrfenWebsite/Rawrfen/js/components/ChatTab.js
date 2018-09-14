import React from "react";
import { inject, observer} from "mobx-react";
@inject("SessionStore")
@observer
export default class ChatTab extends React.Component {
    
    onSelection = e => {
        this.props.SessionStore.focusedChat = e.target.getAttribute("chat_id")
        
    }
    
    render() {
        
        return(
            <li style={styles.TabStyle} key={this.props.chat.id} onClick={this.onSelection}>
                <div chat_id={this.props.chat.id}>{this.props.chat.name}</div>
            </li>
        )
    }
    
}


const styles =
{
    TabStyle: {
        'display':'inline-block',
        'border': '1px solid',
        'padding': '3px',
        'cursor': 'default'
    }
}