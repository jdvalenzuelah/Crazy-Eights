from abc import ABC, abstractmethod

class CrazyClass(ABC):
    
    @abstractmethod
    def serialize(self) -> str:
        pass

    @abstractmethod
    def parse(self, data: str):
        pass