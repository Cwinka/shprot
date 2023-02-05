from messages import Ha, Lu

if __name__ == '__main__':
    import socket

    with socket.create_connection(('localhost', 9342)) as conn:
        messages = [
            Ha(client='foo'),
            Lu(client='foo'),
            Lu(client='foo'),
            Ha(client='foo'),
        ]
        conn.send(b''.join(m.encode() for m in messages))
