import itertools, time, random, pickle

class Menace:
    def __init__(self, start=None):
        self.map = {}
        self.board = [" "]*9
        if start == None:
            start = 50

        # Generate dictionary for every board position
        for board in self.gen_boards():
            prob = []
            # array with probability for play in that position
            # 0 if already played, <start> if empty
            for i,x in enumerate(board):
                if x == " ":
                    prob.append(start)
                else:
                    prob.append(0)

            self.map[str(board)] = prob

        self.plays = []

    def detect_win(self, board):
        # Board positions for win detections
        win_pos = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        win = []

        # Check each possible win position for a win
        for order in win_pos:
            if board[order[0]] == board[order[1]] and board[order[1]] == board[order[2]] and board[order[0]] != " ":
                win.append(board[order[0]])

        # Detect multiple wins, if all the same player return winner
        # If both players, return false
        if len(win) >= 1:
            if all(x == win[0] for x in win):
                return win[0]
            else:
                return False

        # If no winner and board full, CAT
        elif board.count(" ") == 0:
            return "C"

        # Otherwise return None winner
        return None

    def is_valid(self, board):
        os = board.count("O")
        xs = board.count("X")

        winner = self.detect_win(board)

        # Only get boards where it is X's turn
        if not (xs == os):
            return False
        # If two different winners, bad
        elif winner == False:
            return False
        # If no winner, that's a state X cares about
        elif winner == None:
            return True
        # Otherwise, not important
        else:
            return False

    def gen_boards(self):
        # Every 9 character combination of "XO "
        for board in itertools.product("XO ", repeat=9):
            if self.is_valid(board):
                yield list(board)

    def weighted_choice(self,prob):
        # Pass a probability array, [10,5,0,3] will pick a random index with
        # the given probabilities.
        sel = random.randint(1, sum(prob))
        i = -1
        while sel > 0:
            i += 1
            sel -= prob[i]
        return i

    def play(self, move=None):
        # None -> MENACEs turn
        if move == None:
            piece = "X"

            # Check if MENACE can make a move otherwise resign
            if sum(self.map[str(self.board)]) == 0:
                return "O"

            # Random move
            move = self.weighted_choice(self.map[str(self.board)])

            # Store for learning
            self.plays.append([str(self.board),move])
        else:
            piece = "O"

        # Update board with move
        self.board[move] = piece

        # Check if someone won
        winner = self.detect_win(self.board)

        if winner in ["X", "C"]:
            return "X"
        elif winner == "O":
            return winner
        else:
            return False

    def learn(self):
        # Check winner again
        winner = self.detect_win(self.board)

        # Set learning differential for win/tie/lose
        if winner == "X":
            off = 4
        elif winner == "C":
            off = 3
        else:
            off = -1

        # Update all played boards
        for move in self.plays:
            self.map[str(move[0])][move[1]] += off

        # Reset play memory and board
        self.plays = []
        self.board = [" "]*9

    def save(self, file):
        # Save learning map to pickle file
        with open(file, "wb") as f:
            pickle.dump(self.map, f)

    def load(self, file):
        # Load learning map from pickle file
        with open(file, "rb") as f:
            self.map = pickle.load(f)