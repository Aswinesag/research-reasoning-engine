class BaseSimulator(ABC):
    @abstractmethod
    def run(self, state):
        pass