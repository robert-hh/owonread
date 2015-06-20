#!/usr/bin/env python3
#
# read image or trace from scope
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from sys import stdout, stderr, argv
from socket import socket
from getopt import getopt
from struct import pack, unpack
from binascii import unhexlify
from time import strftime, gmtime

def read_data(cmd_txt, parm,  server_addr, fname, skip, get):
    res = b""
    try:
        s = socket()
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
                    f = stdout
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
                    if f == stdout:
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
        stderr.write("Error attempting to get data, reason %s\n" % err)
        return False

# Print a directory file
def print_dir(d, recurse, server_addr):
    s = read_data("INNERFILE", d, server_addr, "", 0, 0)
    if s:
        pos = 0
        while pos < len(s):
# entry type
            if s[pos] == 1 and recurse: # recurse into dir?
                print_entry(d, s, pos)  # first print the entry itself
                newdir = "" # collect name
                pos += 17
                while s[pos] != ord('|'):
                    newdir += chr(s[pos])
                    pos += 1
                pos += 1
                if newdir:
                    print_dir(d + "/" + newdir, True, server_addr)
            else:   # print file entry
                pos = print_entry(d, s, pos)

# print a directory entry at pos
def print_entry(d, s, pos):
# directory/file flag in the first byte
    if s[pos] == 1:
        print ("d ", end="")
    else:
        print ("- ", end="")
    pos += 1
# file size in the next 8 bytes
    size = unpack(">l", unhexlify(s[pos:pos+8]))[0]
    print ("%9d " % size, end="")
    pos += 8
# date in the next 8 bytes
    ftime = unpack(">l", unhexlify(s[pos:pos+8]))[0]
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime(ftime)), end="")
    pos += 8
# path + name in the following bytes, terminated by the char '|'
    print (d + "/", end="")
    while s[pos] != ord('|'):
        print (chr(s[pos]), end="")
        pos += 1
    print("");
    return pos + 1

def usage(msg):
    stderr.write(msg)
    stderr.write ('''
python3 owonread.py [OPTIONS] [source] [target]

Options:
   -t type: data type, as of: bmp jpg png ch1 ch2 ch3 ch4 screen dir file
      type bmp, jpg and png get the screen image in the respective format
      type ch1, ch2, ch3 and ch4 get the deep track data of that channel
      type screen gets the binary screen content
      type dir shows the content of the devices file storage
      type file gets a file. The full path name as shown with the 
          command dir must be supplied. 
   -s # : skip the first # bytes of the data from the device
   -g # : get the following # bytes of the data from the device
   -i ip_addr: IP-Address of the oscilloscope
   -p port : port number, default 3000
   -h print these few help lines
   
If the target file name is missing or '-', the data is written to stdout
Defaults: type = bmp, skip = 0, get = all, ip_addr = 'owon-tds', port = 3000
''')


def main():
#
# look for command line arguments
#
# the defaults are defined here
#
    args_dict = { '-t' : 'BMP' , '-s' : '0' , \
                  '-i': 'owon-tds', '-p' : '3000', '-g' : '0' , '-h' : 'none'}

    try:
        options, args = getopt(argv[1:],"ht:s:i:p:g:") # get the options -t xx -s # -i ip-addr -p port -k # -h    
    except: 
        usage("\nInvalid Option, Usage:\n")
        return

    args_dict.update( options ) # Sort the input into the default parameters
# check options and extract values
    if args_dict['-h'] != 'none':  # check for help option given, which is empty then
        usage("")
        return
# set the parameters
    if len(args) > 0:  # additional argument present?
        fname = args[0] # first guess: that is the target filename
    else:
        fname = "-"

    dtype = args_dict['-t'].upper() # change to uppercase
    skip = int(args_dict['-s'])
    get = int(args_dict['-g'])
    port = int(args_dict['-p'])
    ipaddr = args_dict['-i']
# execute
    if dtype in ("BMP", "JPG", "PNG"):  
# read image
        read_data("IMAGE", dtype, (ipaddr, port), fname, 0, 0)
    elif dtype[0] == 'S': 
# read actual screen content, to be decoded. Header size is 282 bytes
        read_data("CUTDATA", "", (ipaddr, port), fname, skip, get)
    elif dtype in ("CH1", "CH2", "CH3", "CH4"): 
# read full track data, to be decoded. Header size is 78 bytes before the raw data
        read_data("FULLDATA", dtype, (ipaddr, port), fname, skip, get)
    elif dtype[0] == 'D': 
# read Directory
        print("\nDirectory of Files:");
        print_dir("/D", True, (ipaddr, port))
        print("")
    elif dtype[0] == 'F': 
# read file from scope. In that case, there must be at least one, and may be a second filename given
        if fname != "-":
            dtype = fname
            if len(args) > 1:  # additional argument present?
                fname = args[1] # that must be the target filename
            else:
                fname = "-"
            read_data("INNERFILE", dtype, (ipaddr, port), fname, 0, 0)
        else:
            stderr.write("Error: Source file name missing\n")
    else:
        stderr.write ("Wrong parameter given with option -t: -t %s\n" % args_dict['-t'])

##
## That's it
##
# Main program calling stub
if __name__ == '__main__':
    main()
