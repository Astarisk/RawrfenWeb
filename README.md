# RawrfenWeb

An experimental browser interface for **Haven & Hearth**, connecting a React chat UI to the game's protocol through a Python WebSocket bridge.

The original idea was a MUD-like interface for playing through chat commands. This is an older, incomplete experiment: the repository contains both the Python bridge and an initial browser UI, not a complete playable web client.

## How it fits together

```text
React / MobX browser UI
        | WebSocket messages
        v
Python bridge
        | authentication and game-session protocol
        v
Haven & Hearth server
```

- **`RawrfenServer/`** implements authentication, binary message encoding/decoding, game sessions, object-state handling, and translation of UI/chat messages for the browser.
- **`RawrfenWebsite/Rawrfen/`** contains the React/MobX frontend, with login, character-selection, and chat views, plus Webpack/Babel configuration.
- **`RawrfenServer/main.py`** handles the browser's `login`, `play`, and `chat_msg` messages through `SimpleWebSocketServer`.

## Exploring the source

Start with [main.py](RawrfenServer/main.py), [session.py](RawrfenServer/session.py), and [message.py](RawrfenServer/message.py) for the bridge. [App.jsx](RawrfenWebsite/Rawrfen/js/App.jsx) selects the browser views, and [SessionStore.jsx](RawrfenWebsite/Rawrfen/js/stores/SessionStore.jsx) handles WebSocket and chat state.

The frontend package defines `build`, `dev-build`, and `watch` scripts. Its `test` script is a placeholder. The Python entry point imports `SimpleWebSocketServer`; there is no pinned Python dependency file.

## Historical setup assumptions

- The browser connects to `ws://localhost:8000/`; the Python server listens on port 8000.
- Game and authentication endpoints are configured in `RawrfenServer/config.py`.
- The authentication code expects an `authsrv.crt` file that is not included in this checkout.
- `App.jsx` imports a CSS file that is also absent from the checkout, so the frontend source needs that restored or the import revised before rebuilding.

This snapshot has not been checked against the current game protocol or current dependencies. The bridge logs incoming messages, including login payloads, and uses an unencrypted browser WebSocket by default; those paths need attention before using real credentials or exposing it beyond a local development environment.

The useful history here is the protocol and browser-bridge experiment. A full game interface and command-driven gameplay remained the longer-term goal.
