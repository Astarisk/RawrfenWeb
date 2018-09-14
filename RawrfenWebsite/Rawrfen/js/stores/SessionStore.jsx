import { action, computed, observable } from "mobx"

export class SessionStore {
    //webpage data
    @observable page = "login"
    
    
    //Chat data
    @observable chats = []
    @observable messageLog = []
    @observable focusedChat = null
    
    //Websocket data
    @observable ws = null
    @observable address
    @observable port
    
    //Character Login
    @observable characters = []
    
    //Client Data
    @observable gobs = []
    
    @action addCharacter = character => {
        this.characters.push(character);
    }
    
    // TODO: I'd like to split these into seperate stores, 
    // Ideally there should be one for Websocket, Game data, and Chat.
    
    openWebSocket = (data) => {
        console.log("Connecting...")
        this.ws = new WebSocket("ws://localhost:8000/")
        //this.ws.onopen = this.onOpen
        this.ws.onmessage = this.onMessage
    }
    
    closeWebSocket = () => {
        console.log("Closing connection...")
    }
    
    onOpen = (username, password) => {
        var msg = {
            type: "login",
            user: username,
            pw: password
        }
        this.ws.send(JSON.stringify(msg))
    }
    
    onMessage = (e) => {
        var msg = JSON.parse(e.data)
        console.log(msg)
        console.log(msg.type)
        
        if (msg.type == undefined){
            console.log("Recieved an undefined message.")
            return
        }

        if(msg.type == 'login') {
            if (msg.success){
                console.log("logged in succesfully")
                this.page = "charlist"
            }
            else
                console.log("failed to login.")
        }
        
        if(msg.type == "char_add"){
            console.log("Adding to charlist: " + msg.name)
            this.characters.push(msg.name)
        }
        
        if (msg.type == "chat_add") {
            console.log(msg)
            this.addChat(msg)
        }
        
        if (msg.type == "chat_msg"){
            console.log(msg)
            this.addMessage(msg)
        }
    }
    
    // Chat Related Functions
    addChat = chat => {
        console.log("adding chat: " + chat)
        if(this.focusedChat == null)
            this.focusedChat = chat.id
        this.chats.push(chat);
    }
    
    addMessage = message => {
        this.messageLog.push(message);
    }
    
    @computed get filteredMessages() {
        return this.messageLog.filter(message => message.chat_id == this.focusedChat)
    }
}

var store = window.store = new SessionStore
export default store
