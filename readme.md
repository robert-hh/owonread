
#Owonread: Get data from Owon DTS Series oscilloscopes

**Description**

This is small Python3 script to read the screen image, binary images, the 
full track data and files from an OWON TDS-Model oscilloscope using LAN. 
It's quick and dirty, but seems to work.  The preferred habitat is Linux, 
but it should work on OS X and Windows too, since no OS-specific syntax is used.

**Usage**
```
python3 owonread.py [OPTIONS] [source] [target]

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
```   
If the target file name is missing or '-', the data is written to stdout<br>
Defaults: type = bmp, skip = 0, get = all, ip_addr = 'owon.tds', port = 3000<br>

The script contains a shebang line, so you can start it without typing python3 upfront, if you tag is as executable. 
On your system, python3 may be python. 


**Examples:**

`python3 owonread.py image001.bmp`<br>
    *get the screen image as BMP file and store it into image001.bmp*

`python3 owonread.py -t jpg image002.jpg`<br>
    *get the screen image as BMP file*

`python3 owonread.py -t ch1 fulldata.bin`<br>
    *get the full content of CH1 data buffer*

`python3 owonread.py -t ch3 -s 78 rawdata.bin`<br>
    *get the full content of CH3 track buffer, skipping the first 78 bytes with header information*
    
`python3 owonread.py -t dir`<br>
    *Show the list of files stored in the data section of the oscillscope* 

`python3 owonread.py -t file /D/owon00001.csv pulse_response.csv`<br>
    *read the file owon0001.csv from the device and store it as pulse_response.csv*

`python3 owonread.py | display`<br>
    *get the actual screen image and pipe it into the Linux display command*
            
**Notes**
 
- It's work in progress. Open task: Decode the header coming with full track, allowing to send it to e.g. gnuplot. 
Owon provided some information about the header structure, but it does not fit yet properly.
- The skip and get options are obviously obsolete, since you could do the same with the Linux **head** command.

