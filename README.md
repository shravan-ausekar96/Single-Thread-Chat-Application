# Python Chat App (Tkinter + Sockets)

A simple chat application built in Python. It uses **Tkinter** for the graphical interface and **sockets** for client-server communication over localhost.

This project was built to learn how networking and GUIs work together in Python.

## Features

- Client-server architecture using Python's `socket` module
- Graphical chat window built with `tkinter`
- Runs locally on `localhost`, so no setup or internet is needed
- Simple, readable code that is easy to learn from and extend

## Tech Stack

- Python 3
- `tkinter` (GUI)
- `socket` (networking)

Both libraries are part of Python's standard library, so there is nothing extra to install.

## Project Structure

```
.
├── server.py    # Starts the server and handles incoming messages
├── client.py    # Chat window (GUI) that connects to the server
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Tkinter (included with most Python installs; on some Linux systems install it with `sudo apt install python3-tk`)

### Installation

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### Running the App

1. Start the server in one terminal:

   ```bash
   python server.py
   ```

2. Start the client in a second terminal:

   ```bash
   python client.py
   ```

3. Type a message in the chat window and send it.

## How It Works

1. `server.py` creates a socket, binds it to localhost, and listens for connections.
2. `client.py` opens a Tkinter window and connects to the server through a socket.
3. Messages typed in the client are sent over the socket to the server.

## Future Improvements

- Support for multiple clients at once
- Usernames and timestamps
- Message history
- Running across different machines on a network
- Better error handling when the server is unavailable

## What I Learned

- How TCP sockets work in Python
- Building GUIs with Tkinter
- Structuring a client-server program

## Author

**Shravan**
GitHub: [@shravan-ausekar96](https://github.com/shravan-ausekar96)
