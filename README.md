# Tic-Tac-Toe Chat Room

This repository contains code for a chat room with the functionality to play Tic-Tac-Toe game. The chat room allows two clients to connect and communicate with each other while playing the game. The game follows the standard rules of Tic-Tac-Toe, where players take turns marking spaces on a 3x3 grid until one player wins or the game ends in a draw.

## Requirements

- Python 3.x
- socket module

## Usage

1. Clone the repository:
    
    git clone https://github.com/saminoorsyed/pythonSockets.git

2. Open two terminal windows and navigate to the cloned repository in each window.

3. In one terminal window, run the server:

    python server.py

This will start the server and wait for a client to connect.

4. In the other terminal window, run the client:


This will connect the client to the server and prompt for input.

5. Start playing the Tic-Tac-Toe game:

- Type "play tictactoe" in the client or server window to initiate the game.
- The client will make the first move and prompt for input in the range of 0-8 to select a space on the board.
- The server will make its move, and the game continues until a player wins or the game ends in a draw.
- To quit the game or the chat room, type "/q" in the client window.

6. Chat between server and client terminals:

- The Server and Client take turns sending each other messages, starting with the Client
- type '/q' into the server or client terminal to terminate the chat

## How It Works

The repository contains two main files:

- `server.py`: This file implements the server-side functionality. It creates a socket, binds it to a specified address, and listens for incoming connections. Once a client connects, the server waits for messages from the client. It responds to messages and handles the Tic-Tac-Toe game logic when initiated.

- `client.py`: This file implements the client-side functionality. It creates a socket and connects to the server. The client can send messages to the server, receive replies, and interactively play the Tic-Tac-Toe game by making moves on the board.

The game logic is implemented using the `play_tic_tac_toe()` function, which manages the game flow and checks for a winner or a draw after each move.

## Citations

The implementation of the chat room and socket communication in this project were inspired by the following resources:

- "Python Sockets: An Introduction" by Real Python: [https://realpython.com/python-sockets/](https://realpython.com/python-sockets/)
- "Socket Programming HOWTO" from the Python documentation: [https://docs.python.org/3.4/howto/sockets.html](https://docs.python.org/3.4/howto/sockets.html)

Please refer to these resources for more information on socket programming in Python.

## Contributing

Contributions are welcome! If you find any issues or want to add new features, feel free to open an issue or submit a pull request. Please follow the existing code style and include appropriate tests with your changes.


