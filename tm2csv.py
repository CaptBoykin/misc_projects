#!/usr/env/python3
##################################
# Microsoft Threat Modeling (tm) to CSV - Tyler Boykin (@CaptBoykin)
#
# Takes the Threat Modeling htm file from the Microsoft Threat Modeling tool
# and turns it into a .csv file.
#
# 
# I felt like brushing up on my python while making a tool for future use...
#
###################################

__author__ = 'Tyler Boykin'
from bs4 import BeautifulSoup
from datetime import datetime
import os, sys, getopt, inspect, re

def BLURT():
    print(inspect.currentframe().f_back.f_lineno)

def usage():
    print("""
++++++++++++++++++++++++++++++++

tm2csv - Tyler Boykin (@CaptBoykin)

usage
    - python3 ./tm2csv.py -i [IN FILE] -o [OUTFILE]
    - Example: python3 tm2csv.py -i /my/file.htm -o /home/myout.csv

Options:
    -i|--infile     Input File
    -o|--outfile    Output File (ie../home/myout.csv)
    -h|--help       Halp plz..

++++++++++++++++++++++++++++++++
    """)

######  tm2csv ##########
def tm_parse(INFILE,OUTFILE):
    print("DEBUGGING...: INPUT {} OUTPUT {}".format(INFILE,OUTFILE))

    ##################################
    ## PRE-FLIGHT CHECK FOR OUTFILE ##
    print("Checking if outfile already exists...")
    if not os.path.exists(OUTFILE):
        print("Creating outfile: "+OUTFILE)
        f = open(OUTFILE,'w')
        f.write("TITLE,CATEGORY,STATE,PRIORITY,DESCRIPTION,JUSTIFICATION,DATE ADDED\n")
        f.close()

    ###################
    ## FILE HANDLERS ##
    with open(INFILE) as fp:
        soup = BeautifulSoup(fp,"lxml")

    
    FORMAT= '%Y%m%d'
    DATE= datetime.now().strftime(FORMAT)
        
    CTR = 1
    for i in range(0, len(soup.find_all(class_='threat'))):
        TITLE = soup.find_all(class_='threat')[i].find('span').get_text()
        CATEGORY = soup.find_all(class_='threat')[i].find(headers='threat-title-category').get_text()
        STATE_PRIORITY = soup.find_all(class_='threat')[i].get_text()
        STATE = re.findall(r'([\[]{1}[a-z,A-Z,0-9 ]+[:]{1}[a-z,A-Z,0-9 ]+[\]]{1}){1}',STATE_PRIORITY)[0]
        PRIORITY = re.findall(r'([\[]{1}[a-z,A-Z,0-9 ]+[:]{1}[a-z,A-Z,0-9 ]+[\]]{1}){1}',STATE_PRIORITY)[1]
        DESCRIPTION = soup.find_all(class_='threat')[i].find(headers='threat-title-description').get_text()
        JUSTIFICATION = soup.find_all(class_='threat')[i].find(headers='threat-title-justification').get_text()
        CTR += 1


        ############################################################
        ## STRIPPING THE INPUT OF COMMAS THAT WILL BREAK THE FILE ##
        TITLE_N = TITLE.replace(',','')     
        CATEGORY_N = CATEGORY.replace(',','')
        STATE_N = STATE.replace(',','')
        PRIORITY_N = PRIORITY.replace(',','')
        DESCRIPTION_N = DESCRIPTION.replace(',','')
        JUSTIFICATION_N = JUSTIFICATION.replace(',','')
    
        OUTPUT = "%s,%s,%s,%s,%s,%s,%s" % (TITLE_N,CATEGORY_N,STATE_N,PRIORITY_N,\
                                           DESCRIPTION_N,JUSTIFICATION_N,DATE)
        APPEND = 'echo "%s" >> %s' % (OUTPUT,OUTFILE)
        call   = os.popen(APPEND)

    sys.exit(0)


############
##  MAIN  ##
def main():
    INFILE=''
    OUTFILE=''

    ######################
    ## ARGUMENT PARSING ##
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hi:o:", ["help","-infile","-outfile"])
    except getopt.GetoptError:
        print(err)
        usage()
        sys.exit(2)

    #####################################
    ## ARGUMENT TO VARIABLE ASSIGNMENT ##
    for o,a in opts:
        if o in ("-h","--help"):
            usage()
            sys.exit(0)
        elif o in ("-i","--infile"):
            INFILE=a
        elif o in ("-o","--outfile"):
            OUTFILE=a
        else:
            assert False, "Unhandled Option!"

    ##########################################
    ## PARAM VERIFICATION AND FUNCTION CALL ##
    if OUTFILE and INFILE:
        if os.path.exists(INFILE):
            tm_parse(INFILE, OUTFILE)
        else:
            print("Input File Does Not Exist!")
            sys.exit(2)

    else:
        print("\nPlease Provide All Required Arguments!\n[INFILE] [OUTFILE]\n")
        usage()
        sys.exit(2)

main()
