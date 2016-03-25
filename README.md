BiNetflowToSIGs
======

BiNetflowToSIGs is short for converting BiNetflow file To Social Interaction Graphs file.


Usage
=====
Assuming having set `binetflowtosigs_ROOT` path variable correctly, then type `./binetflowtosigs -h` to get the following help message:
```
usage: binetflowtosigs [-h] [-w W] [-p P] [-d D] [-s S] [-e]

optional arguments:
  -h, --help  show this help message and exit
  -w W        window size; default=1
  -p P        path to raw data; default='/home/jzh/Dropbox/Research/Botnet_det
              ection/BiNetflowToSIGs_Data/capture20110816.binetflow.sample'
  -d D        folder for saving output SIGs file; default='/home/jzh/Dropbox/R
              esearch/Botnet_detection/BiNetflowToSIGs_Data/'
  -s S        name of standard output SIGs file; default='result.sigs'
  -e          whether or not to enable the botnet_nodes output; default=False
```

Note: You may need to change the path to your Data folder.

Examples:
====

 `$ ./binetflowtosigs -w 0.01 -p ./demo/capture20110816.binetflow.sliced -d ./demo/`
 
 `$ ./binetflowtosigs -p /home/jzh/Dropbox/Research/Botnet_detection/BiNetflowToSIGs_Data/capture20110816.binetflow.slice_13_1 -w 1 -s capture20110816.binetflow.slice_13_1.sigs -e`


Author
=============
Jing Zhang

Jing Zhang currently is a PhD student in the Division of Systems Engineering at Boston University, advised by Professor [Yannis Paschalidis](http://sites.bu.edu/paschalidis/).


Email: `jzh@bu.edu`

Homepage: http://people.bu.edu/jzh/


Copyright 2015 Jing Zhang. All rights reserved. BiNetflowToSIGs is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software Foundation.
