#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<stdbool.h>
#include<ctype.h>

/*
 * Tyler Boykin
 *
 * Project that handles value from a config file
 *
 * (nothing fancy) compile with: gcc -o config_parser -Wall config_parser.c
 *
 */

// BL = blacklist approach (returns true default) 
// WL = whitelist approach (returns false default)
struct configs *loadCfg(char *filename);
bool BL_validate_PORT(char *port);
bool BL_validate_ADDRESS(char *address);
bool WL_validate_STATE(char *state);
bool BL_validate_FLAGS(struct configs *cfg);
bool WL_validate_PROTOCOL(char *protocol);
bool BL_validate_ENDPOINTS(char *endpoints);
bool validate_FORMAT(struct configs *cfg);
bool validate_CFG(struct configs *cfg);
void print_loaded(struct configs *cfg);

// Config struct
struct configs
{
	char *address;
	char *port;
	char *protocol;
	char *state;
	struct flags
	{	
		char *flag_list;
		int syn;
		int psh;
		int urg;
		int rst;
		int ack;
		int fin;
	}flags;
	char **endpoints;
	int num_endpoints;

}configs;

int main(int argc, char *argv[])
{
	struct configs *config_list;
	
	if(argc < 2)
	{
		fprintf(stderr,"Please supply a config file\n");
		exit(EXIT_FAILURE);
	}

	config_list = loadCfg(argv[1]);
	if(validate_CFG(config_list))
	{
		print_loaded(config_list);
	}

	return 0;
}
/*
 * i. Opens config file
 * ii. Goes line by line looking for keywords
 * iii. takes those key words and breaks the line up by a delimeter using strtok_r()
 * iv. stores the value in the struct
 *
 * Does not evaluate correctness of data, only basic type checking / error checking.
 */

struct configs *loadCfg(char *filename)
{
	const char *_ADDR = "ADDRESS";
	const char *_PORT = "PORT";			
	const char *_STATE = "STATE";
	const char *_PROTO = "PROTOCOL";
	const char *_FLAGS = "FLAGS";
	const char *_ENDPOINTS = "ENDPOINTS";
	int line_no = 1;		// Debug output for syntax
	int i, ii;				// Generic iterators
	int num_endpoints = 0;	// Number of endpoints.
	int token_len = 0;		// 'Token' being used with strtok_r()
	char *line_buf = NULL;	// Buffer used for each line entry... space is reallocated for each entry.
	size_t line_buf_size = 0;
	ssize_t line_size = 0;
	FILE *cfg;		// config file FD
	char *tokenA;	// Original strtok_k token ([PARAM]=value -> PARAM=[Value])
	char *tokenB;	// Drills down into [Value](PARAM=[ValueA,ValueB] -> PARAM=[ValueA],ValueB)
	char *saveA;	// strtok_r()
	char *saveB;	// strtok_r()
	char *orig;		// Used to restore original string for tokenB
	
	// Init. the configs struct
	struct configs *config_list = malloc(sizeof(struct configs));

	if(! (cfg = fopen(filename,"r")) )
	{
		fprintf(stderr,"Error opening cfg file: %s\n",filename);
		exit(EXIT_FAILURE);	
	}

