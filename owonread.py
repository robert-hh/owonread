#!/usr/bin/env python3
#
# read image or trace from scope
#
import struct
import sys
import socket
import getopt
import binascii

def read_data(cmd_txt, parm,  server_addr, fname, skip):
    res = b""
    try:
        s = socket.socket()
        s.connect(server_addr)
        if s:
# pack & send command
            cmd = cmd_txt + parm
            cmd = struct.pack("<l%ds" % len(cmd), len(cmd), cmd.encode())
            s.send(cmd)
# get length of response
            ss = s.recv(4)
            size = struct.unpack("<l", ss)[0]
# skip header
            hdr_size = len(cmd_txt) + 4
            name = s.recv(hdr_size)
            size -= hdr_size
# open file
            if fname == "":
                pass
            elif fname == '-': 
                f = sys.stdout
            else:
                f = open(fname, "wb")
# if additional skip, do it
            while skip > 0:
                img = s.recv(skip)
                size -= len(img)
                skip -= len(img)
# get bulk data
            while size > 0:
                img = s.recv(size)
                if fname != "":
                    if f == sys.stdout:
                        f.buffer.write(img)
                    else:
                        f.write(img)
                else:
                    res += img
                size -= len(img)
# and that's it
            if fname != "" and f != sys.stdout:
                f.close()
            s.close()
            return res
    except Exception as err:
        sys.stderr.write("Error attempting to get data, reason %s\n" % err)
        return False

def print_dir(s):
    pos = 0
    while pos < len(s):
        if s[pos] == 1:
            print ("d ", end="")
        else:   
            print ("  ", end="")
        sb = binascii.unhexlify(s[pos+1:pos+9])
        size = struct.unpack(">l", sb)[0]
        print ("%8d " % size, end="")
        pos += 17
        while s[pos] != ord('|'):
            print (chr(s[pos]), end="")
            pos += 1
        print(" ");
        pos += 1
        

def usage():
    print ("owonread OPTION filename\n" \
            "   Options: \n"\
            "   -t type: type for data - image | track | screen | file\n" \
            "   -c selection: select channel 1/2/3/4 for track data, \n"\
            "                 jpg/bmp/png for image, file name for file\n" \
            "   -s # : skip the first # byte from the scope\n" \
            "   -i ip_addr: IP-Address of the oscilloscope\n" \
            "   -p port : port number - default 3000\n" \
            "   -h print these few help lines\n" \
            "If the file name is missing or '-', the data is written to stdout\n"\
            "Default: image = BMP, skip = 0, ip_addr = 'owon.tds', port = 3000, selection = 1/BMP")


def main():
#
# look for command line arguments
#
    args_dict = { '-t' : 'img' , '-c' : '1' , '-s' : '0' , '-i': 'owon-tds', '-p' : '3000', '-h' : 'none'}

    try:
        options, args = getopt.getopt(sys.argv[1:],"ht:c:s:i:p:") # get the options -t xx -c yy -s nn -i ip-addr -p port -h
    except: 
        usage()

    args_dict.update( options ) # Sort the input into the default parameters

    if args_dict['-h'] != 'none':  # check for help option given, which is empty then
        usage()
        return

    if len(args) > 0:  # additional argument present?
        fname = args[0] # that must be the filename
    else:
        fname = "-"

    skip = int(args_dict['-s'])
    dtype = args_dict['-t'][0].lower()
    port = int(args_dict['-p'])
    ipaddr = args_dict['-i']

    if dtype == 'i':  # read image
        if args_dict['-c'].upper() in ("BMP", "JPG", "PNG"):
            read_data("IMAGE", args_dict['-c'].upper(), (ipaddr, port), fname, skip)
        else:
            read_data("IMAGE", "", (ipaddr, port), fname, skip)
    elif dtype == 's': # read actual screen content, to be decoded. Header size is 278 bytes
        read_data("CUTDATA", "", (ipaddr, port), fname, skip)
    elif dtype == 't': # read full track data, to be decoded. Header size is 74 bytes before the raw data
        channel=args_dict['-c'][0]
        read_data("FULLDATA", "CH" + channel, (ipaddr, port), fname, skip)
    elif dtype == 'f': # read actual screen content, to be decoded. Header size is 278 bytes
        if args_dict['-c'] == '1': # default
#            read_data("ROOTDIR", "", (ipaddr, port), "", skip)
            print_dir(read_data("INNERFILE", "/D", (ipaddr, port), "", skip))
        else:
            read_data("INNERFILE", "/D/" + args_dict['-c'], (ipaddr, port), fname, skip)
    else:
        sys.stderr.write ("Unkown data type: %s \n" % args_dict['-t'])

##
## That's it
##
# Main program calling stub
if __name__ == '__main__':
    main()
