#!/usr/bin/env python3
#
# read image or trace from scope
#
import struct
import sys
import socket
import getopt

def read_data(cmd_txt, server_addr, fname, skip):
    try:
        s = socket.socket()
        s.connect(server_addr)
        if s:
# send command
            cmd = struct.pack("<l%ds" % len(cmd_txt), len(cmd_txt), cmd_txt.encode())
            s.send(cmd)
# get length of response
            ss = s.recv(4)
            size = struct.unpack("<l", ss)[0]
# skip header
            hdr_size = len(cmd_txt) + 4
            name = s.recv(hdr_size)
            size -= hdr_size
# open file
            if fname == '-': 
                f = sys.stdout
            else:
                f = open(fname, "wb")
# if additional skip, do it
            if skip:
                img = s.recv(skip)
                size -= skip
# get bulk data
            nrecv = 0
            while nrecv < size:
                img = s.recv(size - nrecv)
                f.buffer.write(img)
                nrecv += len(img)
# and that's it
            if f != sys.stdout:
                f.close()
            s.close()
            return True
    except Exception as err:
        sys.stderr.write("Error attempting to get data, reason %s\n" % err)
        return False

def usage():
    print ("readowon OPTION filename\n" \
            "   Options: \n"\
            "   -t type: type for data - image | track | screen\n" \
            "   -c channel: select channel for track data\n" \
            "   -s # : skip the first # byte from the scope\n" \
            "   -i ip_addr: IP-Address of the oscilloscope\n" \
            "   -p port : port number - default 3000\n" \
            "   -h print these few help lines\n" \
            "If the file name is missing or '-', the data is written to stdout\n"\
            "Default: image, skip = 0")


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
    channel=args_dict['-c'][0]
    port = int(args_dict['-p'])
    ipaddr = args_dict['-i']

    if dtype == 'i':  # read image
        read_data("IMAGE", (ipaddr, port), fname, skip)
    elif dtype == 's': # read actual screen content, to be decoded. Header size is 278 bytes
        read_data("CUTDATA", (ipaddr, port), fname, skip)
    elif dtype == 't': # read full track data, to be decoded. Header size is 74 bytes before the raw data
        read_data("FULLDATACH" + channel + '\x7c', (ipaddr, port), fname, skip)
    else:
        sys.stderr.write ("Unkown data type: %s \n" % args_dict['-t'])

##
## That's it
##
# Main program calling stub
if __name__ == '__main__':
    main()
