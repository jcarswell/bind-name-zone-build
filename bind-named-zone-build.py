#!/usr/bin/python

## Bind Named Zone Config Builder: is a simple script which takes a list of domains
##	and output a named.conf file with all of the configuration of all
##	of the domains.
##
## Setup notes:
## ============
##
## Please set the variables fileDomains, type and masters if type is slave.
##
## If you wish to change the output file name and/or location set change 
##	the variable fileNamed to the path/name desired
##
## If you wish to change the path that your zone files are stored change the
##	variable zonePath to the desired location
##
## If you are creating a file for a Windows system ensure that you escape
##  the backslashed i.e. "\\"
##
## 
## Created by Josh Carswell on February 8th 2016
## Licensed under GUN GPL v3 see LICENSE.txt

import sys
import os
import re

def main():
	fileDomains = "domains.txt"                 #A list of domains
	type = "slave"                              #This should be weither "slave" or "master"
	masters = ["1.1.1.1", "2.2.2.2"]            #A list of master servers
	
	fileNamed = "named.conf"                    #The output file
	zonePath = "/var/named/"                    #The location of the zone files

	with open(fileDomains,"r") as domains:	    #Open domains file
		with open(fileNamed,"w") as namedConf:  #Open named.conf file
			for domain in domains:			    #Loop through the list of domains
				domain = domain.strip("\n")     #Remove the newline character
				domain = domain.lower()         #Conver to lower case
				
				namedConf.write("zone \"%s\" {\n" % domain) #Write the zone derective
				namedConf.write("\ttype %s;\n" % type) #Write the zone type
				
				if type == "slave":             #If the zone is a slave do the following
					if re.search("arpa", domain): #If the zone is a rev domain don't add .hosts to the zone file path
						namedConf.write("\tfile \"%sslaves/%s\";\n" % (zonePath, domain) )
					else:                       #Else append .hosts to the zone file name
						namedConf.write("\tfile \"%sslaves/%s.hosts\";\n" % (zonePath, domain) )
					
					namedConf.write("\tmasters {\n") #Write the masters directive
					
					for master in masters:      #Loop through the possible master and write them
						namedConf.write("\t\t%s;\n" % master)
					namedConf.write("\t};\n")   #Close the masters directive
				elif type == "master":          #if the zone is a master do the following
					if re.search("arpa", domain): #If the zone is a rev domain don't add .hosts to the zone file path
						namedConf.write("\tfile \"%s%s\";\n" % (zonePath, domain) )
					else:                       #Else append .hosts to the zone file name
						namedConf.write("\tfile \"%s/%s.hosts\";\n" % (zonePath, domain) )
					namedConf.write("\tnotify yes;\n") #notify slaves
				else:                           #if the type is not master or slave
					print("%s is not a valid zone type") 
					sys.exit(1) #goodbye
					
				namedConf.write("};\n\n")       #Close the zone
	sys.exit(0)
	
if __name__ == "__main__": #if we are being called from the shell enter main()
	main()