#!/Library/installapplications/Python.framework/Versions/3.8/bin/python3
from time import sleep
import os
import subprocess


PING_HOSTNAME = 'adrastea.brandwatch.net'
VPNUTIL = '/usr/local/bin/vpnutil'
VPNLABEL = 'VPN (IKEv2) Brandwatch'
VPNLABEL ='VPN (IKEv2) ' #testing
IASHOSTNAME = 'https://adrastea.brandwatch.net'


def invokecmd(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutput, stderrdata = process.communicate()
    return {'stdout': stdoutput, 'stderr': stderrdata}


def hostping(hostname):
    FNULL = open(os.devnull, 'w')
    response = invokecmd(["ping","-c","1", hostname])
    return response


def vpnconnected():
    sleep(20)
    response = invokecmd([VPNUTIL,"status",VPNLABEL])
    
    if b'Connected' in response['stdout']:
        return True
    else:
        print("Connection failed will try again")
        #kill the process as its stuck connecting
        invokecmd(['/usr/bin/killall', '-9', 'NEIKEv2Provider'])
        return False


def validvpn(label):
    status = invokecmd([VPNUTIL, 'list'])
    if VPNLABEL.encode('utf8') in status['stdout']:
        return True
    return False


def vpnutilcheck():
    if os.path.isfile(VPNUTIL):
        return True
    else:
        return False


def launchvpn():
    if validvpn(VPNLABEL):
        cmd = [VPNUTIL, 'status', VPNLABEL]
        status = invokecmd(cmd)
        if b"Connected" not in status['stdout']:
            invokecmd([VPNUTIL,"start",VPNLABEL])
            while not vpnconnected():
                invokecmd([VPNUTIL,"start",VPNLABEL])
            else:
                print("IAS: VPN is connected!")
                return True
        else:
            print(f"IAS: {VPNLABEL} - Does Not exist!")
            return False
    else:
        #print("IAS: VPN Label is wrong")
        return False
    return True


def hostreachable():
    cmd = ['/usr/bin/nscurl',IASHOSTNAME]
    status = invokecmd(cmd)
    if b'error' in status['stderr']:
        return False
    else:
        return True

#vpnlaunched = launchvpn()
#if vpnlaunched:
 #   print("YEAH!")

print("Waiting for vpnutil")
while not vpnutilcheck():
    sleep(5)
print("Waiting for connection")
if not hostreachable():
    while not launchvpn():
        pass
else:
    print("Host reachable VPN not required")





