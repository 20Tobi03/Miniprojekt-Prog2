from socketIO_client import SocketIO, LoggingNamespace

def on_aaa_response(args):
    print('on_aaa_response', args['data'])

socketIO = SocketIO('192.168.178.126', 5000, LoggingNamespace)
socketIO.connect()