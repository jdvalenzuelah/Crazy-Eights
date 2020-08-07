from abc import ABC, abstractmethod

class CrazyClass(ABC):
    
    @abstractmethod
    def serialize(self) -> str:
        pass

    @abstractmethod
    @classmethod
    def parse(self, data: str) -> CrazyClass:
        pass