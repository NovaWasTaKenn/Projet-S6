import abc 
from othello.logic.models import GameState

class Renderer(metaclass= abc.ABCMeta):
    
    @abc.abstractmethod
    def Render(gameState: GameState) -> None:
        """Renders the gameState"""