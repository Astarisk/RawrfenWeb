// App.jsx
import React from "react";
import "./../css/main.css";

import { inject, observer} from "mobx-react";

import Login from "./views/Login"
import CharList from "./views/CharList"
import ChatBox from "./components/ChatBox"

@inject("SessionStore")
@observer
export default class App extends React.Component {
    
    render() {
        
        
        //TODO: Make this with react-router? for a proper SPA design, I'm just being lazy here for no good reason...
        if (this.props.SessionStore.page == "login"){
            return(
                <Login />)
        } else if (this.props.SessionStore.page == "charlist"){
            return(
                <CharList/>)    
        } else if (this.props.SessionStore.page == "chat"){
            return(
                <ChatBox/>)   
        } else {
            return(
            <h2>In Development</h2>)
        }
    }
}
