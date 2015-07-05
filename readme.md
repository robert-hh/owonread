
#Owonread: Get track data, files and screen shots from Owon TDS Series oscilloscopes

**Description**

This is small Python3 script for reading the screen image, binary images, the 
full track data and files from an OWON TDS-Model oscilloscope using LAN. 
The preferred habitat is Linux, but it works as well on OS X and Windows, 
with the usual piping problems in Windows.

**Usage**
```
python3 owonread.py [OPTIONS] action [target]

action:
    data type to read, as of: bmp jpg png ch1 ch2 ch3 ch4 screen dir file_name
      bmp, jpg and png get the screen image in the respective format
      ch1, ch2, ch3 and ch4 get the deep track data of that channel
      screen delivers the binary screen content of all visible tracks
      dir shows the content of the devices file storage. If the option 
          -a is given, the files on an USB drive are displayed as well
      if action starts with the letter /, a file is read from the devices file storage.
          The full path name as shown with the command dir must be supplied. 
Options:
   -a show all files includes those on attached USB drives
   -s # : skip the first # bytes of the data from the device
   -g # : get the following # bytes of the data from the device
   -i ip_addr: IP-Address of the oscilloscope
   -p port : port number, default 3000
   -h print these few help lines
   
If the target file name is missing, the data is written to stdout
Defaults: skip = 0, get = all, ip_addr = 'owon-tds', port = 3000, action = bmp
```
The script contains a shebang line, so you can start it without typing python3 upfront, if it is tagged as executable. On your system, python3 may be python. 


**Examples:**

`python3 owonread.py bmp image001.bmp`<br>
    *get a screen shot as BMP file and store it into image001.bmp*

`python3 owonread.py jpg image002.jpg`<br>
    *get a screen shot as jpg file and store it into image002.jpg*

`python3 owonread.py ch1 fulldata_ch1.bin`<br>
    *get the full content of CH1 data buffer*

`python3 owonread.py -s 78 ch3 rawdata.bin`<br>
    *get the full content of CH3 track buffer, skipping the first 78 bytes with header information*
    
`python3 owonread.py dir`<br>
    *Show the list of files stored in the data section of the oscilloscope* 

`python3 owonread.py -a dir`<br>
    *Show the list of files stored in the data section of the oscilloscope and on an attached USB drive* 

`python3 owonread.py screen`<br>
    *get the traces of all channels as shown on the screen, including the math trace* 

`python3 owonread.py /D/owon00001.csv pulse_response.csv`<br>
    *read the file /D/owon0001.csv from the device and store it as pulse_response.csv*

`python3 owonread.py | display`<br>
    *get a screen shot and pipe it into the Linux display command*
            
**Notes**
 
- Directories can be read as files, using name of the directory as the file name.

**Files**
 
- owonread.py   The Python script that performs the magic
- TDS Protocol.doc  A description of the communication protocol and the structure of the data exchanged
- readme.md  This file
- fullprint.py  a sample python script which prints the header of the full trace data file, obtained with owonread and file type option  ch1, ch2, ch3 or ch4. 
- cutprint.py a sample python script which prints the header of the screen type data file, obtained with owonread and the file type option screen. 

The latter two scripts do not create a nicely formatted output. I just used them to match the various setting of the device with what is delivered with the command responses. I present them here for convenience of others in implementing their data file processing.
