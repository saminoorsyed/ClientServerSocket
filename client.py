import socket

def client():
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    server_address = ('localhost', 1234)
    client_socket.connect(server_address)
    # use try in case there are any errors
    try:
        while True:
            # Prompt for message
            message = input("Enter Input > ")

            # Check if the message is '/q' to quit
            if message.strip() == "/q":
                break

            # Check if the message is 'play tic-tac-toe' to initiate the game
            if message.strip() == "play tic-tac-toe":
                # Send the message to the server
                client_socket.send(message.encode())
                # Start the Tic-Tac-Toe game
                play_tic_tac_toe(client_socket)
                continue

            # Send the message to the server
            client_socket.send(message.encode())

            # Receive the reply from the server
            reply = client_socket.recv(4096).decode()
            print("Server:", reply)

            if reply.strip() == "play tic-tac-toe":
                # Start the Tic-Tac-Toe game
                play_tic_tac_toe(client_socket)
                continue

    finally:
        # Close the socket
        client_socket.close()

def play_tic_tac_toe(client_socket):
    # Initialize the tic-tac-toe board
    board = [' '] * 9
    possible_moves = [ "0", "1", "2", "3", "4", "5", "6", "7", "8","/q"]
    while True:
        # Print the current board
        print_board(board)

        # Prompt for a move
        reply = input("Enter Input (0-8) > ")
        # assure that the reply is an integer between 0 and 8
        while reply not in possible_moves:
            print("invalid response")
            reply = input("Enter Input (0-8) > ")
        
        possible_moves.remove(reply)
        # Send the move to the server
        client_socket.send(reply.encode())
        if reply == "/q":
            break
        # Update the board with the player's move
        index = int(reply)

        board[index] = 'X'

        # Check if the player won or the board is full
        if check_winner(board, 'X'):
            print_board(board)
            print("you won!")
            break
        elif is_board_full(board):
            print("draw game")
            break

        # Receive the opponent's move
        opponent_move = client_socket.recv(4096).decode()
        if not opponent_move or opponent_move == "/q":
            break
        # remove opponent move from possible moves
        if opponent_move in possible_moves:
            possible_moves.remove(opponent_move)
        # Update the board with the opponent's move
        index = int(opponent_move)
        board[index] = 'O'
        print_board(board)
        # Check if the opponent won or the board is full
        if check_winner(board, 'O'):
            print("the server won!")
            break
        elif is_board_full(board):
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
    client()
