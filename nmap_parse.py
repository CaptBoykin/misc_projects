# NMAP Parse - Tyler Boykin
#
#- Parses NMAP output to CSV
#
# (Currently) Supported Formats
# - XML
# - Greppable
# 
# This is another capstone of mine, with emphasis on pure python
#
# TO DO LIST:
# - Normal Output
# - Automatically check and install 
#   python modules
# - Expand output to more info
#
###################################

import xmltodict, os, sys, getopt


def usage():
    print("""
++++++++++++++++++++++++++++++++
NMAP Parser - Tyler Boykin

usage
- python3 ./nmap_parser.py [OPTION] -i [IN FILE] -o [OUTFILE]
- Example: python3 nmap_parse.py -g -i /my/file -o /home/myout.csv

Options:
    -x|--xml        Parse NMAP XML Output
    -n|--normal     Parse Normal NMAP Output
    -g|--grepable   Parse Grepable NMAP Output
    -i|--infile     Input File
    -o|--outfile     Output File (ie../home/myout.csv)
    -h|--help       Halp plz..
++++++++++++++++++++++++++++++++
    """)

######  XML  ##########
def xml_parse(INFILE,OUTFILE):
    print("XML PARSE: INPUT {} OUTPUT {}".format(INFILE,OUTFILE))

    # PRE-FLIGHT CHECK FOR OUTFILE
    print("Checking if outfile already exists...")
    if not os.path.exists(OUTFILE):
        print("Creating outfile: "+OUTFILE)
        f = open(OUTFILE,'w')
        f.write("IP_ADDR,PORT_NUM,PORT_STATE,PORT_PROTO,PORT_SERV,VENDOR\n")
        f.close()

    # FILE HANDLER / XML HANDLER
    fileH4 = open(INFILE,'r')
    xmlH = xmltodict.parse(fileH4.read())

    # ITERATING THROUGH EACH HOSTS VALUES
    for i in range(0, len(xmlH['nmaprun']['host'])):
        IP = xmlH['nmaprun']['host'][i]['address'][0]['@addr'].strip()

        for x in range(0,len(xmlH['nmaprun']['host'][i]['ports']['port'])-1):
            PORT_NUM = xmlH['nmaprun']['host'][i]['ports']['port'][x]['@portid'].strip()
            PORT_STATE = xmlH['nmaprun']['host'][i]['ports']['port'][x]['state']['@state'].strip()        
            PORT_PROTO = xmlH['nmaprun']['host'][i]['ports']['port'][x]['@protocol'].strip()
            PORT_SERV = xmlH['nmaprun']['host'][i]['ports']['port'][x]['service']['@name'].strip()
            VENDOR = xmlH['nmaprun']['host'][i]['address'][1]['@vendor'].strip()

            OUTPUT = IP+","+PORT_NUM+","+PORT_STATE+","+PORT_PROTO+","+PORT_SERV+","+VENDOR
            APPEND = "echo "+OUTPUT+" >> "+OUTFILE
            callH4 = os.popen(APPEND)

    fileH4.close()
    sys.exit(0)


######  GREPABLE OUTPUT  #####
def grep_parse(INFILE,OUTFILE):
    print("GREP PARSE: INPUT {} OUTPUT {}".format(INFILE,OUTFILE))

    # PRE-FLIGHT CHECK FOR OUTFILE
    print("Checking if outfile already exists...")
    if not os.path.exists(OUTFILE):
        print("Creating outfile: "+OUTFILE)
        fileH3 = open(OUTFILE,'w')
        fileH3.write("IP_ADDR,PORT_NUM,PORT_STATE,PORT_PROTO,PORT_SERV,OS_INFO\n")
        fileH3.close()

    # GRABBING THE IP
    IP_ADDR = "cat "+INFILE+" |  grep 'Ports' | cut -d':' -f2 | cut -d' ' -f2"
    callH1 = os.popen(IP_ADDR)
    cHresult1 = callH1.read().strip().split('\n')
    IP_ADDR = cHresult1

    # GRABBING EVERYTHING ELSE
    for IP in IP_ADDR:
        PORT_NUM = "cat "+INFILE+" |  grep "+IP+" | grep 'Ports' | cut -d':' -f3"
        callH2 = os.popen(PORT_NUM)
        cHresult2 = callH2.read().strip().split('\n')
        PORTS = cHresult2
        PORTS = PORTS[0].split(',')

        OS_INFO = "cat "+INFILE+" |  grep "+IP+" | grep 'Ports' | cut -d':' -f5"
        callH3 = os.popen(OS_INFO)
        cHresult3 = callH3.read().split('|')
        OS_INFO = cHresult3[0].strip()
        
        # ITERATING THROUGH THE RESULT AND ASSIGNING VALUES
        for i in range(0,len(PORTS)):
            PORTS[i] = PORTS[i].split('/')
            PORT_NUM = PORTS[i][0].strip()
            PORT_STATE = PORTS[i][1].strip()
            PORT_PROTO = PORTS[i][2].strip()
            PORT_SERV = PORTS[i][4].strip()
            OUTPUT = IP+","+PORT_NUM+","+PORT_STATE+","+PORT_PROTO+","+PORT_SERV+","+OS_INFO
            APPEND = "echo "+OUTPUT+" >> "+OUTFILE
            callH3 = os.popen(APPEND)
        
    sys.exit(0)

#######  NORMAL OUTPUT PARSING (UNDER CONSTRUCTION) ##
def normal_parse(INFILE,OUTFILE):
    print("NORMAL PARSE: INPUT {} OUTPUT {}".format(INFILE,OUTFILE))
    sys.exit(0)


####### MAIN #######
def main():
    INFILE=''
    OUTFILE=''
    XML=False
    GREP=False
    NORMAL=False

    ## ARGUMENT PARSING ##
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hxgni:o:", ["help","xml","grepable","normal","infile","outfile"])
    except getopt.GetoptError:
        print(err)
        usage()
        sys.exit(2)

    ## ARGUMENT TO VARIABLE ASSIGNMENT ##
    for o,a in opts:
        if o in ("-h","--help"):
            usage()
            sys.exit(0)
        elif o in ("-x","--xml"):
            XML=True
        elif o in ("-g","--grepable"):
            GREP=True
        elif o in ("-n","--normal"):
            NORMAL=True
        elif o in ("-i","--infile"):
            INFILE=a
        elif o in ("-o","--outfile"):
            OUTFILE=a
        else:
            assert False, "Unhandled Option!"

    ## PARAM VERIFICATION AND FUNCTION CALL #
    if XML and OUTFILE and INFILE:
        if os.path.exists(INFILE):
            xml_parse(INFILE, OUTFILE)
        else:
            print("XML Input File Does Not Exist!")
            sys.exit(2)
    elif GREP and OUTFILE and INFILE:
        if os.path.exists(INFILE):
            grep_parse(INFILE, OUTFILE)
        else:
            print("GREP Input File Does Not Exist!")
            sys.exit(2)
    elif NORMAL and OUTFILE and INFILE:
        if os.path.exists(INFILE):
            normal_parse(INFILE, OUTFILE)
        else:
            print("NORMAL Input File Does Not Exist!")
            sys.exit(2)
    else:
        print("\nPlease Provide All Required Arguments!\n[FORMAT] [INFILE] [OUTFILE]\n")
        usage()
        sys.exit(2)

main()
