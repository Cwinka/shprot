import pydantic
from typing import TypeVar, Type

T = TypeVar('T', bound='Message')


class Message(pydantic.BaseModel):
    _spec_sign = '|'

    @classmethod
    def split(cls, content: bytes) -> tuple[str, bytes]:
        """ Возвращает имя класса сообщения и данные """
        header, payload = content.split(cls._spec_sign.encode('ascii'), 1)
        return header.decode('ascii'), payload

    @classmethod
    def decode(cls: Type[T], payload: bytes) -> T:
        return cls.parse_raw(payload)

    def encode(self) -> bytes:
        return f'{self.__class__.__name__}{self._spec_sign}{self.json()}\n'.encode('utf-8')
