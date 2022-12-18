import os, time, signal, subprocess, console_ctrl

def gatherIPs():
    fin = False
    IPs = []
    timeToRun = input("How many minutes would you like each test to run? ")

    while not fin:
        try:
            timeToRun = float(timeToRun)
        except:
            print("The entered value is invalid")
            timeToRun = 0.0
        while timeToRun <= 0.0:
            timeToRun = input("How many minutes would you like each test to run? ")
            try:
                timeToRun = float(timeToRun)
            except:
                print("The entered value is invalid")
                timeToRun = 0.0

        IP = input("Enter an IP to ping: ")
        IPVerify = IP.split('.')

        if len(IPVerify) != 4:
            print("This IP address is not valid")
        else:
            count = 0
            invalid = False
            for num in IPVerify:
                if int(num) > 255 or int(num) < 0:
                    invalid = True
                else:
                    count += 1
            if invalid:
                print("This IP address is not valid")
            if count == 4:
               IPs.append(IP) 

        moreIPs = input("Enter another IP address? Y or N ")

        if moreIPs == 'n' or moreIPs == 'N':
            fin = True
        elif moreIPs == 'y' or moreIPs == 'Y':
            pass
        else:
            while moreIPs != 'y' and  moreIPs != 'Y' and moreIPs != 'n' and moreIPs != 'N':
                moreIPs = input("Enter another IP address? Y or N ")
                if moreIPs == 'n' or moreIPs == 'N':
                    fin = True
                elif moreIPs == 'y' or moreIPs == 'Y':
                    pass 
 
    return IPs,timeToRun

def formatResultsFile():
    count = 0

    with open('results.txt') as results:
        lines = results.readlines()
        for line in lines:
            if line.find("rtt") != -1:
                lines[count] = lines[count] + "\n"
            count += 1
    results.close()
    
    with open('results.txt','w') as results:
        for line in lines:
            results.write(line)

    print("\nResults can be viewed in the results.txt file")
  
def testIPs(IPs,timeToRun):
    with open('results.txt','w') as logFile:
        for IP in IPs:
            print("Ping test on {} is in progress".format(IP))
            process = subprocess.Popen("ping {}".format(IP),stdout=logFile,shell=True)
            time.sleep(timeToRun * 60) # convert to seconds from minutes
            process.send_signal(signal.SIGINT) # send CTRL + C (We need this for the ending statistics)
            time.sleep(.5)
            process.kill()
            print("Ping test on {} is complete \n".format(IP))

 
def main():
    IPList,timeToRun = gatherIPs()
    testIPs(IPList,timeToRun)
    formatResultsFile()

if __name__ == "__main__":
    main()
