import sys
import getopt

import Checksum
import BasicSender

'''
This is a skeleton sender class. Create a fantastic transport protocol here.
'''
class Sender(BasicSender.BasicSender):
    def __init__(self, dest, port, filename, debug=True, sackMode=True):
        super(Sender, self).__init__(dest, port, filename, debug)
        # if sackMode:
        #     raise NotImplementedError #remove this line when you implement SACK
        #self.file_len = len(self.infile)
        self.sackMode = sackMode
        self.window_base = 0
        self.window_max = 4
        #self.max_seqno = self.file_len/1472
        self.current_ack = [-1,-1] #[seqno, repitions]
        self.current_cum_ack = -1
        self.current_sack = []
        self.window = {}


    # Main sending loop.
    def start(self):
        message = "data"
        seqno = 0
        #if (max_seqno == 0): #the size of the file can be handled in one send call
            #data = self.infile.read(self.file_len % 1472)
        new_packet = self.make_packet("start", seqno, "")
        self.send(new_packet)
        self.window[0] = new_packet
        response = self.receive(.5)
        # while self.handle_response(response) == False:
        #     self.send(new_packet)
        #     response = self.receive(.5)
        # print "start packet recieved"

            #data = self.infile.read(1472)
        while not message == "end":
            for i in range(self.window_base, self.window_max + 1):
                # if i != max_seqno:
                #     new_packet = self.make_packet(message, seqno, data)
                #     window[i] = new_packet
                #     self.send(new_packet)

                if not i in self.window.keys():
                    #print i
                    data = self.infile.read(1400)
                    if (len(data) < 1400):
                        message = "end"
                        #if end, send end, otherwise send data
                    new_packet = self.make_packet(message, i, data)
                    self.window[i] = new_packet
                    #print data
                    self.send(new_packet)
                if message == "end":
                    break       
            #print self.window
            response = self.receive(.5)
            self.handle_response(response)

        while len(self.window) != 0:
            response = self.receive(.5)
            self.handle_response(response)


    def handle_response(self, response_packet):
        if response_packet == None:           
            self.handle_timeout()
            # return False
        if Checksum.validate_checksum(response_packet):
            msg_type, seqno, data, checksum = self.split_packet(response_packet)
            if self.sackMode:
                self.handle_sack(seqno)
            else:
                seqno = int(seqno)
                print seqno
                if seqno > self.current_ack[0]:
                    self.handle_new_ack(seqno)
                if seqno == self.current_ack[0]:
                    self.handle_dup_ack(seqno)
            # return True

    def handle_sack(self, sack):
        info = sack.split(";")
        if info[1] == '':
            info.remove('')
            self.current_sack = []
        else:
            sacks = info[1].split(",")
            sacks = map(int, sacks)
            self.current_sack = sacks
        print info
        self.current_cum_ack = int(info[0])
        if self.current_cum_ack in self.window:
            self.send(self.window[self.current_cum_ack])
        self.window_base = self.current_cum_ack
        self.window_max = self.current_cum_ack + 4
        if len(self.current_sack)> 1:
            for key in self.window:
                if not key in self.sacks:
                    self.send(self.window[key])

    def handle_timeout(self):
        if self.sackMode:
            for i in range(self.window_base, self.window_max + 1):
                if (not i in self.current_sack):
                    self.send(self.window[i])


        else:
            self.send(self.window[self.window_base])
        print "resend due to timeout"

    def handle_new_ack(self, ack):
        self.window_base = ack
        self.window_max = ack + 4
        self.current_ack = [ack, 1]
        to_delete = []
        for key in self.window:
            if key < self.window_base:
                to_delete.append(key)
        for key in to_delete:
            del self.window[key]
        '''if ack in self.window.keys():
            self.send(self.window[ack])
            response = self.receive(.5)
            self.handle_response(response)'''

    def handle_dup_ack(self, ack):
        self.current_ack[1] += 1
        if self.current_ack[1] >= 4:
            self.send(self.window[ack])
            print "resend due to dup ack"

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
