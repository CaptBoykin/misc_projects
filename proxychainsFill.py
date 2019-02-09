#!/usr/bin/python3

# I got tired of looking for random proxies so I made this to fill the
# proxychains .conf file for me.

# 1. Makes a backup of the old proxychains (/etc/proxychains.conf)
#    and stores it as (/etc/proxychains_old.conf)
# 2. Creates a temp output file (/tmp/proxychains_updated.conf)
# 3. Tmp output file becomes active .conf file
# 4. Tmp file removed

# This does not validate the proxy if it works.  That's coming soon

__author__ = 'Tyler Boykin'

from bs4 import BeautifulSoup
import sys, inspect, requests, base64, subprocess, getopt

OUTFILE="/tmp/proxychains_updated.conf"
INFILE="/etc/proxychains.conf"

# Debugging macro...
def BLURT():
    print(inspect.currentframe().f_back.f_lineno)

# In progress....
def usage():
    pass

# Returns the last line number of the specified file
def return_eof():
    completed = subprocess.run("wc -l /etc/proxychains.conf | awk '{print $1}'",
                                            check=True,shell=True,stdout=subprocess.PIPE,)
    eof = int(completed.stdout.decode('utf-8').strip())
    return eof


def reload_conf():
    BLURT()
    subprocess.run(["wget","https://raw.githubusercontent.com/haad/proxychains/master/src/proxychains.conf","-O","/etc/proxychains.conf"])
 
def url1(infile,outfile):
    #URL1 = https://proxy-list.org/english/index.php
    url_1 = "https://proxy-list.org/english/index.php?p="
    url_1_name = "Proxy-List.org"
    print("Harvesting Proxy-List.org")
    outfile.write("# Proxy-List.org\n")

    # For multiple pages
    for x in range(1, 10):
        url = "{0}{1}".format(url_1,x)
        outfile.write("# From {0}\n".format(url))

        # Initial request and data processing
        try:
            reqHandler = requests.get(url,timeout=10)
        except requests.exceptions.Timeout:
            print("Timeout Occurred!")
                        
        data = reqHandler.text
        soup = BeautifulSoup(data,"lxml")
        list_len = len(soup.find_all("li",class_="proxy"))

        # Iterating over the fields and writing to file
        for i in range(1, list_len):
            addrs = soup.find_all("li",class_="proxy")[i].get_text().split("'")
            addrs = str(base64.b64decode(addrs[1]),'utf-8').split(":")
            ip  = addrs[0]
            port  = addrs[1]
            proto = soup.find_all("li",class_="https")[i].get_text().split("'")[0]
                
            if proto == '-':
                continue
            
            outfile.write("{0} {1} {2}\n".format(proto,ip,port))
        print("Done with {0}".format(url))

def url2(infile,outfile):               
    #URL2 = https://www.socks-proxy.net/
    url_2 = "https://www.socks-proxy.net/"
    print("Harvesting from Socks-Proxy.net")
    outfile.write("# From {0}\n".format(url_2))
    try:
        reqHandler = requests.get(url_2,timeout=10)
    except requests.exceptions.Timeout:
        print("Timeout Occurred!")
                
    data = reqHandler.text
    soup = BeautifulSoup(data,"lxml")
    list_len = len(soup.find_all("td"))

    for i in range(0,list_len,8):
        addrs = soup.find_all("td")[i].get_text()
        port = soup.find_all("td")[i+1].get_text()
        outfile.write("socks4 {0} {1}\n".format(addrs,port))
        outfile.write("socks5 {0} {1}\n".format(addrs,port))
    print("Done with {0}".format(url_2))
 
    
def main():
    APPEND  = False
    RELOAD  = False
    try:
        opts,args = getopt.getopt(sys.argv[1:],"ar",["append","reload"])
    except getopt.GetoptError:
        print(err)
        sys.exit(2)

    for o,a in opts:
        if o in ("-a","--append"):
            APPEND = True
        elif o in ("-r","--refill"):
            RELOAD = True
        else:
            assert False, "Unhandled Option!"
            usage()
            sys.ext(2)

    # Reload downloads a fresh configuration file from github
    if RELOAD:
        reload_conf()

    # Before we do anythiung we make a backup of the original config file
    try:
        subprocess.run(["cp","/etc/proxychains.conf","/etc/proxychains_old.conf"])
    except OSError:
        print("Error copying file /etc/proxychains.conf")

    try:
        infile = open(INFILE,'r')
    except OSError:
        print("Error opening file {0}\n".format(INFILE))

    try:
        outfile = open(OUTFILE,'a')
    except OSError:
        print("Error opening file {0}\n".format(OUTFILE))

    eof = return_eof()
    # Check to see if bottom of page
    for line,data in enumerate(infile):
        if line < eof:
            outfile.write(data)
        if line == (eof-1):
            url1(infile,outfile)
            url2(infile,outfile)

    outfile.truncate()
    outfile.close()
    infile.close()
    subprocess.run(["mv",OUTFILE,INFILE])


main()
