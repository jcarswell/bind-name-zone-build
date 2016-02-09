# Bind Named Zone Config File Builder
:----:

This is a simple script which takes a list of domains and output a named.conf file with all of the configuration of all of the domains.

## Setup notes:
- Please set the variables fileDomains, type and masters if type is slave.
- If you wish to change the output file name and/or location set change the variable fileNamed to the path/name desired.
- If you wish to change the path that your zone files are stored change the variable zonePath to the desired location.
- If you are creating a file for a Windows system ensure that you escape the backslashed i.e. "\\".
 
Created by Josh Carswell on February 8th 2016
Licensed under GUN GPL v3 see LICENSE.txt