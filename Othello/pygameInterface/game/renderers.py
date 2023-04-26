import abc 
from logic.models import GameState

class Renderer(metaclass= abc.ABCMeta):
    
    @abc.abstractmethod
    def Render(gameState: GameState) -> None:
        """Renders the gameState"""