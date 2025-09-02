from GameState import GameState
from Action import Action
from threading import Thread
import random

class Player(Thread):
    def __init__(self, *args):
        # Internal
        Thread.__init__(self)
        self.args = args
        self.action = Action(-1)

    def act(self, gamestate):
        pieces = gamestate.pieces
        my_piece = 1
        opp_piece = 2

        # 1. Try to win
        for move in range(9):
            if pieces[move] == 0:
                temp = pieces.copy()
                temp[move] = my_piece
                if self.check_winner(temp) == my_piece:
                    self.action = Action(move)
                    return

        # 2. Block opponent
        for move in range(9):
            if pieces[move] == 0:
                temp = pieces.copy()
                temp[move] = opp_piece
                if self.check_winner(temp) == opp_piece:
                    self.action = Action(move)
                    return

        # 3. Take center
        if pieces[4] == 0:
            self.action = Action(4)
            return

        # 4. Take a corner
        for move in [0, 2, 6, 8]:
            if pieces[move] == 0:
                self.action = Action(move)
                return

        # 5. Random move
        free = [i for i in range(9) if pieces[i] == 0]
        self.action = Action(random.choice(free))

    def check_winner(self, pieces):
        # Check rows & columns
        for i in range(3):
            if pieces[3*i] == pieces[3*i+1] == pieces[3*i+2] != 0:
                return pieces[3*i]
            if pieces[i] == pieces[i+3] == pieces[i+6] != 0:
                return pieces[i]
        # Check diagonals
        if pieces[0] == pieces[4] == pieces[8] != 0:
            return pieces[0]
        if pieces[2] == pieces[4] == pieces[6] != 0:
            return pieces[2]
        return 0

    # Required internal
    def run(self):
        self.act(self.args[0])
