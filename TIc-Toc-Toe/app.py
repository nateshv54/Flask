from flask import Flask, render_template, request, redirect

import random,time

app = Flask(__name__)

# Number of rows and columns in the table
rows = 3
cols = 3

# Create a 2D list to store the cell values
board = [['' for _ in range(cols)] for _ in range(rows)]

# Player symbols
symbols = ['X', 'O']
current_player = 0  # Index of the current player in the symbols list

def check_win():
    # Check rows
    for row in board:
        if all(cell == row[0] and cell != '' for cell in row):
            return row[0]

    # Check columns
    for col in range(cols):
        if all(board[row][col] == board[0][col] and board[row][col] != '' for row in range(rows)):
            return board[0][col]

    # Check diagonals
    if all(board[i][i] == board[0][0] and board[i][i] != '' for i in range(rows)) or \
       all(board[i][cols - i - 1] == board[0][cols - 1] and board[i][cols - i - 1] != '' for i in range(rows)):
        return board[1][1]  # Return the center cell value for diagonal win

    return None


def check_draw():
    return all([all(row) for row in board]) and not check_win()

@app.route('/')
def index():
    return render_template('Home.html')

@app.route('/tictactoe/computer')
def tictactoe_computer():
    global current_player
    current_player = 0
    return render_template('tictoc1.html', rows=rows, cols=cols, board=board, symbols=symbols, current_player=current_player)

@app.route('/tictactoe/twoplayer')
def tictactoe_twoplayer():
    global current_player
    current_player = 0
    return render_template('tictoc.html', rows=rows, cols=cols, board=board, symbols=symbols, current_player=current_player)

@app.route('/move1', methods=['POST'])
def move1():
    global current_player
    row = int(request.form['row'])
    col = int(request.form['col'])
    if board[row][col] == '':
        board[row][col] = symbols[current_player]
        winner = check_win()
        if winner:
            message = f'{winner} wins!'
            current_player=-1
        elif check_draw():
            message = 'It\'s a draw!'
            current_player=-1
        else:
            message = None
        current_player = (current_player + 1) % len(symbols)
        
        # Automate player K's move
        if current_player == 1:
            empty_cells = [(r, c) for r in range(rows) for c in range(cols) if board[r][c] == '']
            if empty_cells:
                r, c = random.choice(empty_cells)
                board[r][c] = symbols[current_player]
                winner = check_win()
                if winner:
                    message = f'{winner} wins!'
                    current_player=-1
                elif check_draw():
                    message = 'It\'s a draw!'
                    current_player=-1
                current_player = 0  # Switch back to player J after player K's move
        
    else:
        message = None
    return render_template('tictoc1.html', rows=rows, cols=cols, board=board, symbols=symbols, current_player=current_player, message=message)

@app.route('/move', methods=['POST'])
def move():
    global current_player
    row = int(request.form['row'])
    col = int(request.form['col'])
    if board[row][col] == '':
        board[row][col] = symbols[current_player]
        winner = check_win()
        if winner:
            message = f'{winner} is the Winner'
            current_player=-1
        elif check_draw():
            message = 'It\'s a draw!'
            current_player=-1
        else:
            message = None
        current_player = (current_player + 1) % len(symbols)
        
    else:
        message = None
    return render_template('tictoc.html', rows=rows, cols=cols, board=board, symbols=symbols, current_player=current_player, message=message)


@app.route('/reset1')
def reset_computer():
    global board, current_player
    board = [['' for _ in range(cols)] for _ in range(rows)]
    current_player = 0
    return redirect('/tictactoe/computer')

@app.route('/reset')
def reset_twoplayer():
    global board, current_player
    board = [['' for _ in range(cols)] for _ in range(rows)]
    current_player = 0
    return redirect('/tictactoe/twoplayer')


if __name__ == '__main__':
    app.run(debug=True)
