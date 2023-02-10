class CanNotConvertObjectToJson(Exception):
    @classmethod
    def create(cls, entity: object, details: str = None) -> Exception:
        return cls(f'"{entity.__class__}" is not serializable. {details}'.strip())


class CanNotConvertObjectFromJson(Exception):
    @classmethod
    def create(cls, entity_class: str, details: str = None) -> Exception:
        return cls(f'"{entity_class}" is not unserializable. {details}'.strip())
