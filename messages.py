from msg import Message


class Ha(Message):
    client: str
    ssu: int = 3


class Lu(Message):
    client: str
    lu: float = 0.5
    h: tuple[int, ...] = (1, 2, 3)
