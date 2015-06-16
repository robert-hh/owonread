
This is small Python3 script to read the bitmap image, binary image and the 
full track data from an OWON TDS-Model oscilloscope using LAN. 
It's quick and dirty, but seems to work. 
The preferred habitat is Linux, but it should work on OS X and Windows too.

readowon OPTION filename
   Options: 
   -t type: type for data - image | track | screen
   -c selection: select channel 1/2/3/4 for track data, jpg/bmp/png for image
   -s # : skip the first # byte from the scope
   -i ip_addr: IP-Address of the oscilloscope
   -p port : port number - default 3000
   -h print these few help lines
If the file name is missing or '-', the data is written to stdout
Default: image = BMP, skip = 0, ip_addr = 'owon.tds', port = 3000, selection = 1/BMP

It's work in progress. Open tasks: 
    - Decode the header coming with full track and binary screen data
    - reading files from the file system

This morning, Owon supplied a files documenting the communication protocol, just one
day after I made the first version of this script. That supported me in adding the
JPG/PNG options.

B.T.W.: You can logon into the TDS-models with telnet and user root w/o password.

