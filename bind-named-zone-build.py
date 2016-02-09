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

#creating the zone files
def zone(zonePath, domain):
    zoneSerial = 1000                           #The Starting Serial number for the zone
    zoneRefresh = 86400                         #The Refresh time for the zone
    zoneRetry = 3600                            #The Retry time for the zone
    zoneExpiry = 604800                         #The Max time that Cached entries can live
    zoneNxDomain = 3600                         #The Minimum time that Cached entries live
    
    zoneTTL = 38400                             #The TTL for the domain
    zoneDNSServer = ["ns1", "ns2.example.com."] #The DNS servers for the zone
        
    cwd = os.path.dirname(os.path.abspath(__file__)) + "/" #We are here
    
    if not os.path.exists(cwd+zonePath[1:]):     #Does the path exist for the zonePath
        os.makedirs(cwd + zonePath[1:])         #Lets create it
    
    if re.search("arpa", domain):               #Are we creating a reverse zone
        zoneFile = cwd + zonePath[1:] + domain  #This is where we will save the generated zone file
    else:                                       #If were not create a reverse zone file
        zoneFile = cwd + zonePath[1:] + domain + ".hosts" #This is where we will save the generated zone file
    
    if domain[-1] != ".":                       #Sytnax Checking to ensure that we are using a FQDN
        domain += "."
    
    zoneDNSadmin = "dnsadmin." + domain         #The zone adminstrators email can be replaced with admin.example.com.
    
    for x in range(0,len(zoneDNSServer)):       #Sytnax Checking for the DNS Servers
        if zoneDNSServer[x][-1] != ".":
            zoneDNSServer[x] += domain
    
    zoneDNSadmin = zoneDNSadmin.replace("@", ".").lower() #Syntax Checking for the DNS admin email replacing "@" with "."
    if zoneDNSadmin[-1] != ".":                 #Syntax Checking for the DNS admin email ensure that it ends with a dot
        zoneDNSadmin += "."
    
    print("Creating zone file at \"%s\"\n" % zoneFile)
    
    with open(zoneFile, "w") as zf:                  #Lets write the zone file using the standard format
        zf.write("$TTL %s\n" % zoneTTL)         #Start SOA record
        zf.write("@\tIN\tSOA\t%s\t%s (\n" % (zoneDNSServer[1],zoneDNSadmin))
        zf.write("\t\t\t\t%s\n" % zoneSerial)
        zf.write("\t\t\t\t%s\n" % zoneRefresh)
        zf.write("\t\t\t\t%s\n" % zoneRetry)
        zf.write("\t\t\t\t%s\n" % zoneExpiry)
        zf.write("\t\t\t\t%s )\n" % zoneNxDomain) #End SOA Record
        for dnsServer in zoneDNSServer:         #Create the NS records
            zf.write("@\tIN\tNS\t%s\n" % dnsServer)     

#main funtion of the program
def main():
    fileDomains = "domains.txt"                 #A list of domains
    type = "master"                              #This should be weither "slave" or "master"
    masters = ["1.1.1.1", "2.2.2.2"]            #A list of master servers
    
    fileNamed = "named.conf"                    #The output file
    zonePath = "/var/named/"                    #The location of the zone files
    
    with open(fileDomains,"r") as domains:      #Open domains file
        with open(fileNamed,"w") as namedConf:  #Open named.conf file
            for domain in domains:              #Loop through the list of domains
                domain = domain.strip("\n")     #Remove the newline character
                domain = domain.lower()         #Conver to lower case
                
                print("Creating %s zone %s" % (type,domain))
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
                    
                    zone(zonePath, domain)      #Generate the zone file for the domain
                else:                           #if the type is not master or slave
                    print("%s is not a valid zone type") 
                    sys.exit(1) #goodbye
                    
                namedConf.write("};\n\n")       #Close the zone
    sys.exit(0)

if __name__ == "__main__": #if we are being called from the shell enter main()
	main()