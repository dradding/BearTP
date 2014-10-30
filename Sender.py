import sys
import getopt

import Checksum
import BasicSender

'''
This is a skeleton sender class. Create a fantastic transport protocol here.
'''
class Sender(BasicSender.BasicSender):
    def __init__(self, dest, port, filename, debug=False, sackMode=False):
        super(Sender, self).__init__(dest, port, filename, debug)
        if sackMode:
            raise NotImplementedError #remove this line when you implement SACK
        self.file_len = len(self.infile)
        self.window_base = 0
        self.window_max = 4
        self.max_seqno = self.file_len/1472
        self.acks_received = {}
        self.window = {}


    # Main sending loop.
    def start(self):
        message = "start"
        seqno = 0
        if (max_seqno == 0): #the size of the file can be handled in one send call
            data = self.infile.read(self.file_len % 1472)
            new_packet = self.make_packet(message, seqno, data)
            self.send(new_packet)
            response = self.receive(500)
            handle_response(response)

        else:
            data = self.infile.read(1472)
            self.make_packet(message, seqno, None) #send start message first 
            self.send(new_packet)
            response = self.receive(500)
            handle_response(response)
            message = "data"
            seqno +=1
            while not message == "end":
                for i in range(window_base, window_max + 1):
                    if i != max_seqno:
                        self.acks_received[i] = 0
                        new_packet = self.make_packet(message, seqno, data)
                        self.send(new_packet)
                    else:










    def handle_response(self, response_packet):
        pass

    def handle_timeout(self):
        #resend
        pass

    def handle_new_ack(self, ack):
        self.window_open = 106
        self.current_ack = [rcv, 1]

    def handle_dup_ack(self, ack):
        self.current_ack[1] += 1
        if self.current_ack[1] == 4:
            #trigger resend
        pass

    def log(self, msg):
        if self.debug:
            print msg


'''
This will be run if you run this script from the command line. You should not
change any of this; the grader may rely on the behavior here to test your
submission.
'''
if __name__ == "__main__":
    def usage():
        print "BEARS-TP Sender"
        print "-f FILE | --file=FILE The file to transfer; if empty reads from STDIN"
        print "-p PORT | --port=PORT The destination port, defaults to 33122"
        print "-a ADDRESS | --address=ADDRESS The receiver address or hostname, defaults to localhost"
        print "-d | --debug Print debug messages"
        print "-h | --help Print this usage message"
        print "-k | --sack Enable selective acknowledgement mode"

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                               "f:p:a:dk", ["file=", "port=", "address=", "debug=", "sack="])
    except:
        usage()
        exit()

    port = 33122
    dest = "localhost"
    filename = None
    debug = False
    sackMode = False

    for o,a in opts:
        if o in ("-f", "--file="):
            filename = a
        elif o in ("-p", "--port="):
            port = int(a)
        elif o in ("-a", "--address="):
            dest = a
        elif o in ("-d", "--debug="):
            debug = True
        elif o in ("-k", "--sack="):
            sackMode = True

    s = Sender(dest, port, filename, debug, sackMode)
    try:
        s.start()
    except (KeyboardInterrupt, SystemExit):
        exit()
