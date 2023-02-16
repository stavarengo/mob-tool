from mobt.JsonSerializer.Exceptions import CanNotConvertObjectFromJson, CanNotConvertObjectToJson
from mobt.JsonSerializer.JsonSerializerInterface import JsonSerializerInterface


class DataClassesSerializer(JsonSerializerInterface):

    def to_json(self, entity: object) -> str:
        try:
            return entity.to_json(indent=2)
        except AttributeError as e:
            if 'to_json' in str(e):
                raise CanNotConvertObjectToJson.create(entity, str(e))
            raise e

    def from_json(self, EntityClass, json_string: str):
        try:
            return EntityClass.from_json(json_string)
        except AttributeError as e:
            if 'from_json' in str(e):
                raise CanNotConvertObjectFromJson.create(EntityClass, str(e))
            raise e
