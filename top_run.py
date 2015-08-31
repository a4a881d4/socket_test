from CliSocket import CliSocket
from SerSocket import SerSocket

host='localhost'
#host = '10.0.77.111'
port=13053
addr=(host,port)

cli_sock= CliSocket(addr)
cli_sock.start()

srv_sock= SerSocket(addr)
srv_sock.start()
