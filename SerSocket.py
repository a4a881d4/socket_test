import threading
import struct,socket,select,time
from ctypes import *

RxBuf = (c_short*8)()
class SerSocket(threading.Thread):
    def __init__(self,addr):
        threading.Thread.__init__(self)
        self.addr=addr            
    def run(self):        
        sock = socket.socket(socket.AF_INET, socket. SOCK_DGRAM)
        #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY,1)
        sock.bind(self.addr);
        #sock.listen(2);
        #while True :
        #    try:
        #        clisock, addr = sock.accept()
        #        print 'Accept OK!!'
        #        break
        #    except:
        #        pass
            
        sock_receiver=sock_recv(sock)
        sock_receiver.start()
        
        #sock_sender=sock_send(clisock)
        #sock_sender.start()

class sock_recv(threading.Thread):
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock=sock
        self.time_out=0.005
        self.start_state = 0
    def run(self):

        PktNum = 100000
        rx_num = 0
        PayloadLen = 0
        while True:
            data, addr = self.sock.recvfrom(1200+8)
            if self.start_state==0:
                self.start_state = 1
                start_time = time.time()
            PayloadLen = PayloadLen + len(data)
            rx_num = rx_num + 1
            if rx_num == PktNum:
                break
        print 'rx_num',rx_num
        end_time = time.time()
        total_time = end_time - start_time
        print 'SerRxRate', PayloadLen,total_time,PayloadLen/total_time
            
class sock_send(threading.Thread):
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock=sock
        self.time_out=0.005
    def run(self):
        length = 600
        pkt = (c_short*length)()
        pkt[:] = range(length)
        pkt_format = str(length) + 'h'
        payload_len = sizeof(c_short)*length
        up_data='\x7f'*4+struct.pack('2H',payload_len,payload_len)+struct.pack(pkt_format,*pkt)

        PktNum = 100000
        PayloadLen = 0
        start_time = time.time()
        for i in range(PktNum):
            infds,outfds,errfds = select.select([],[self.sock],[],self.time_out)
            if len(outfds):                
                send_size = self.sock.send(up_data)
            PayloadLen = PayloadLen + send_size
        end_time = time.time()
        total_time = end_time - start_time
        print 'SerTxRate',PayloadLen, total_time, PayloadLen/total_time
