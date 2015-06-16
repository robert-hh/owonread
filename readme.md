
# Owonread: Reading data from the Owon DTS Series oscilloscopes

This is small Python3 script to read the bitmap image, binary image and the 
full track data from an OWON TDS-Model oscilloscope using LAN. 
It's quick and dirty, but seems to work. 
The preferred habitat is Linux, but it should work on OS X and Windows too.

Usage:

owonread OPTION filename
   Options: 
   -t type: type for data - image | track | screen | file
   -c selection: select channel 1/2/3/4 for track data, 
                 jpg/bmp/png for image, file name for file
   -s # : skip the first # byte from the scope
   -i ip_addr: IP-Address of the oscilloscope
   -p port : port number - default 3000
   -h print these few help lines

If the file name is missing or '-', the data is written to stdout

Default: image = BMP, skip = 0, ip_addr = 'owon.tds', port = 3000, selection = 1/BMP

Reading the file system is pretty basic. If with option -t f no file name is
given in option -c, the to level directory is displayed. If a file name is
give in option -c, this file is read.

It's work in progress. Open tasks: 
    - Decode the header coming with full track and binary screen data

