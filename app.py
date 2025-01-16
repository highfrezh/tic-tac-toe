from flask import Flask, render_template, request, redirect, url_for, make_response
import random

app = Flask(__name__)

# Helper Functions
def create_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def check_winner(board, player):
    for i in range(3):
        # Check rows and columns
        if all([board[i][j] == player for j in range(3)]) or all([board[j][i] == player for j in range(3)]):
            return True
    # Check diagonals
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

def check_tie(board):
    return all(board[i][j] != " " for i in range(3) for j in range(3))

def ai_move(board):
    available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    move = random.choice(available_moves)
    board[move[0]][move[1]] = "O"

@app.route("/", methods=["GET", "POST"])
def index():
    # Reset the game if "reset" query parameter is present
    if request.method == "GET" and request.args.get("reset"):
        board = create_board()
        winner = ""
        response = redirect(url_for("index"))
        response.set_cookie("board", str(board))
        response.set_cookie("winner", winner)
        return response

    # Retrieve the board and winner status from cookies
    board = eval(request.cookies.get("board", str(create_board())))
    winner = request.cookies.get("winner", "")

    # Handle player move
    if request.method == "POST" and winner == "":
        row = int(request.form["row"])
        col = int(request.form["col"])
        if board[row][col] == " ":
            board[row][col] = "X"
            # Check for player win
            if check_winner(board, "X"):
                winner = "Player X wins!"
            elif check_tie(board):
                winner = "It's a tie!"
            else:
                # AI's turn
                ai_move(board)
                if check_winner(board, "O"):
                    winner = "Player O wins!"
                elif check_tie(board):
                    winner = "It's a tie!"

    # Update cookies
    response = render_template("index.html", board=board, winner=winner)
    response = make_response(response)
    response.set_cookie("board", str(board))
    response.set_cookie("winner", winner)
    return response

if __name__ == "__main__":
    app.run(debug=True)
