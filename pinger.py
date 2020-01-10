#! /usr/bin/env python
import subprocess,sys,time,os,signal


def signal_handler(sig, frame):
    print('Exiting gracefully Ctrl-C detected...')
    sys.exit(0)

def progress(count, total, response,line):
    # Draw progress bar if host not reachable print . else !
    bar_len = 15

    filled_len = int(round(bar_len * count / float(total)))

    if (response == 0):
        status = line.rstrip() + " is Reachable "
        bar = '!' * filled_len + '-' * (bar_len - filled_len)
    else:
        status = line.rstrip() + " is Not reachable "
        bar = '.' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] ...%s\r' % (bar, status))

def clear():
    # check and make call for specific operating system
    _ = subprocess.call('clear' if os.name =='posix' else 'cls')

def main():
    try:
        with open("hosts", "r") as f:
            lines = f.readlines()
    except IOError:
        print
        "Could not read file hosts"

    clear()

    i = 1

    while True:
        #for each host in the hosts file send ping and surpress os output
        for line in lines:
             response=subprocess.Popen(["ping", "-c", "1", line.strip()],
             stdout=subprocess.PIPE,
             stderr=subprocess.STDOUT)
             stdout, stderr = response.communicate()

             progress(i, 15, response.returncode, line)
             print

        time.sleep(1)
        clear()
        i = i + 1
        if i == 15:
            i = 1

        sys.stdout.flush()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler) # catch ctrl-c and call handler to terminate the script
    main()
