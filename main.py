from dispatcher import Dispatcher
from messages import Ha, Lu

d = Dispatcher()


@d.register_for(Lu)
def case_m(message: Lu):
    print('lu', message)


@d.register_for(Ha)
def case_b(message: Ha):
    print('ha', message)


if __name__ == '__main__':
    import socket

    with socket.create_server(('localhost', 9342)) as server:
        while True:
            conn, address = server.accept()
            d.dispatch(conn)
