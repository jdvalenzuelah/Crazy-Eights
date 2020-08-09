import dataclasses
from crazy_serializer.crazy_class import CrazyClass

class CrazySerializer:

    def serialize(self, data: CrazyClass) -> str:
        if not isinstance(data, CrazyClass):
            return None
        return data.serialize()
        
    def parse(self, data: str, target: CrazyClass) -> CrazyClass:
        return target.parse(data)
