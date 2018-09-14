import React from "react";
import { inject, observer} from "mobx-react";

@inject("SessionStore")
@observer
export default class CharList extends React.Component {
    
    onSelection = e => {
        //console.log(e.target.innerText)
        var msg = {
                type: "play",
                name: e.target.innerText
        }
        this.props.SessionStore.ws.send(JSON.stringify(msg))
        this.props.SessionStore.page = "chat"
    }
    
    render() {
        return (
            <div>
                <h2>Character List</h2>
                <ul>
                    <div onClick={this.onSelection}>
                    {this.props.SessionStore.characters.map(character => <li key={character}>{character}</li>)}
                    </div>
                </ul>
            </div>
        )
    }
}
