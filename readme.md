
#Owonread: Get data from Owon DTS Series oscilloscopes

**Description**

This is small Python3 script to read the screen image, binary images, the 
full track data and files from an OWON TDS-Model oscilloscope using LAN. 
It's quick and dirty, but seems to work.  The preferred habitat is Linux, 
but it works as well on OS X and Windows.

**Usage**
```
python3 owonread.py [OPTIONS] [source] [target]

Options:
   -t type: data type, as of: bmp jpg png ch1 ch2 ch3 ch4 screen dir file
      type bmp, jpg and png get the screen image in the respective format
      type ch1, ch2, ch3 and ch4 get the deep track data of that channel
      type screen gets the binary screen content
      type dir shows the content of the devices file storage. If the optional 
           parameter source is 'all', the files on an USB drive a displayed as 
           well
      type file gets a file. The full path name as shown with the 
          command dir must be supplied. 
   -s # : skip the first # bytes of the data from the device
   -g # : get the following # bytes of the data from the device
   -i ip_addr: IP-Address of the oscilloscope
   -p port : port number, default 3000
   -h print these few help lines

If the target file name is missing, the data is written to stdout
Defaults: type = bmp, skip = 0, get = all, ip_addr = 'owon-tds', port = 3000
```
The script contains a shebang line, so you can start it without typing python3 upfront, if it is tagged as executable. On your system, python3 may be python. 


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

`python3 owonread.py -t dir all`<br>
    *Show the list of files stored in the data section of the oscillscope and in the attached USB drive* 

`python3 owonread.py -t file /D/owon00001.csv pulse_response.csv`<br>
    *read the file owon0001.csv from the device and store it as pulse_response.csv*

`python3 owonread.py | display`<br>
    *get the actual screen image and pipe it into the Linux display command*
            
**Notes**
 
- Directories can be read as a file, using the file data type and the name of the directory as the source.

