import pytest
from dispatcher import Dispatcher
from conftest import MockMessage
import threading


# generate 10 messages, send them to socket, receive them back and compare
def test_message_count(receive_bytes, send_bytes, gen_message):
    messages = [gen_message() for _ in range(5)]
    content = b''.join(m.encode() for m in messages)
    send_bytes(content)
    received = receive_bytes(len(content))

    assert received.count(b'\n') == len(messages)
    restored = [MockMessage.decode(m) for m in received.split(b'\n') if m]
    assert len(restored) == len(messages)


def test_messages_order(receive_bytes, send_bytes, gen_message):
    messages = [gen_message() for _ in range(5)]
    content = b''.join(m.encode() for m in messages)
    send_bytes(content)
    received = receive_bytes(len(content))

    restored = [MockMessage.decode(m) for m in received.split(b'\n') if m]
    for m1, m2 in zip(messages, restored):
        assert m1 == m2
