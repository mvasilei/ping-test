#! /usr/bin/env python
from datetime import datetime, timedelta
import subprocess, re, signal

def signal_handler(sig, frame):
    print('Exiting gracefully Ctrl-C detected...')
    sys.exit(0)

def main():
    try:
        with open('/etc/hosts', 'r') as f:
            lines = f.readlines()
    except IOError:
        print 'Could not read file hosts'

    pattern = re.compile(r'^(?P<module>LC\/0\/[0-9]\/CPU0).*(?P<error>LICENSE)', re.MULTILINE)
    pe = re.compile(r'ukx[a-z]{2}[1-9][ap][be][0-1][1-9]')
    igw = re.compile(r'[a-z]{4}[0-9]{2}-igw-a1')

    yesterday = datetime.strftime(datetime.now() - timedelta(1), ' %b %d ')
    flag = 0

    for host in lines:
        if (re.findall(pe, host.lower()) or re.findall(igw, host.lower())):
            ip, name = host.split()

            response = subprocess.Popen(['rcomauto ' + name.strip() + ' "show log start' + yesterday + ' 00:00:00 | include LICENSE"'],
                                        stdout=subprocess.PIPE,
                                        shell=True)

            print name
            if response.returncode == None :
                #m = pattern.findall(response.communicate()[0].strip('\n'))

                for m in pattern.finditer(response.communicate()[0].strip('\n')):
                    if flag == 0:
                        with open('swap','w') as f:
                            f.write('Host:' + name + ' Module: ' + m.group('module') + ' needs Licensing\n')
                    else:
                        with open('swap','a') as f:
                            f.write('Host:' + name + ' Module: ' + m.group('module') + ' needs Licensing\n')

                    flag = 1
            else:
                print 'An error occurred'

    if flag == 1:
            response = subprocess.Popen(['mailx -s "Unlicensed ASR9K Nodes" IPMobileCore@vodafone.com < swap'],
                                        stdout=subprocess.PIPE,
                                        shell=True)
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)  # catch ctrl-c and call handler to terminate the script
    main()
