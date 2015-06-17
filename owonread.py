#!/usr/bin/env python3
#
# read image or trace from scope
#
import sys
import socket
from getopt import getopt
from struct import pack, unpack
from binascii import unhexlify
import time

def read_data(cmd_txt, parm,  server_addr, fname, skip, get):
    res = b""
    try:
        s = socket.socket()
        s.settimeout(5)
        s.connect(server_addr)
        if s:
# pack & send command
            cmd = cmd_txt + parm
            cmd = pack("<l%ds" % len(cmd), len(cmd), cmd.encode())
            s.send(cmd)
# get length of response
            ss = s.recv(4)
            size = unpack("<l", ss)[0]
# skip header
            hdr_size = len(cmd_txt) + 4
            name = s.recv(hdr_size)
            size -= hdr_size
# open file, if required
            if fname != "":
                if fname != "-":
                    f = open(fname, "wb")
                else:
                    f = sys.stdout
# if additional skip, do it
            while skip > 0:
                img = s.recv(skip)
                size -= len(img)
                skip -= len(img)
# check, whether not the full data is required
            if get > 0 and get < size:
                skip = size - get
                size = get
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
# eat up what's left                
            while skip > 0:
                img = s.recv(skip)
                skip -= len(img)
# and that's it
            if fname != "" and fname != "-":
                f.close()
            s.close()
            return res
    except Exception as err:
        sys.stderr.write("Error attempting to get data, reason %s\n" % err)
        return False

# Print a directory file
def print_dir(d, recurse, ipaddr, port):
    s = read_data("INNERFILE", d, (ipaddr, port), "", 0, 0)
    pos = 0
    while pos < len(s):
# entry type
        if s[pos] == 1 and recurse: # recurse into dir
            print_entry(d, s, pos)  # first print the entry itself
            newdir = "" # collect name
            pos += 17
            while s[pos] != ord('|'):
                newdir += chr(s[pos])
                pos += 1
            pos += 1
            if newdir:
                print_dir(d + "/" + newdir, True, ipaddr, port)
        else:   # print entry
            pos = print_entry(d, s, pos)

# print a directory entry at pos
def print_entry(d, s, pos):
    if s[pos] == 1:
        print ("d ", end="")
    else:
        print ("- ", end="")
# file size
    size = unpack(">l", unhexlify(s[pos+1:pos+9]))[0]
    print ("%9d " % size, end="")
    pos += 9
# date
    ftime = unpack(">l", unhexlify(s[pos:pos+8]))[0]
    print (time.strftime("%Y-%m-%d %H:%M:%S ", time.gmtime(ftime)), end="")
    pos += 8
# path + name
    print (d + "/", end="")
    while s[pos] != ord('|'):
        print (chr(s[pos]), end="")
        pos += 1
    print("");
    pos += 1
    return pos

def usage():
    sys.stderr.write ('''
owonread [OPTIONS] [source] [target]

Options:
   -t type: data type, as of: bmp jpg png ch1 ch2 ch3 ch4 screen dir file
      types bmp jpg png get the screen picture
      types ch1 ch2 ch3 ch4 get the deep trach data of that channel
      type screen gets the binary screen content
      type dir shows the content of the devices file store
      type files get a file. The full path name as shown with dir must
         be supplied. 
   -s # : skip the first # bytes of the data from the device
   -g # : get the following # bytes of the data from the device
   -i ip_addr: IP-Address of the oscilloscope
   -p port : port number, default 3000
   -h print these few help lines
   
If the target file name is missing or '-', the data is written to stdout
Defaults: type = bmp, skip = 0, get = all, ip_addr = 'owon.tds', port = 3000
''')


def main():
#
# look for command line arguments
#
    args_dict = { '-t' : 'BMP' , '-s' : '0' , \
                  '-i': 'owon-tds', '-p' : '3000', '-g' : '0' , '-h' : 'none'}

    try:
        options, args = getopt(sys.argv[1:],"ht:s:i:p:g:") # get the options -t xx -s # -i ip-addr -p port -k # -h
    except: 
        sys.stderr.write("Option not defined, Usage:\n")
        usage()
        return

    args_dict.update( options ) # Sort the input into the default parameters

    if args_dict['-h'] != 'none':  # check for help option given, which is empty then
        usage()
        return

    if len(args) > 0:  # additional argument present?
        fname = args[0] # that must be the filename
    else:
        fname = "-"

    dtype = args_dict['-t'].upper()
    skip = int(args_dict['-s'])
    get = int(args_dict['-g'])
    port = int(args_dict['-p'])
    ipaddr = args_dict['-i']

    if dtype in ("BMP", "JPG", "PNG"):  # read image
        read_data("IMAGE", dtype, (ipaddr, port), fname, 0, 0)
    elif dtype == 'SCREEN': # read actual screen content, to be decoded. Header size is 278 bytes
        read_data("CUTDATA", "", (ipaddr, port), fname, skip, get)
    elif dtype in ("CH1", "CH2", "CH3", "CH4"): # read full track data, to be decoded. Header size is 74 bytes before the raw data
        read_data("FULLDATA", dtype, (ipaddr, port), fname, skip, get)
    elif dtype == 'DIR': # read Directory
        print("\nDirectory of Files:");
        print_dir("/D", True, ipaddr, port)
        print("")
    elif dtype == 'FILE': # read files from scope
        if fname != "-":
            dtype = fname
            if len(args) > 1:  # additional argument present?
                fname = args[1] # that must be the filename
            else:
                fname = "-"
            read_data("INNERFILE", dtype, (ipaddr, port), fname, 0, 0)
        else:
            sys.stderr.write("Error: Source file name missing\n")
    else:
        sys.stderr.write ("Wrong data type: -t %s\n" % args_dict['-t'])

##
## That's it
##
# Main program calling stub
if __name__ == '__main__':
    main()
