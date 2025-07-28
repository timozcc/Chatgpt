import sys

BOARD_SIZE = 15

EMPTY = '.'
PLAYER_MARKS = ['X', 'O']


def create_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def print_board(board):
    header = '   ' + ' '.join(f'{i+1:2}' for i in range(BOARD_SIZE))
    print(header)
    for idx, row in enumerate(board):
        print(f'{idx+1:2} ' + ' '.join(row))
    print()


def check_five(board, mark, row, col):
    directions = [
        (1, 0),  # vertical
        (0, 1),  # horizontal
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        for step in [1, -1]:
            r, c = row + dr * step, col + dc * step
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == mark:
                count += 1
                r += dr * step
                c += dc * step
            if count >= 5:
                return True
    return False


def get_move(player):
    while True:
        try:
            move = input(f"Player {player+1} ({PLAYER_MARKS[player]}), enter row and column (e.g., 8 8): ")
            if move.lower() in {'quit', 'exit'}:
                sys.exit(0)
            r_str, c_str = move.strip().split()
            r, c = int(r_str) - 1, int(c_str) - 1
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                return r, c
        except (ValueError, KeyboardInterrupt):
            sys.exit(0)
        print("Invalid move. Please enter valid row and column numbers.")


def play_game():
    board = create_board()
    current_player = 0
    turns = 0
    print("\n=== Gomoku Game ===")
    while True:
        print_board(board)
        r, c = get_move(current_player)
        if board[r][c] != EMPTY:
            print("Cell already occupied. Try again.")
            continue
        board[r][c] = PLAYER_MARKS[current_player]
        turns += 1
        if check_five(board, PLAYER_MARKS[current_player], r, c):
            print_board(board)
            print(f"Player {current_player+1} ({PLAYER_MARKS[current_player]}) wins!")
            break
        if turns == BOARD_SIZE * BOARD_SIZE:
            print("It's a draw!")
            break
        current_player = 1 - current_player
    print("Game over. Thanks for playing!")


if __name__ == "__main__":
    try:
        play_game()
    except SystemExit:
        print("Goodbye!")
