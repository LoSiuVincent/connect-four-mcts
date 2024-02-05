from .game import Game
from .node import Node


class MCTS:
    def __init__(self, game: Game, C: float = 1):
        self._root = Node(game)
        self._C = C

    def select(self) -> Node:
        current = self._root
        while not current.is_leaf():
            current = current.get_child_with_highest_UCB(self._C)
        return current
        
    def expand(self, node: Node) -> None:
        node.expand()

    def rollout(self, node: Node) -> float:
        return node.rollout()
