import dataclasses
from crazy_class import CrazyClass

class CrazySerializer:

    def serialize(self, data) -> str:
        if not isinstance(data, CrazyClass):
            return None
        return data.serialize()
        
    def parse(self, data: CrazyClass) -> str:
        if not isinstance(data, CrazyClass):
            return None
        return data.parse(data)
