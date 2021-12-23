import subprocess as sub
import argparse 
import re
import random

interface = 'en1'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface', dest = 'interface', help = 'Interface name to change mac')
    option = parser.parse_args()

    if not option.interface:
        parser.error("Please specify an interface in the arguments, use --help for more info")
    return option

#Randomize new mac address
new_mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255),random.randint(0, 255))


#Get Current mac to compare
def get_current_mac(interface):
  output = sub.check_output(['ifconfig', interface], universal_newlines = True)
  search_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", output)
  if search_mac:
    print('Old MAC: ' + search_mac.group(0))
    old_mac = search_mac.group(0)

  else:
    print('[-] Could not read the MAC Address')

def maskon(interface, new_mac):
    print("\n Putting Mask On \n")
    sub.call(['sudo', 'ifconfig', interface, 'ether', new_mac])


mac = get_current_mac(interface)

maskon(interface, new_mac)

if mac != new_mac:
    print('MAC has been changed')
    print('New mac is ' + new_mac)
else:
    print('Could not change MAC')