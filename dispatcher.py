from typing import Protocol, Type, Callable, Any, TypeVar, Generator
from msg import Message

Msg = TypeVar('Msg', bound=Message)


class InvalidMessage(Exception):
    pass


class Na(Protocol):

    def recv(self, bufsize: int, flags: int = ...) -> bytes: ...


class Dispatcher:

    def __init__(self):
        self._rg: dict[str, tuple[Type[Message], Callable[[Message], Any]]] = {}

    def register_for(self, message_type: Type[Msg]):
        def wrap(f: Callable[[Msg], Any]):
            self._rg[message_type.__name__] = (message_type, f)
            return f
        return wrap

    def dispatch(self, io: Na):
        for message in self._read_to_end(io):
            msg_class_name, payload = Message.split(message)
            try:
                message_type, callback = self._rg[msg_class_name]
            except KeyError:
                print(f'No handler for message type: {msg_class_name}')
                return

            callback(message_type.decode(payload))

    @staticmethod
    def _read_to_end(io: Na) -> Generator[bytes, None, None]:
        before: bytes = b''
        while chunk := io.recv(512):
            chunk = before + chunk
            prev_stop = 0
            while (stop := chunk.find(b'\n', prev_stop)) != -1:
                yield chunk[prev_stop:stop]
                prev_stop = stop+1

            before = chunk[prev_stop:]
