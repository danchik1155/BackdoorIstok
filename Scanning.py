import os
import platform
import threading
import socket
from datetime import datetime
import subprocess as sp

def getMyIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Создаем сокет (UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Настраиваем сокет на BROADCAST вещание.
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

def scan_Ip(ip, strin):
    net = getMyIp()
    net_split = net.split('.')
    a = '.'
    net = net_split[0] + a + net_split[1] + a + net_split[2] + a

    oss = platform.system()
    if (oss == "Windows"):
        ping_com = "ping -n 1 -a "
    else:
        ping_com = "ping -c 1 "

    addr = net + str(ip)
    comm = ping_com + addr
    response = os.popen(comm)
    data = response.readlines()
    #response = sp.Popen(comm)
    #data = response.communicate()[0]
    name = data[1].split(' ')
    for line in data:
        if 'TTL' in line:
            response_art = os.popen('arp -a')
            data_arp = response_art.readlines()
            #response_art = sp.Popen('arp -a')
            #data_arp = response_art.communicate()
            for line_arp in data_arp:
                flag = line_arp.split()
                if len(flag) > 0 and flag[0] == addr:
                    tmp =(addr+"--> Ping Ok"+ '    '+ name[3]+'    '+flag[1])
                    strin.append([addr, flag[1]])

            break

def sscan():
    net = getMyIp()
    net_split = net.split('.')
    a = '.'
    net = net_split[0] + a + net_split[1] + a + net_split[2] + a

    start_point = 0
    end_point = 255

    t1 = datetime.now()
    #print("Scanning in Progress:")
    #print('IP                 Status          Name            MAC')
    strin = []
    for ip in range(start_point, end_point):
        if ip == int(net_split[3]):
            pass
            #continue
        potoc = threading.Thread(target=scan_Ip, args=[ip, strin])
        potoc.start()
        # potoc.join()
    potoc.join()
    t2 = datetime.now()
    total = t2 - t1
    for i in strin:
        if '94-39-e5-70-d5-ad' in i:
            return i[0]
    return 'Error'
        #print(i)
    #print('Find ip :', len(strin))
    #print("Scanning completed in: ", total)
