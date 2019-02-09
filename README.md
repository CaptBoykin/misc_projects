# misc_projects
Various tools I've made while during my growth and developement.  None of these should require any installation, save installing python modules.  

### firewall_hero_iptables
This script takes recently established connections and applies them towards an iptables ruleset.  This was utilized in Sam Bowne's Firewall Hero challenges.
https://attack.samsclass.info/firewallhero/

### hashCheck.py
An exercise in tkinter and graphical interfaces.  Utilizes hash comparison to detect collisions / tampering.

### nmap_parse.py
Takes the output from NMAP and puts it into .csv.  20180103:  Supports Greppable and XML format.

```
Usage:   python3 ./nmap_parser.py [OPTION] -i [IN FILE] -o [OUTFILE]
Example: python3 nmap_parse.py -g -i /my/file -o /home/myout.csv

Options:
    -x|--xml        Parse NMAP XML Output
    -n|--normal     Parse Normal NMAP Output
    -g|--grepable   Parse Grepable NMAP Output
    -i|--infile     Input File
    -o|--outfile    Output File (ie../home/myout.csv)
    -h|--help       Halp plz..
```

### proxychainsFill.py
A script I wrote to refill and harvest lists or proxyservers into proxychains configuration file.  Utilizes BeautifulSoup to pull proxy information.
```
Usage:  python3 ./proxychainsFill.py [a|r]

Options:
    -a|--append     Append to existing proxychains.conf
    -r|--refill     Clear existing, and start from scratch
```

### tm2csv.py
Similar to nmap_parse.  This takes the Microsoft Threat Modeling HTML output and generates a csv.
```
Usage:      python3 ./tm2csv.py -i [IN FILE] -o [OUTFILE]
Example:    python3 ./tm2csv.py -i my_tm_doc.html -o my_tm_results.csv

Options:
    -i|--infile     Input File
    -o|--outfile    Output File (ie../home/myout.csv)
    -h|--help       Halp plz..
```
