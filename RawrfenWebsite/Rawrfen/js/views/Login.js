import React from "react";
import { inject, observer} from "mobx-react";

import sha256 from "js-sha256";

@inject("SessionStore")
@observer
export default class Login extends React.Component {
    
    constructor(props) {
        super(props)
    
        //TODO: I most likely don't need these to be a state..
        this.state = {
            username: "",
            password: ""
        };
    }
    
    onLogin = e => {
        //This stops the page from reloading when it submits
        e.preventDefault()
        
        //Connects the websocket
        this.props.SessionStore.openWebSocket()

        //Send the login info when the session is opened
        this.props.SessionStore.ws.onopen = () => {
            var hash = sha256(this.state.password)
            var msg = {
                type: "login",
                user: this.state.username,
                pw: hash
            }
            this.props.SessionStore.ws.send(JSON.stringify(msg))
        }
    }
    
    onFieldChange = e => {
        this.setState({
            [e.target.name]: e.target.value
        });
    }
    
    render () {
        return (
            <form className="login-form" onSubmit={this.onLogin}>
                <h2>Rawrfen Web Login</h2>
                <input name="username" type="username" placeholder="Username" onChange={this.onFieldChange} required autoFocus/>
                <input name="password" type="password" placeholder="Password"
                onChange={this.onFieldChange}required autoFocus/>
                <button type="submit">Login</button>
            </form>
            )
    }
}