
This is small Python3 script to read the bitmap image, binary image and the 
full track data from an OWON TDS-Model oscilloscope using LAN. 
It's quick and dirty, but seems to work. 
The preferred habitat is Linux, but it should work on OS X and Windows too.

readowon OPTION filename
   Options: 
   -t type: type for data - image | track | screen
   -c channel: select channel for full track data capture
   -s # : skip the first # byte from the scope
   -i ip_addr: IP-Address of the oscilloscope
   -p port : port number - default 3000
   -h print these few help lines
If the file name is missing or '-', the data is written to stdout
Default: image, skip = 0, ip_addr = 'owon.tds', port = 3000, channel = 1

It's work in progress. Open tasks: 
    - Decode the header coming with full track and binary screen data
    - reading files from the file system

B.T.W.: You can logon into the TDS-models with telnet and user root w/o password.

