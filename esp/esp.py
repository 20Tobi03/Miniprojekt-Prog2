import socketio

socket=socketio.Client()

def on_aaa_response(args):
    print('on_aaa_response', args['data'])


socket.connect("http://192.168.178.126:5000")
socket.wait()