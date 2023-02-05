import pydantic
from typing import TypeVar, Type

T = TypeVar('T', bound='Message')


class Message(pydantic.BaseModel):
    _spec_sign = '|'

    @classmethod
    def _split(cls, content: bytes) -> tuple[str, bytes]:
        """ Возвращает имя класса сообщения и данные """
        header, payload = content.split(cls._spec_sign.encode('ascii'), 1)
        return header.decode('ascii'), payload

    @classmethod
    def get_name(cls, content: bytes) -> str:
        """ Возвращает имя класса сообщения """
        return content.split(cls._spec_sign.encode('ascii'), 1)[0].decode('ascii')

    @classmethod
    def decode(cls: Type[T], content: bytes) -> T:
        message_name, payload = cls._split(content)
        if message_name != cls.name():
            raise ValueError(f'Invalid message type: {message_name}, need {cls.name()}')
        return cls.parse_raw(payload)

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    def encode(self) -> bytes:
        return f'{self.name()}{self._spec_sign}{self.json()}\n'.encode('utf-8')