	line_size = getline(&line_buf, &line_buf_size, cfg);
	while(line_size >= 0)
	{
		for(i=0;i<line_buf_size;i++)
		{
			if(line_buf[i] == '#')
			{
				break;
			}
			else if(line_buf[i] == '=')
			{
				/*
				 * Evaluates [PARAM]=value...  basic schema is detailed below
				 */
				// populate the first token with the first [PARAM]
				tokenA = strtok_r(line_buf,"=",&saveA);

				// evaluate the [PARAM]
				if( (strcmp(tokenA,_ADDR)) == 0)
				{
					// this shift down to PARAM=[value]
					tokenA = strtok_r(NULL,"=",&saveA);
					token_len = strlen(tokenA)+1;

					// create space in the pointer for [value]
					if(! (config_list->address = calloc(token_len,sizeof(char))))
					{
						fprintf(stderr,"Allocation failed | config_list->address\n");
						exit(EXIT_FAILURE);
					}
					// copy value into the space
					strncpy(config_list->address,tokenA,token_len);
					break;
				}
				else if( (strcmp(tokenA,_PORT)) == 0)
				{
					tokenA = strtok_r(NULL,"=",&saveA);
					token_len = strlen(tokenA)+1;
					if(! (config_list->port = calloc(token_len,sizeof(char))))
					{
						fprintf(stderr,"Allocation failed | config_list->port\n");
						exit(EXIT_FAILURE);
					}
					strncpy(config_list->port,tokenA,token_len);
					break;
				}
				else if( (strcmp(tokenA,_STATE)) == 0)
				{
					tokenA = strtok_r(NULL,"=",&saveA);
					token_len = strlen(tokenA)+1;
					if(! (config_list->state = calloc(token_len,sizeof(char))))
					{
						fprintf(stderr,"Allocation failed | config_list->state\n");
						exit(EXIT_FAILURE);
					}
					strncpy(config_list->state,tokenA,strlen(tokenA));
					break;
				}
				else if( (strcmp(tokenA,_PROTO)) == 0)
				{
					tokenA = strtok_r(NULL,"=",&saveA);
					token_len = strlen(tokenA)+1;
					if(! (config_list->protocol = calloc(token_len,sizeof(char))))
					{
						fprintf(stderr,"Allocation failed | config_list->protocol\n");
						exit(EXIT_FAILURE);
					}
					strncpy(config_list->protocol,tokenA,token_len);
					break;

				}
				else if( (strcmp(tokenA,_FLAGS)) == 0)

				{
					tokenA = strtok_r(NULL,"=",&saveA);
					token_len = strlen(tokenA)+1;
					if(! (config_list->flags.flag_list = calloc(token_len,sizeof(char))))
					{
						fprintf(stderr,"Allocation failed | config_list->flags\n");
						exit(EXIT_FAILURE);
					}
					strncpy(config_list->flags.flag_list,tokenA,token_len);
					
					// Defaulting these to 0
					config_list->flags.urg = 0;
					config_list->flags.syn = 0;
					config_list->flags.ack = 0;
					config_list->flags.fin = 0;
					config_list->flags.rst = 0;
					config_list->flags.psh = 0;
					break;
				}
				else if( (strcmp(tokenA,_ENDPOINTS)) == 0)
				{
					// Adjust from [PARAM]=Value to PARAM=[Value]  
					tokenA = strtok_r(NULL,"=",&saveA);

					// Saving the original place of strtok_r
					orig = calloc(strlen(tokenA)+1,sizeof(char));
					strncpy(orig,tokenA,strlen(tokenA));

					// Drill down into PARAM=[Value]
					tokenB = strtok_r(tokenA,",",&saveB);

					while(tokenB != NULL)
					{
						num_endpoints++;
						tokenB = strtok_r(NULL,",",&saveB);
					}
					// store this in the struct
					config_list->num_endpoints = num_endpoints;

					if(! (config_list->endpoints = calloc(num_endpoints,sizeof(char *))))
					{
						fprintf(stderr,"Calloc Error | config_list->endpoints\n");
						exit(EXIT_FAILURE);
					}

					// Restore tokenB to old value (ie 1.1.1.1,2.2.2.2,3.3.3.3)
					tokenB = orig;
					
					// refer back to itself, when doing the initial strtok_r()
					tokenB = strtok_r(tokenB,",",&saveB);
					
					for(ii=0;ii<num_endpoints;ii++)
					{
						if(! (config_list->endpoints[ii] = calloc(sizeof(tokenB)+1,sizeof(char))))
						{
							fprintf(stderr,"Calloc Error | config_list->endpoints->%d\n",ii);
							exit(EXIT_FAILURE);
						}
						strncpy(config_list->endpoints[ii],tokenB,strlen(tokenB));
						tokenB = strtok_r(NULL,",",&saveB);
					}
				}
			}
		}

		line_no++;
		line_size = getline(&line_buf, &line_buf_size, cfg);
	}

