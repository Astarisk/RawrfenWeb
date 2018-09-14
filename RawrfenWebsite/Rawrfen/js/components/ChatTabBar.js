import React from "react";
import { inject, observer} from "mobx-react";

import ChatTab from "./ChatTab"

@inject("SessionStore")
@observer
export default class ChatTabBar extends React.Component {
    render() {
        return (
            <div>
                <ul>
                    {
                       this.props.SessionStore.chats.map(chat =><ChatTab chat={chat}/>)
                    }
                </ul>
            </div>
        )
    }
}