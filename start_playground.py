#Search for the word CHANGEME in this script to see where you can make changes

#Requirements:
#Minimega v.2.0: minimega.org
#Before compiling, modify a line in vminfo.go file located under src/minimega folder
#Change from: args = append(args, "0.0.0.0:"+sId)
#Change to: args = append(args, "0.0.0.0:"+sId+",password")

#VNC2FLV: http://www.unixuser.org/~euske/python/vnc2flv/ (install by running "pip install vnc2flv")

import os, json, hashlib, random
from time import sleep

#Compiled minimega binary
minimega_path = "/home/livlab/minimega-2.0/bin/minimega" #CHANGEME
#Minimega web folder
minimega_web_path = "/home/livlab/minimega-2.0/misc/web" #CHANGEME
#Kali linux iso
kali_path = "/home/livlab/kali.iso" #CHANGEME
#Web1 and Web2 lab iso
web1_path = "/home/livlab/web_for_pentester_i386.iso" #CHANGEME
web2_path = "/home/livlab/web_for_pentester_II_i386.iso" #CHANGEME

minimega_start = minimega_path + " -nostdin &"
minimega_cmd = minimega_path + " -e "

print "Starting minimega"
os.system(minimega_start)#Start minimega
sleep(5)#Sleep for 5 seconds

#Start minimega's web interface
#Screenshots of all the machines will be displayed in this mode. To disable it, just comment the line out.
#If you do disable web access, the students will have to use a VNC client and they'll need port numbers.
os.system(minimega_cmd + "web root " + minimega_web_path)

#Enable Kernel Samepage Merging.
os.system(minimega_cmd + "optimize ksm true")

print "Starting dnsmasq"
#Network configuration
#Kill dnsmasq if it's running
os.system("killall dnsmasq")
#Create a tap so we can do dhcp
os.system(minimega_cmd + "tap create 1 ip 10.2.0.1/24")
#Start dnsmasq / dhcp server to assign IP's
os.system(minimega_cmd + "dnsmasq start 10.2.0.1 10.2.0.2 10.2.0.254")

#Virtual machine configuration
#Assign the machines 2GB
os.system(minimega_cmd + "vm config memory 2048")
#Assign VM's to network 1
os.system(minimega_cmd + "vm config net 1")

print "Starting VMs"
#Launch and start VMs
#Start web for pentesters 1 and 2
os.system(minimega_cmd + "vm config disk "+web1_path)
os.system(minimega_cmd + "vm launch web1")
os.system(minimega_cmd + "vm config disk "+web2_path)
os.system(minimega_cmd + "vm launch web2")
os.system(minimega_cmd + "vm start all")
#Start 5 kali linux VMs
os.system(minimega_cmd + "vm config disk "+kali_path)
os.system(minimega_cmd + "vm launch kali1")
os.system(minimega_cmd + "vm launch kali2")
os.system(minimega_cmd + "vm launch kali3")
os.system(minimega_cmd + "vm launch kali4")
os.system(minimega_cmd + "vm launch kali5")
os.system(minimega_cmd + "vm start all")

print "Generating and assigning passwords"
#Assign passwords to all the kali VMs
vmpw_list = {}
for numb in range(1,6):
        password = hashlib.md5(str(random.random())).hexdigest()[:6]
        vmname = "kali"+str(numb)
        vmpw_list[vmname] = password,(numb+1)
        testcmd = """'{ "execute": "change", "arguments": { "device": "vnc", "target": "password", "arg": "%s" } }'"""%password
        os.system(minimega_cmd+"vm qmp "+vmname+" "+json.dumps(testcmd))

print "Starting the recordings"
#Create password files
for line in vmpw_list:
        passfile = open(line,'w')
        passfile.write(vmpw_list[line][0])
        passfile.close()
        #Start recording
        os.system("flvrec.py -o "+line+".flv -P "+line+" localhost:" + str(vmpw_list[line][1]) + "&") #.flv files will contain the recordings

print "\n"
print "Web interface is on port 9001"
print "\n"
print "Passwords for all the VM's"
print "VMname \t Password \t port"
for line in vmpw_list:
        print line + "\t" + vmpw_list[line][0] + "\t" + str((vmpw_list[line][1]+5900))
print "\n"
print "\'minimega -e quit\' will kill minimega"
