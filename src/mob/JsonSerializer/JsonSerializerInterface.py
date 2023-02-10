import abc


class JsonSerializerInterface(abc.ABC):
    @abc.abstractmethod
    def to_json(self, entity: object) -> str:
        pass

    @abc.abstractmethod
    def from_json(self, EntityClass, json_string: str):
        pass;
