import socket

def client():
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    server_address = ('localhost', 2222)
    client_socket.connect(server_address)
    
    # print directions for chat
    print("connection accepted, you (the client) talk first")
    print("type 'play tictactoe' to play game, '/q' to exit the chat")

    # use try in case there are any errors
    try:
        while True:
            # Prompt for message
            message = input("Enter Input > ")

            # Check if the message is '/q' to quit
            if message.strip() == "/q":
                break

            # Check if the message is 'play tic-tac-toe' to initiate the game
            if message.strip() == "play tictactoe":
                # Send the message to the server so that it starts the game too
                client_socket.send(message.encode())
                play_tic_tac_toe(client_socket)
                print("game over, client talks first")
                continue

            # Send the message to the server
            client_socket.send(message.encode())

            # Receive the reply from the server
            reply = client_socket.recv(4096).decode()
            print("Server:", reply)

            # if the server quits, the client also quits
            if reply.strip() =="/q":
                break

            # if the server starts a game, start the game on the client side too
            if reply.strip() == "play tictactoe":
                # Start the Tic-Tac-Toe game
                play_tic_tac_toe(client_socket)
                continue

    finally:
        # Close the socket
        client_socket.close()
        print("sockets are now closed")


def play_tic_tac_toe(client_socket):
    
    # Initialize the tic-tac-toe board
    board = [' '] * 9
    possible_moves = [ "0", "1", "2", "3", "4", "5", "6", "7", "8","/q"]
    
    # print directions
    print("choose space 0-8 to make your move. The Client always goes first")
    print("if you want to quit, just enter '/q' ")
    print_board(board)
    while True:
        # Prompt for a move
        reply = input("Enter Input (0-8) > ")
        
        # validate that the reply is an integer between 0 and 8
        while reply not in possible_moves:
            print("invalid response")
            reply = input("Enter Input (0-8) > ")
        
        # if the move is valid, remove it from the possible moves
        possible_moves.remove(reply)
        
        # Send the move to the server
        client_socket.send(reply.encode())
        # end the game if user wants to quit
        if reply == "/q":
            break
        
        # Update the board with the player's move
        index = int(reply)
        board[index] = 'X'
        print_board(board)
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
        
        # if the opponent quits, end the game 
        if not opponent_move or opponent_move == "/q":
            break
        
        # remove opponent move from possible moves
        if opponent_move in possible_moves:
            possible_moves.remove(opponent_move)
        
        # Update the board with the opponent's move
        index = int(opponent_move)
        board[index] = 'O'
        print_board(board)
        
        # end the game if the opponent won or the board is full
        if check_winner(board, 'O'):
            print("the server won!")
            break
        elif is_board_full(board):
            print("draw game")
            break

# prints the board array in 3 rows with borders for each space
def print_board(board):
    print("-------------")
    for i in range(3):
        print("|", board[i * 3], "|", board[i * 3 + 1], "|", board[i * 3 + 2], "|")
        print("-------------")

def check_winner(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],    # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],    # columns
        [0, 4, 8], [2, 4, 6]                # diagonals
    ]
    
    for combination in winning_combinations:
        # check if any combos = player mark
        if all(board[i] == player for i in combination):
            return True
    return False


def is_board_full(board):
    # true if no empty spaces on board
    return ' ' not in board


if __name__ == '__main__':
    client()
