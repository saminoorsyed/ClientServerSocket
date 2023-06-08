import socket

def server():
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set socket option to reuse address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to localhost and port
    server_address = ('localhost', 1234)
    server_socket.bind(server_address)

    # Listen for connections
    server_socket.listen(1)

    print("Waiting for a connection...")

    # Accept a connection
    client_socket, client_address = server_socket.accept()
    print("Connected to:", client_address)

    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(4096).decode()

            if not data:
                break

            print("Client:", data)

            # Check if the data is '/q' to quit
            if data.strip() == "/q":
                break

            # Check if the data is 'play tic-tac-toe' to initiate the game
            if data.strip() == "play tic-tac-toe":
                # Start the Tic-Tac-Toe game
                play_tic_tac_toe(client_socket)
                continue

            # Prompt for reply
            reply = input("Enter Input > ")

            # Send the reply to the client
            client_socket.send(reply.encode())

            if reply.strip() == "play tic-tac-toe":
                # Start the Tic-Tac-Toe game
                play_tic_tac_toe(client_socket)
                continue

            # Check if the reply is '/q' to quit
            if reply.strip() == "/q":
                break

    finally:
        # Close the sockets
        client_socket.close()
        server_socket.close()

def play_tic_tac_toe(client_socket):
    # Initialize the tic-tac-toe board
    board = [' '] * 9
    possible_moves = [ "0", "1", "2", "3", "4", "5", "6", "7", "8","/q"]

    while True:
        # Receive the opponent's move
        opponent_move = client_socket.recv(4096).decode()
        if not opponent_move or opponent_move == "/q":
            break
        if opponent_move in possible_moves:
            possible_moves.remove(opponent_move)
        # Update the board with the opponent's move
        index = int(opponent_move)
        board[index] = 'O'

        # Print the updated board
        print_board(board)

        # Check if the opponent won or the board is full
        if check_winner(board, 'O'):
            print("the client won")
            break
        elif is_board_full(board):
            print("draw game")
            break


        # Prompt for a move
        reply = input("Enter Input (0-8) > ")
        # assure that the reply is an integer between 0 and 8
        while reply not in possible_moves:
            print("invalid response")
            reply = input("Enter Input (0-8) > ")
        possible_moves.remove(reply)
        # Send the move to the client
        client_socket.send(reply.encode())
        
        if reply == "/q":
            break
        
        # Update the board with the player's move
        index = int(reply)
        board[index] = 'X'

        # Check if the player won or the board is full
        if check_winner(board, 'X'):
            # Print the updated board
            print_board(board)
            print("You won!")
            break
        elif is_board_full(board):
            # Print the updated board
            print_board(board)
            print("draw game")
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
    server()
