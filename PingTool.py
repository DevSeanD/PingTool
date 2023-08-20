import os, time, signal, subprocess

def gatherIPs():
    fin = False
    ips = []
    numOfPackets = input("How many ICMP packets would you like to send? ")

    while not fin:
        try:
            numOfPackets = int(numOfPackets)
        except:
            print("The entered value is invalid")
            numOfPackets = 0
        while int(numOfPackets) <= 0:
            numOfPackets = input("How many ICMP packets would you like to send? ")
            try:
                numOfPackets = int(numOfPackets)
            except:
                print("The entered value is invalid")
                numOfPackets = 0.0

        ip = input("Enter an IP to ping: ")
        ipVerify = ip.split('.')

        if len(ipVerify) != 4:
            print("This IP address is not valid")
        else:
            count = 0
            invalid = False
            for num in ipVerify:
                if int(num) > 255 or int(num) < 0:
                    invalid = True
                else:
                    count += 1
            if invalid:
                print("This IP address is not valid")
            if count == 4:
               ips.append(ip) 
 
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
 
    return ips,numOfPackets

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
  
def testIPs(ips,numOfPackets):
    with open('results.txt','w') as logFile:
        for ip in ips:
            print("Ping test on {} is in progress".format(ip))
            process = subprocess.Popen("ping {} -c {} | while read pong; do echo $(date): $pong; done >> results.txt".format(ip,numOfPackets),shell=True)
            process.wait()
 
def main():
    ipList,numOfPackets = gatherIPs()
    testIPs(ipList,numOfPackets)
    formatResultsFile()

if __name__ == "__main__":
    main()