	// Nomralization: Rid the struct of newlines
	for(i=0;i<strlen(config_list->address);i++)
	{
		if( (config_list->address[i] == '\n') || (config_list->address[i] == '\r'))
		{
			config_list->address[i] = '\0';
		}
	}
	for(i=0;i<strlen(config_list->port);i++)
	{	
		if( (config_list->port[i] == '\n') || (config_list->port[i] == '\r'))
		{
			config_list->port[i] = '\0';
		}
	}
	for(i=0;i<strlen(config_list->protocol);i++)
	{
		if( (config_list->protocol[i] == '\n') || (config_list->protocol[i] == '\r'))
		{
			config_list->protocol[i] = '\0';
		}
	}
    for(i=0;i<strlen(config_list->state);i++)
    {
        if( (config_list->state[i] == '\n') || (config_list->state[i] == '\r'))
       	{
        	config_list->state[i] = '\0';
       	}
    }
	for(i=0;i<strlen(config_list->flags.flag_list);i++)
	{
		if( (config_list->flags.flag_list[i] == '\n') || (config_list->flags.flag_list[i] == '\r'))
		{
			config_list->flags.flag_list[i] = '\0';
		}
	}
    for(i=0;i<num_endpoints;i++)
    {
		for(ii=0;ii<strlen(config_list->endpoints[i]);ii++)
		{
        	if( (config_list->endpoints[i][ii] == '\n') || (config_list->endpoints[i][ii] == '\r'))
            {
            	config_list->endpoints[i][ii] = '\0';
            }
		}
	}

	free(line_buf);
	line_buf = NULL; 
	fclose(cfg);

	return config_list;
}



bool BL_validate_PORT(char *port)
{
	int len = strlen(port);
	int port_no = atoi(port);
	int i;
	// We're evaluating _PORT as a string
	
	// 1-65535... anything len 0 or 6+ is invalid
	if( (len <= 0) || (len >= 6) )
	{
		fprintf(stderr,"Invalid Port. Incorrect Length.\n");
		return false;
	}
	// make sure all digits
	for(i=0;i<len;i++)
	{
		if(isdigit(port[i]) == 0)
		{
			fprintf(stderr,"Invalid Port. Invalid Char.\n");
			return false;
		}
	}
	// 1-65535
	if(! ((port_no >= 1) && (port_no <= 65535)))
	{
		fprintf(stderr,"Invalid Port. Out of range.\n");
		return false;
	}
	

	return true;
}


bool BL_validate_ADDRESS(char *address)
{
	const char *reserved_bcast = "255.255.255.255";
	const char *reserved_this = "0.0.0.0";
	char *octet;
	char *octet_save;
	char *octet_copy;
	int i, octet_no=0, len=0, dots=0;
	int octet_value;
	len = strlen(address);

	octet_copy = calloc(strlen(address)+1,sizeof(char));
	strncpy(octet_copy,address,len);

	// are they all digits or .'s
	for(i=0;i<len;i++)
	{
		if( (isdigit(address[i]) == 0) && (address[i] != '.'))
		{
			fprintf(stderr,"Invalid Address.  Invalid character(hex: %x )\n",address[i]);
			return false;
		}	
	}
	
	// are there too many octets (indicative by more than 3 .'s)
	for(i=0;i<len;i++)
	{
		if(	(address[i] == '.'))
		{
			dots++;
		}
	}
	if(dots >= 4)
	{
		fprintf(stderr,"Invalid Address. Improper number of octets\n");
		return false;
	}
	// no 255.255.255.255
	if(strncmp(address,reserved_bcast,strlen(reserved_bcast)) == 0)
	{
		fprintf(stderr,"Invalid Address. Broadcast not allowed\n");
		return false;
	}
	// no 0.0.0.0
	if(strncmp(address,reserved_this,strlen(reserved_this)) == 0)
	{
		fprintf(stderr,"Invalid Address. 0.0.0.0 not allowed\n");
		return false;
	}
	octet = strtok_r(octet_copy,".",&octet_save);
	while(octet != NULL)
	{
		octet_value = atoi(octet);	
		octet_no++;
		// make sure that three digit octets only have 2xx.2xx.2xx.2xx maximum
		if(	( strlen(octet) > 3) || (strlen(octet) < 1) )
		{
			fprintf(stderr,"Invalid Address. Invalid Octet size\n");
			return false;
		}
		// no 0xx.xxx.xxx.xxx
		if( (octet_value <= 0) && (octet_no == 1) )
		{
			fprintf(stderr,"Invalid Address. Cannot start with 0\n");
			return false;
		}
		// 1-255,  no 0 or 256+
		if(! ((octet_value >= 0) && (octet_value <= 255)))
		{
			fprintf(stderr,"Invalid Address. Octet range 1-255\n");
			return false;
		}
		octet = strtok_r(NULL,".",&octet_save);
	}
	return true;
}

