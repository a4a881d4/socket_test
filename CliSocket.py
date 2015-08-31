import threading
import struct,socket,select,time
from ctypes import *


class CliSocket(threading.Thread):
    def __init__(self,addr):
        threading.Thread.__init__(self)
        self.addr=addr            
    def run(self):        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY,1)
        while True:
            try:
                sock.connect(self.addr)
                break
            except:
                pass
            
        sock_receiver=sock_recv(sock)
        sock_receiver.start()
        sock_sender=sock_send(sock)
        sock_sender.start()
            
class sock_recv(threading.Thread):
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock=sock
        self.time_out=0.005
    def run(self):

        PktNum = 10000
        start_time = time.time()
        PayloadLen = 0
        rx_num = 0
        while True:

            infds,outfds,errfds = select.select([self.sock],[],[],self.time_out)

            if len(infds):
                info_header=''
                req_msg=''

                try:                    
                    info_header=self.sock.recv(8)                    
                    if info_header:                
                        if info_header[:4]=='\x7f'*4:                            
                            len1,len2=struct.unpack_from('2H',info_header,4)
                            if len1==len2:
                                msg_len=len1
                                req_msg=self.sock.recv(msg_len)

                            PayloadLen = PayloadLen + len(req_msg)
                            rx_num = rx_num + 1
                            if rx_num == PktNum:
                                break

                except:
                    pass

        end_time = time.time()
        total_time = end_time - start_time
        print 'CliRxRate', PayloadLen,total_time,PayloadLen/total_time    
            
            
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

        PktNum = 10000
        PayloadLen = 0
        start_time = time.time()
        for i in range(PktNum):
            infds,outfds,errfds = select.select([],[self.sock],[],self.time_out)
            if len(outfds):                
                send_size = self.sock.send(up_data)
            PayloadLen = PayloadLen + send_size
            #time.sleep(0.0001)
            
        end_time = time.time()
        total_time = end_time - start_time
        print 'CliTxRate',PayloadLen, total_time, PayloadLen/total_time
            
