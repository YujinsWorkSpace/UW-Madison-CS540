import random
import time
import copy


class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    HW9 cooperated with Robbie Xu
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def succ(self, state, piece, drop_phase=True):
        succ_set = []
        if drop_phase:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        state_copy = copy.deepcopy(state)
                        state_copy[row][col] = piece
                        succ_set.append(state_copy)
        else:
            for row in range(len(state)):
                for col in range(5):
                    if state[row][col] == piece:
                        if col + 1 < 5 and state[row][col + 1] == ' ':
                            state_copy = copy.deepcopy(state)
                            state_copy[row][col] = ' '
                            state_copy[row][col + 1] = piece
                            succ_set.append(state_copy)
                        if row + 1 < 5 and state[row + 1][col] == ' ':
                            state_copy = copy.deepcopy(state)
                            state_copy[row][col] = ''
                            state_copy[row + 1][col] = piece
                            succ_set.append(state_copy)
                        if col - 1 >= 0 and state[row][col - 1] == ' ':
                            state_copy = copy.deepcopy(state)
                            state_copy[row][col] = ' '
                            state_copy[row][col - 1] = piece
                            succ_set.append(state_copy)
                        if row - 1 >= 0 and state[row - 1][col] == ' ':
                            state_copy = copy.deepcopy(state)
                            state_copy[row][col] = ' '
                            state_copy[row - 1][col] = piece
                            succ_set.append(state_copy)
                        if row - 1 >= 0 and col - 1 >= 0 and state[row - 1][col - 1] == ' ':
                            state_copy = copy.deepcopy(state)
                            state_copy[row][col] = ' '
                            state_copy[row - 1][col - 1] = piece
                            succ_set.append(state_copy)
                        if row + 1 < 5 and col + 1 < 5 and state[row + 1][col + 1] == ' ':
                            state_copy = copy.deepcopy(state)
                            state_copy[row][col] = ' '
                            state_copy[row + 1][col + 1] = piece
                            succ_set.append(state_copy)
                        if row - 1 >= 0 and col + 1 < 5 and state[row - 1][col + 1] == ' ':
                            state_copy = copy.deepcopy(state)
                            state_copy[row][col] = ' '
                            state_copy[row - 1][col + 1] = piece
                            succ_set.append(state_copy)
                        if row + 1 <= 4 and col - 1 >= 0 and state[row + 1][col - 1] == ' ':
                            state_copy = copy.deepcopy(state)
                            state_copy[row][col] = ' '
                            state_copy[row + 1][col - 1] = piece
                            succ_set.append(state_copy)
        return succ_set

    def heuristic_game_value_piece(self, state, piece):
        # Initialize max_consecutive_pieces to 0
        max_consecutive_pieces = 0

        # Iterate over each position in the game board
        for row in range(5):
            for col in range(5):
                # Check if the current position contains the player's piece
                if state[row][col] == piece:
                    # Check for consecutive pieces in a horizontal direction
                    following_col = col
                    consecutive_pieces = 1
                    while following_col < 4 and state[row][following_col + 1] == piece:
                        following_col += 1
                        consecutive_pieces += 1
                    if consecutive_pieces > max_consecutive_pieces:
                        max_consecutive_pieces = consecutive_pieces

                    # Check for consecutive pieces in a vertical direction
                    following_row = row
                    consecutive_pieces = 1
                    while following_row < 4 and state[following_row + 1][col] == piece:
                        consecutive_pieces += 1
                        following_row += 1
                    if consecutive_pieces > max_consecutive_pieces:
                        max_consecutive_pieces = consecutive_pieces

                    # Check for consecutive pieces in a right diagonal direction
                    consecutive_pieces = 1
                    following_row = row
                    following_col = col
                    while following_row < 4 and following_col < 4 and state[following_row + 1][following_col + 1] == piece:
                        consecutive_pieces += 1
                        following_row += 1
                        following_col += 1
                    if consecutive_pieces > max_consecutive_pieces:
                        max_consecutive_pieces = consecutive_pieces

                    # Check for consecutive pieces in a left diagonal direction
                    consecutive_pieces = 1
                    following_row = row
                    following_col = col
                    while following_row < 4 and following_col > 0 and state[following_row + 1][
                        following_col - 1] == piece:
                        following_col -= 1
                        following_row += 1
                        consecutive_pieces += 1
                    if consecutive_pieces > max_consecutive_pieces:
                        max_consecutive_pieces = consecutive_pieces

                    # Check for consecutive pieces in a square direction
                    consecutive_pieces = 1
                    if row < 4 and state[row + 1][col] == piece:
                        consecutive_pieces += 1
                    if col < 4 and state[row][col + 1] == piece:
                        consecutive_pieces += 1
                    if row < 4 and col < 4 and state[row + 1][col + 1] == piece:
                        consecutive_pieces += 1
                    if consecutive_pieces > max_consecutive_pieces:
                        max_consecutive_pieces = consecutive_pieces

        # Return the maximum number of consecutive pieces found in any direction
        return max_consecutive_pieces

    def heuristic_game_value(self, state):
        if self.game_value(state) != 0:
            return self.game_value(state)
        return (self.heuristic_game_value_piece(state, self.my_piece) - self.heuristic_game_value_piece(state,
                                                                                                        self.opp)) / 4

    def mini_max(self, state, depth, drop_phase):
        # Check if the current state is a terminal state
        if self.game_value(state) != 0:
            # If it is, return the game value of the state
            return self.game_value(state)
        # If we've reached the depth limit, return the heuristic value of the state
        elif depth == 3:
            return self.heuristic_game_value(state)
        # If it's the turn of the maximizing player
        elif depth % 2 == 0:
            # Generate the successor states and recursively call mini_max on each of them
            # Choose the maximum value returned by the recursive calls
            return max(
                [self.mini_max(succ, depth + 1, drop_phase) for succ in self.succ(state, self.my_piece, drop_phase)])
        # If it's the turn of the minimizing player
        else:
            # Generate the successor states and recursively call mini_max on each of them
            # Choose the minimum value returned by the recursive calls
            return min([self.mini_max(succ, depth + 1, drop_phase) for succ in self.succ(state, self.opp, drop_phase)])

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        s1 = time.time()
        piece_count = 0
        for row in state:
            for piece in row:
                if piece != ' ':
                    piece_count += 1
        if piece_count < 8:
            drop_phase = True
        else:
            drop_phase = False

        if not drop_phase:
            move = []
            highest_succ = state
            highest_value = self.mini_max(state, 0, False)
            for succ in self.succ(state, self.my_piece, False):
                if self.mini_max(succ, 1, False) == highest_value:
                    highest_succ = succ

            for row in range(5):
                for column in range(5):
                    if state[row][column] != highest_succ[row][column] and state[row][column] != ' ':
                        move_row_from = row
                        move_column_from = column
                    if state[row][column] != highest_succ[row][column] and state[row][column] == ' ':
                        move_row_to = row
                        move_column_to = column
            move.insert(0, (move_row_from, move_column_from))
            move.insert(0, (move_row_to, move_column_to))
            s2 = time.time()
            print(s2 - s1)

            return move

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        move = []
        highest_succ = state
        highest_value = self.mini_max(state, 0, True)
        for succ in self.succ(state, self.my_piece, True):
            if self.mini_max(succ, 1, True) == highest_value:
                highest_succ = succ
        for row in range(5):
            for column in range(5):
                if state[row][column] != highest_succ[row][column]:
                    move.insert(0, (row, column))
                    s2 = time.time()
                    print(s2 - s1)
                    return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # check \ diagonal wins
        for row in range(3, 5):
            for column in range(2):
                if state[row][column] != ' ' and state[row][column] == state[row - 1][column - 1] == state[row - 2][column - 2] == state[row - 3][column - 3]:
                    return 1 if state[row][column] == self.my_piece else -1
        # check / diagonal wins
        for row in range(2):
            for column in range(2):
                if state[row][column] != ' ' and state[row][column] == state[row + 1][column + 1] == state[row + 2][column + 2] == state[row + 3][column + 3]:
                    return 1 if state[row][column] == self.my_piece else -1
        # check box wins
        for row in range(4):
            for column in range(4):
                if state[row][column] != ' ' and state[row][column] == state[row + 1][column] == state[row + 1][column + 1] == state[row][column + 1]:
                    return 1 if state[row][column] == self.my_piece else -1

        return 0  # no winner yet


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                      (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
