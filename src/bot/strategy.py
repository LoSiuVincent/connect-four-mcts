import random

from src.bot.board import Board
from src.bot.mcts.game import ConnectFour
from src.bot.mcts.mcts import MCTS


def create_strategy(strategy: str):
    if strategy == 'fixed':
        return FixedStrategy()
    elif strategy == 'random':
        return RandomStrategy()
    elif strategy == 'mcts':
        return MCTSStrategy()


class FixedStrategy:
    def predict(self, board: Board):
        if not board.is_column_full(1):
            return 1
        else:
            return board.get_next_available_column()


class RandomStrategy:
    def predict(self, board: Board):
        return random.choice(board.get_available_columns())


class MCTSStrategy:
    def predict(self, board: Board):
        game = ConnectFour(board)
        mcts = MCTS(game)
        return mcts.get_next_move()