bool BL_validate_FLAGS(struct configs *cfg)
{
	int i;
	int len1 = strlen(cfg->flags.flag_list);

	for(i=0;i<len1;i++)
	{
		if( (cfg->flags.flag_list[i] != 'f') && (cfg->flags.flag_list[i] != 'p') &&
			(cfg->flags.flag_list[i] != 's') && (cfg->flags.flag_list[i] != 'r') &&
			(cfg->flags.flag_list[i] != 'a') && (cfg->flags.flag_list[i] != 'u') )
		{
			return false;
		}
		else
		{
			if(cfg->flags.flag_list[i] == 'f')
			{
				cfg->flags.fin = 1;
			}
			else if(cfg->flags.flag_list[i] == 'p')
			{		
				cfg->flags.psh = 1;
			}
			else if(cfg->flags.flag_list[i] == 'u')
			{
				cfg->flags.urg = 1;
			}
			else if(cfg->flags.flag_list[i] == 's')
			{
				cfg->flags.syn = 1;
			}
			else if(cfg->flags.flag_list[i] == 'a')
			{
				cfg->flags.ack = 1;
			}
			else if(cfg->flags.flag_list[i] == 'r')
			{
				cfg->flags.rst = 1;
			}	
		}
	}
	return true;
}

bool WL_validate_STATE(char *state)
{
	// stole these states from VyOS
	char states[4][12] = {"invalid","new","established","related"};
	int i;
	int len;
	
	for(i=0;i<4;i++)
	{
		len = strlen(states[i]);
		if( (strncmp(state,states[i],len) == 0) )
		{
			return true;
		}
	}

	fprintf(stderr,"Unknown State!  Acceptable states [ new, related, established, invalid ]\n");
	return false;
}

bool WL_validate_PROTOCOL(char *proto)
{
	// tcp, udp, esp, ospf, eigrp, icmp, igmp, gre, ah, rsvp, l2tp, vrrp, isis, mpls, 
	char proto_list[][8] = {"tcp", "udp","esp","ospf",
							"eigrp","icmp","igmp","gre",
							"ah","rsvp","l2tp","vrrp","isis",
							"mpls"};
	int i;
	for(i=0;i<14;i++)
	{
		if( (strcmp(proto,proto_list[i]) == 0))
		{
			return true;
		}
	}
	fprintf(stderr,"Invalid Protocol entry\n");
	return false;
}

bool BL_validate_ENDPOINTS(struct configs *cfg)
{
	int i;
	for(i=0;i<cfg->num_endpoints;i++)
	{
		if(!(BL_validate_ADDRESS(cfg->endpoints[i])))
		{
			fprintf(stderr,"Invalid Endpoint. Entry %d\n",i);
			return false;
		}
	}
	return true;
}

bool validate_CFG(struct configs *cfg)
{
	if(! BL_validate_PORT(cfg->port))
	{
		return false;
	}
	if(! BL_validate_ADDRESS(cfg->address))
	{
		return false;
	}
	if(! WL_validate_STATE(cfg->state))
	{
		return false;
	}
	if(! BL_validate_FLAGS(cfg))
	{
		return false;
	}
	if(! WL_validate_PROTOCOL(cfg->protocol))
	{
		return false;
	}
	if(! BL_validate_ENDPOINTS(cfg))
	{
		return false;
	}

	return true;
}

void print_loaded(struct configs *cfg)
{
	int i;
	printf(	"- ADDRESS: %s\n"
			"- PORT:	%s\n"
			"- PROTO: %s\n"
			"- STATE: %s\n"
			"- FLAGS: %s\n"
			"---> Syn: %d\n"
			"---> Fin: %d\n"
			"---> Ack: %d\n"
			"---> Urg: %d\n"
			"---> Rst: %d\n"
			"---> Psh: %d\n",
			cfg->address,
			cfg->port,
			cfg->protocol,
			cfg->state,
			cfg->flags.flag_list,
			cfg->flags.syn,
			cfg->flags.fin,
			cfg->flags.ack,
			cfg->flags.urg,
			cfg->flags.rst,
			cfg->flags.psh);

	printf( "- ENDPOINTS\n");
	for(i=0;i<cfg->num_endpoints; i++)
	{
		printf("---> %s\n",cfg->endpoints[i]);
	}

}
