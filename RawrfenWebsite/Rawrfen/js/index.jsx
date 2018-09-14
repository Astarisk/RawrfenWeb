// index.jsx
import React from "react";
import ReactDOM from "react-dom";
import App from "./App";

import { Provider } from "mobx-react"
import SessionStore from "./SessionStore"

const Root = (
    <Provider SessionStore={SessionStore}>
        <App/>
    </Provider>
)

ReactDOM.render(Root, document.getElementById("root"));