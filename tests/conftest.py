import pytest
import socket
from msg import Message
import random
import string


class MockMessage(Message):
    field1: str
    field2: int
    field3: float
    field4: bool
    field5: list[str]
    field6: list[int]
    field7: list[float]
    field8: list[bool]
    field9: tuple[int, ...]
    field10: tuple[float, ...]
    field11: tuple[bool, ...]
    field12: tuple[str, ...]


@pytest.fixture(scope="session")
def receive_bytes():
    with socket.create_server(('localhost', 9342)) as server:
        def receive(length: int):
            conn, addr = server.accept()
            return conn.recv(length)
        yield receive
        server.close()


@pytest.fixture(scope="session")
def send_bytes():
    with socket.create_connection(('localhost', 9342)) as conn:
        def send(msg: bytes):
            conn.send(msg)
        yield send
        conn.close()


@pytest.fixture(scope="session")
def gen_message():
    return lambda: MockMessage(
        field1=''.join(random.choices(string.ascii_letters, k=10)),
        field2=random.randint(0, 1000),
        field3=random.randint(0, 1000) / 10,
        field4=random.choice([True, False]),
        field5=random.choices(string.ascii_letters, k=10),
        field6=random.choices(range(1000), k=10),
        field7=list(map(lambda x: x / 10, random.choices(range(1000), k=10))),
        field8=random.choices([True, False], k=10),
        field9=tuple(random.choices(range(1000), k=10)),
        field10=tuple(map(lambda x: x / 10, random.choices(range(1000), k=10))),
        field11=tuple(random.choices([True, False], k=10)),
        field12=tuple(random.choices(string.ascii_letters, k=10))
    )
