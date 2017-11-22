import itertools, time, random, pickle

class Menace:
    def __init__(self, start=None):
        self.map = {}
        self.board = [" "]*9
        if start == None:
            start = 50

        for board in self.gen_boards():
            prob = []
            for i,x in enumerate(board):
                if x == " ":
                    prob.append(start)
                else:
                    prob.append(0)

            self.map[str(board)] = prob

        self.plays = []

    def detect_win(self, board):
        win_pos = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        win = []
        for order in win_pos:
            if board[order[0]] == board[order[1]] and board[order[1]] == board[order[2]] and board[order[0]] != " ":
                win.append(board[order[0]])
        if len(win) >= 1:
            if all(x == win[0] for x in win):
                return win[0]
            else:
                return False
        elif board.count(" ") == 0:
            return "C"
        return None

    def is_valid(self, board):
        os = board.count("O")
        xs = board.count("X")

        winner = self.detect_win(board)

        if not ((xs == os) or (xs == (os+1))):
            return False
        elif winner == False:
            return False
        elif winner == "O":
            return xs == os
        elif winner == "X":
            return xs == (os + 1)
        return True

    def gen_boards(self):
        for board in itertools.product("XO ", repeat=9):
            if self.is_valid(board):
                yield list(board)

    def weighted_choice(self,prob):
        sel = random.randint(1, sum(prob))
        i = -1
        while sel > 0:
            i += 1
            sel -= prob[i]
        return i

    def play(self, move=None):
        if move == None:
            piece = "X"
            if sum(self.map[str(self.board)]) == 0:
                return "O"
            move = self.weighted_choice(self.map[str(self.board)])
            self.plays.append([str(self.board),move])
        else:
            piece = "O"
        self.board[move] = piece

        winner = self.detect_win(self.board)
        if winner in ["X", "C"]:
            return "X"
        elif winner == "O":
            return winner
        else:
            return False

    def learn(self):
        if sum(self.map[str(self.board)]) == 0 and " " in self.board:
            off = -1
        else:
            winner = self.detect_win(self.board)
            if winner == "X":
                off = 4
            elif winner == "C":
                off = 3
            else:
                off = -1

        for move in self.plays:
            self.map[str(move[0])][move[1]] += off
        self.plays = []
        self.board = [" "]*9

    def print_board(self):
        print("+---+")
        for i,x in enumerate(self.board):
            if i in [0,3,6]:
                print("|", end="")
            if x == " ":
                print(i, end="")
            else:
                print(x, end="")
            if i in [2,5,8]:
                print("|")
        print("+---+")

    def get_play(self):
        self.print_board()

        valid = [i for i, x in enumerate(self.board) if x == " "]

        choice = -1
        while choice not in valid:
            choice = input("Make a move: ")
            if choice.isdigit():
                choice = int(choice)
            else:
                choice = -1

        return choice

    def save(self, file):
        with open(file, "wb") as f:
            pickle.dump(self.map, f)

    def load(self, file):
        with open(file, "rb") as f:
            self.map = pickle.load(f)

    def run(self):
        print("""
  __  __ ______ _   _          _____ ______
 |  \/  |  ____| \ | |   /\   / ____|  ____|
 | \  / | |__  |  \| |  /  \ | |    | |__
 | |\/| |  __| | . ` | / /\ \| |    |  __|
 | |  | | |____| |\  |/ ____ \ |____| |____
 |_|  |_|______|_| \_/_/    \_\_____|______|\n\n""")

        input("\n\nPress enter to start")

        while True:
            win = self.play()

            if win:
                if win == "O":
                    print("You won!!!")
                else:
                    print("Menace won!!!")
                continue

            move = self.get_play()

            win = self.play(move)

            if win:
                if win == "O":
                    print("You won!!!")
                else:
                    print("Menace won!!!")

                continue