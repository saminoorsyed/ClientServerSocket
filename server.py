import socket

def start_server():
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set socket option to reuse the address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to localhost and port xxxx
    server_address = ('localhost', 1234)
    server_socket.bind(server_address)

    # Listen for connections
    server_socket.listen(1)
    print("Server is listening on {}:{}".format(*server_address))

    while True:
        # Wait for a connection
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print("Connected to:", client_address)

        # Handle the chat until the game is initiated
        while True:
            # Receive data from the client
            data = client_socket.recv(4096).decode()
            if not data:
                break

            print("Received:", data)

            # Check if the client wants to play tic-tac-toe
            if data.strip().lower() == "play tic-tac-toe":
                play_tic_tac_toe(client_socket)
                break

            # Prompt for a reply
            reply = input("Enter Input > ")

            # Send the reply to the client
            client_socket.send(reply.encode())
            if reply.strip().lower()=="play tic-tac-toe":
                play_tic_tac_toe(client_socket)
                break
            # Check if the reply is '/q' to quit
            if reply.strip() == "/q":
                break

        client_socket.close()
        print("Connection closed.")


def play_tic_tac_toe(client_socket):
    # Initialize the tic-tac-toe board
    board = [' '] * 9

    while True:
        # Receive the opponent's move
        opponent_move = client_socket.recv(4096).decode()
        if not opponent_move:
            break

        # Update the board with the opponent's move
        index = int(opponent_move)
        board[index] = 'O'

        # Check if the opponent won or the board is full
        if check_winner(board, 'O'):
            reply = "You win!"
            client_socket.send(reply.encode())
            break
        elif is_board_full(board):
            reply = "It's a draw!"
            client_socket.send(reply.encode())
            break

        # Print the updated board
        print_board(board)

        # Prompt for a move
        reply = input("Enter Input (0-8) > ")

        # Send the move to the client
        client_socket.send(reply.encode())

        # Update the board with the player's move
        index = int(reply)
        board[index] = 'X'

        # Check if the player won or the board is full
        if check_winner(board, 'X'):
            reply = "You win!"
            client_socket.send(reply.encode())
            break
        elif is_board_full(board):
            reply = "It's a draw!"
            client_socket.send(reply.encode())
            break


def print_board(board):
    print("-------------")
    for i in range(3):
        print("|", board[i * 3], "|", board[i * 3 + 1], "|", board[i * 3 + 2], "|")
        print("-------------")


def check_winner(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]  # diagonals
    ]
    for combination in winning_combinations:
        if all(board[i] == player for i in combination):
            return True
    return False


def is_board_full(board):
    return ' ' not in board


if __name__ == '__main__':
    start_server()
